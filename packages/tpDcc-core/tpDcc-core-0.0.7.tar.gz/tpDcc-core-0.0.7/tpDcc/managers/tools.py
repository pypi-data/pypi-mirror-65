#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains implementation for DCC tools
"""

from __future__ import print_function, division, absolute_import

import os
import inspect
from collections import OrderedDict

import appdirs

import tpDcc as tp
from tpDcc import register
from tpDcc.core import plugin, tool
from tpDcc.libs.python import decorators, python, importer, path as path_utils

if python.is_python2():
    import pkgutil as loader
else:
    import importlib as loader


class ToolImporter(importer.Importer, object):
    def __init__(self, tool_pkg, debug=False):

        self.tool_path = tool_pkg.filename

        super(ToolImporter, self).__init__(module_name=tool_pkg.fullname, debug=debug)

    def get_module_path(self):
        """
        Returns path where module is located
        :return: str
        """

        return self.tool_path


class ToolsManager(plugin.PluginsManager, object):

    INTERFACE = tool.DccTool

    def __init__(self):
        super(ToolsManager, self).__init__()

        self._layout = dict()

    # ============================================================================================================
    # BASE
    # ============================================================================================================

    def register_plugin(
            self, package_name, package_loaders, environment, root_package_name=None, config_dict=None, load=True):
        """
        Implements register_plugin function
        Registers a plugin instance to the manager
        :param package_loaders: plugin instance to register
        :param environment:
        :param config_dict:
        :param load:
        :return: Plugin
        """

        if not package_loaders:
            return False

        package_loader = package_loaders[0]

        plugin_path = package_loader.fullname

        if not config_dict:
            config_dict = dict()

        config_dict.update({
            'join': os.path.join,
            'user': os.path.expanduser('~'),
            'filename': package_loader.filename,
            'fullname': package_loader.fullname
        })

        if package_name not in self._plugins:
            self._plugins[package_name] = dict()

        plugins_found = list()
        version_found = None
        for sub_module in loader.walk_packages([package_loader.filename]):
            importer, sub_module_name, _ = sub_module
            qname = '{}.{}'.format(package_loader.fullname, sub_module_name)
            try:
                mod = importer.find_module(sub_module_name).load_module(sub_module_name)
            except Exception as exc:
                tp.logger.error('Impossible to register plugin: "{}"'.format(plugin_path), exc_info=True)
                continue

            if qname.endswith('__version__') and hasattr(mod, '__version__'):
                if version_found:
                    tp.logger.warning('Already found version: "{}" for "{}"'.format(version_found, plugin_path))
                else:
                    version_found = getattr(mod, '__version__')

            mod.LOADED = load

            for cname, obj in inspect.getmembers(mod, inspect.isclass):
                if issubclass(obj, self.INTERFACE):
                    plugin_config_dict = obj.config_dict(file_name=package_loader.filename) or dict()
                    if not plugin_config_dict:
                        continue
                    plugin_id = plugin_config_dict.get('id', None)
                    plugin_name = plugin_config_dict.get('name', None)
                    plugin_icon = plugin_config_dict.get('icon', None)
                    if not plugin_id:
                        tp.logger.warning(
                            'Impossible to register plugin "{}" because its ID is not defined!'.format(plugin_path))
                        continue
                    if not plugin_name:
                        tp.logger.warning(
                            'Impossible to register plugin "{}" because its name is not defined!'.format(plugin_path))
                        continue
                    if plugin_id in self._plugins[package_name]:
                        tp.logger.warning(
                            'Impossible to register plugin "{}" because its ID "{}" its already defined!'.format(
                                plugin_path, plugin_id))
                        continue

                    if not version_found:
                        version_found = '0.0.0'
                    obj.VERSION = version_found
                    obj.FILE_NAME = package_loader.filename
                    obj.FULL_NAME = package_loader.fullname

                    plugins_found.append((qname, version_found, obj))
                    version_found = True

        if not plugins_found:
            tp.logger.warning('No plugins found in module "{}". Skipping ...'.format(plugin_path))
            return False
        if len(plugins_found) > 1:
            tp.logger.warning(
                'Multiple plugins found ({}) in module "{}". Loading first one. {} ...'.format(
                    len(plugins_found), plugin_path, plugins_found[-1]))
            plugin_found = plugins_found[-1]
        else:
            plugin_found = plugins_found[0]
        plugin_loader = loader.find_loader(plugin_found[0])

        # Check if DCC specific implementation for plugin exists
        dcc_path = '{}.dccs.{}'.format(plugin_path, tp.Dcc.get_name())
        dcc_loader = None
        dcc_config = None
        try:
            dcc_loader = loader.find_loader(dcc_path)
        except ImportError:
            pass

        plugin_config_dict = plugin_found[2].config_dict(file_name=package_loader.filename) or dict()
        plugin_id = plugin_config_dict['id']
        plugin_name = plugin_config_dict['name']
        plugin_icon = plugin_config_dict['icon']

        plugin_config_name = plugin_path.replace('.', '-')
        plugin_config = tp.ConfigsMgr().get_config(
            config_name=plugin_config_name, package_name=package_name, root_package_name=root_package_name,
            environment=environment, config_dict=config_dict, extra_data=plugin_config_dict)

        if dcc_loader:
            dcc_path = dcc_loader.fullname
            dcc_config = tp.ConfigsMgr().get_config(
                config_name=dcc_path.replace('.', '-'), package_name=package_name,
                environment=environment, config_dict=config_dict)

        # Register resources
        def_resources_path = os.path.join(package_loader.filename, 'resources')
        # resources_path = plugin_config.data.get('resources_path', def_resources_path)
        resources_path = plugin_config_dict.get('resources_path', None)
        if not resources_path or not os.path.isdir(resources_path):
            resources_path = def_resources_path
        if os.path.isdir(resources_path):
            tp.ResourcesMgr().register_resource(resources_path, key='tools')
        else:
            tp.logger.info('No resources directory found for plugin "{}" ...'.format(plugin_name))

        # Register DCC specific resources
        if dcc_loader and dcc_config:
            def_resources_path = os.path.join(dcc_loader.filename, 'resources')
            resources_path = dcc_config.data.get('resources_path', def_resources_path)
            if not resources_path or not os.path.isdir(resources_path):
                resources_path = def_resources_path
            if os.path.isdir(resources_path):
                tp.ResourcesMgr().register_resource(resources_path, key='plugins')
            else:
                tp.logger.info('No resources directory found for plugin "{}" ...'.format(plugin_name))

        # Create tool loggers directory
        default_logger_dir = os.path.normpath(os.path.join(os.path.expanduser('~'), 'tpDcc', 'logs', 'tools'))
        default_logging_config = os.path.join(package_loader.filename, '__logging__.ini')
        logger_dir = plugin_config_dict.get('logger_dir', default_logger_dir)
        if not os.path.isdir(logger_dir):
            os.makedirs(logger_dir)
        logging_file = plugin_config_dict.get('logging_file', default_logging_config)

        self._plugins[package_name][plugin_id] = {
            'name': plugin_name,
            'icon': plugin_icon,
            'package_name': package_name,
            'loader': package_loader,
            'config': plugin_config,
            'config_dict': plugin_config_dict,
            'plugin_loader': plugin_loader,
            'plugin_package': package_loader.fullname,
            'plugin_package_path': package_loader.filename,
            'version': plugin_found[1] if plugin_found[1] is not None else "0.0.0",
            'dcc_loader': dcc_loader,
            'dcc_package': dcc_loader.fullname if dcc_loader else None,
            'dcc_package_path': dcc_loader.filename if dcc_loader else None,
            'dcc_config': dcc_config,
            'logging_file': logging_file,
            'plugin_instance': None
        }

        tp.logger.info('Plugin "{}" registered successfully!'.format(plugin_path))

        return True

    def reload_plugin(self, plugin_id, debug=False):
        """
        Implements reload_plugin function
        Reloads given plugin
        :param plugin_id: str
        :param debug: bool
        :return:
        """

        plugin_data = self.get_plugin_data_from_id(plugin_id)
        if not plugin_data:
            tp.logger.warning('Plugin with id "{}" not found! Impossible to reload.'.format(plugin_id))
            return False

        package_loader = plugin_data.get('loader', None)
        if not package_loader:
            tp.logger.warning('Loader for plugin with id "{}" not found! Impossible to reload'.format(plugin_id))
            return False

        plugin_config = plugin_data.get('config', None)
        if not plugin_config:
            tp.logger.warning('Config for plugin id "{}" not found! Impossible to reload'.format(plugin_id))
            return False

        dcc_loader = plugin_data.get('dcc_loader', None)
        dcc_config = plugin_data.get('dcc_config', None)

        plugin_importer = plugin.PluginImporter(package_loader, debug=debug)
        import_order = ['{}.{}'.format(package_loader.fullname, mod) for mod in
                        plugin_config.data.get('import_order', list())]
        skip_modules = ['{}.{}'.format(package_loader.fullname, mod) for mod in
                        plugin_config.data.get('skip_modules', list())]
        plugin_importer.import_packages(order=import_order, only_packages=False, skip_modules=skip_modules)
        plugin_importer.reload_all()

        if dcc_loader:
            dcc_importer = plugin.PluginImporter(dcc_loader, debug=debug)
            dcc_import_order = list()
            dcc_skip_modules = list()
            if dcc_config:
                dcc_import_order = ['{}.{}'.format(
                    package_loader.fullname, mod) for mod in dcc_config.data.get('import_order', list())]
                dcc_skip_modules = ['{}.{}'.format(
                    package_loader.fullname, mod) for mod in dcc_config.data.get('skip_modules', list())]
            dcc_importer.import_packages(order=dcc_import_order, only_packages=False, skip_modules=dcc_skip_modules)
            dcc_importer.reload_all()

    def get_plugin_data_from_id(self, plugin_id, package_name=None):
        """
        Returns registered plugin data from its id
        :param plugin_id: str
        :param package_name: str
        :return: dict
        """

        if not plugin_id:
            return None

        if not package_name:
            package_name = plugin_id.replace('.', '-').split('-')[0]

        if package_name and package_name not in self._plugins:
            tp.logger.error('Impossible to retrieve data from id: package "{}" not registered!'.format(package_name))
            return None

        return self._plugins[package_name][plugin_id] if plugin_id in self._plugins[package_name] else None

    def get_plugin_data_from_plugin_instance(self, plugin, as_dict=False, package_name=None):
        """
        Returns registered plugin data from a plugin object
        :return: dict
        """

        plugin_data = super(ToolsManager, self).get_plugin_data_from_plugin_instance(
            plugin=plugin, as_dict=as_dict, package_name=package_name)
        if plugin_data:
            return plugin_data

        if not plugin or not hasattr(plugin, 'config'):
            return None

        if not package_name:
            package_name = plugin.PACKAGE
        if not package_name:
            tp.logger.error('Impossible to retrieve data from plugin with undefined package!')
            return None

        if package_name not in self._plugins:
            tp.logger.error(
                'Impossible to retrieve data from instance: package "{}" not registered!'.format(package_name))
            return None

        plugin_id = plugin.config.data.get('id', None)
        if plugin_id and plugin_id in self._plugins:
            if as_dict:
                return {
                    plugin_id: self._plugins[package_name][plugin_id]
                }
            else:
                return self._plugins[package_name][plugin_id]

        return None

    def cleanup(self):
        tp.logger.info('Cleaning tools ...')
        for plug_name, plug in self._plugins.items():
            plug.cleanup()
            tp.logger.info('Shutting down tool: {}'.format(plug.ID))
            self.unload(plug_name)

        self._plugins = dict()
        for package_name in self._plugins.keys():
            tp.MenusMgr().remove_previous_menus(package_name=package_name)

    # ============================================================================================================
    # TOOLS
    # ============================================================================================================

    def load_package_tools(self, package_name, root_package_name=None, tools_to_load=None, dev=True, config_dict=None):
        """
        Loads all tools available in given package
        """

        environment = 'development' if dev else 'production'

        if not tools_to_load:
            return
        tools_to_load = python.force_list(tools_to_load)

        if config_dict is None:
            config_dict = dict()

        tools_to_register = OrderedDict()
        tools_path = '{}.tools.{}'
        for tool_name in tools_to_load:
            pkg_path = tools_path.format(package_name, tool_name)
            pkg_loader = loader.find_loader(pkg_path)
            if not pkg_loader:
                # tp.logger.warning('No loader found for tool: {}'.format(pkg_path))
                continue
            if tool_name not in tools_to_register:
                tools_to_register[tool_name] = list()
            tools_to_register[tool_name].append(pkg_loader)

        for pkg_loaders in tools_to_register.values():
            self.register_plugin(
                package_name=package_name, root_package_name=root_package_name, package_loaders=pkg_loaders,
                environment=environment, load=True, config_dict=config_dict)

    def launch_tool(self, tool_inst, *args, **kwargs):
        """
        Launches given tool class
        :param tool_inst: cls, DccTool instance
        :param args: tuple, arguments to pass to tool execute function
        :param kwargs: dict, keyword arguments to pass to the tool execute function
        :return: DccTool or None, executed tool instance
        """

        tool_inst._launch(*args, **kwargs)
        tp.logger.debug('Execution time: {}'.format(tool_inst.stats.execution_time))

        return tool_inst

    def get_registered_tools(self, package_name=None):
        """
        Returns all registered tools
        :param package_name: str or None
        :return: list
        """

        if not self._plugins:
            return None

        if package_name and package_name not in self._plugins:
            tp.logger.error(
                'Impossible to retrieve data from instance: package "{}" not registered!'.format(package_name))
            return None

        if package_name:
            return self._plugins[package_name]
        else:
            all_tools = dict()
            for package_name, package_data in self._plugins.items():
                for tool_name, tool_data in package_data.items():
                    all_tools[tool_name] = tool_data

            return all_tools

    def get_package_tools(self, package_name):
        """
        Returns all tools of the given package
        :param package_name: str
        :return: list
        """

        if not package_name:
            tp.logger.error('Impossible to retrieve data from plugin with undefined package!')
            return None

        if package_name not in self._plugins:
            tp.logger.error(
                'Impossible to retrieve data from instance: package "{}" not registered!'.format(package_name))
            return None

        package_tools = self.get_registered_tools(package_name=package_name)

        return package_tools

    def get_tool_by_plugin_instance(self, plugin, package_name=None):
        """
        Returns tool instance by given plugin instance
        :param plugin:
        :return:
        """

        if not package_name:
            package_name = plugin.PACKAGE
        if not package_name:
            tp.logger.error('Impossible to retrieve data from plugin with undefined package!')
            return None

        if package_name not in self._plugins:
            tp.logger.error(
                'Impossible to retrieve data from instance: package "{}" not registered!'.format(package_name))
            return None

        if hasattr(plugin, 'ID'):
            return self.get_tool_by_id(tool_id=plugin.ID, package_name=plugin.PACKAGE)

        return None

    def get_tool_by_id(self, tool_id, package_name=None, do_reload=False, debug=False, *args, **kwargs):
        """
        Launches tool of a specific package by its ID
        :param tool_id: str, tool ID
        :param package_name: str, str
        :param do_reload: bool
        :param debug: bool
        :param args: tuple, arguments to pass to the tool execute function
        :param kwargs: dict, keyword arguments to pas to the tool execute function
        :return: DccTool or None, executed tool instance
        """

        from tpDcc.libs.qt.core import settings

        if not package_name:
            package_name = tool_id.replace('.', '-').split('-')[0]

        if package_name not in self._plugins:
            tp.logger.warning('Impossible to load tool by id: package "{}" is not registered!'.format(package_name))
            return None

        if tool_id in self._plugins[package_name]:
            tool_inst = self._plugins[package_name][tool_id].get('tool_instance', None)
            if tool_inst:
                if do_reload:
                    self.reload_plugin(tool_id, debug=debug)
                return tool_inst

        tool_to_run = None

        for plugin_id in self._plugins[package_name].keys():
            tool_path = self._plugins[package_name][plugin_id]['plugin_package']
            sec_path = tool_path.replace('.', '-')
            if sec_path == tool_path or sec_path == tool_id:
                tool_to_run = tool_id
                break
            else:
                tool_name = tool_path.split('.')[-1]
                if tool_name == tool_path:
                    tool_to_run = tool_id
                    break

        if not tool_to_run or tool_to_run not in self._plugins[package_name]:
            tp.logger.warning('Tool "{}" is not registered!'.format(tool_id))
            return None

        pkg_loader = self._plugins[package_name][tool_to_run]['loader']
        tool_config = self._plugins[package_name][tool_to_run]['config']
        tool_fullname = self._plugins[package_name][tool_to_run]['loader'].fullname
        tool_version = self._plugins[package_name][tool_to_run]['version']
        dcc_loader = self._plugins[package_name][tool_to_run]['dcc_loader']
        dcc_config = self._plugins[package_name][tool_to_run]['dcc_config']

        # Initialize and reload tool modules if necessary
        tool_importer = ToolImporter(pkg_loader, debug=debug)

        if tool_config:
            import_order = ['{}.{}'.format(pkg_loader.fullname, mod) for mod in
                            tool_config.data.get('import_order', list())]
            skip_modules = ['{}.{}'.format(pkg_loader.fullname, mod) for mod in
                            tool_config.data.get('skip_modules', list())]
            tools_to_reload = tool_config.data.get('tools_to_reload', list())
            if tools_to_reload:
                for tool_to_reload in tools_to_reload:
                    self.reload_tool(tool_to_reload)
        else:
            import_order = list()
            skip_modules = list()
        tool_importer.import_packages(order=import_order, only_packages=False, skip_modules=skip_modules)
        if do_reload:
            tool_importer.reload_all()

        # Initialize and reload DCC tool implementation modules if necessary
        if dcc_loader:

            dcc_importer = ToolImporter(dcc_loader, debug=debug)
            dcc_import_order = ['{}.{}'.format(pkg_loader.fullname, mod) for mod in
                                dcc_config.data.get('import_order', list())]
            dcc_skip_modules = ['{}.{}'.format(pkg_loader.fullname, mod) for mod in
                                dcc_config.data.get('skip_modules', list())]
            tools_to_reload = dcc_config.data.get('tools_to_reload', list())
            if tools_to_reload:
                for tool_to_reload in tools_to_reload:
                    self.reload_tool(tool_to_reload)
            dcc_importer.import_packages(order=dcc_import_order, only_packages=False, skip_modules=dcc_skip_modules)
            if do_reload:
                dcc_importer.reload_all()

        tool_found = None
        for sub_module in loader.walk_packages([self._plugins[package_name][tool_to_run]['plugin_package_path']]):
            importer, sub_module_name, _ = sub_module
            mod = importer.find_module(sub_module_name).load_module(sub_module_name)
            for cname, obj in inspect.getmembers(mod, inspect.isclass):
                if issubclass(obj, tool.DccTool):
                    obj.FILE_NAME = pkg_loader.filename
                    obj.FULL_NAME = pkg_loader.fullname
                    tool_found = obj
                    break
            if tool_found:
                break

        if not tool_found:
            tp.logger.error("Error while launching tool: {}".format(tool_fullname))
            return None

        # if dcc_loader:
        #     tool_config = dcc_config

        settings_path = appdirs.user_data_dir(appname=tool_id)
        settings_file = path_utils.clean_path(os.path.expandvars(os.path.join(settings_path, 'settings.cfg')))
        tool_settings = settings.QtSettings(filename=settings_file)
        if not tool_settings.has_setting('theme'):
            tool_settings.set('theme', 'default')
        tool_settings.setFallbacksEnabled(False)

        tool_inst = tool_found(self, config=tool_config, settings=tool_settings, *args, **kwargs)
        tool_inst.ID = tool_id
        tool_inst.VERSION = tool_version
        tool_inst.AUTHOR = tool_inst.config_dict().get('creator', None)
        tool_inst.PACKAGE = package_name

        self._plugins[package_name][plugin_id]['tool_instance'] = tool_inst

        return tool_inst

    def launch_tool_by_id(self, tool_id, package_name=None, do_reload=False, debug=False, *args, **kwargs):
        """
        Launches tool of a specific package by its ID
        :param tool_id: str, tool ID
        :param package_name: str, str
        :param do_reload: str, bool
        :param debug: str, bool
        :param args: tuple, arguments to pass to the tool execute function
        :param kwargs: dict, keyword arguments to pas to the tool execute function
        :return: DccTool or None, executed tool instance
        """

        parent = tp.Dcc.get_main_window()
        if parent:
            for child in parent.children():
                if child.objectName() == tool_id:
                    child.close()
                    child.setParent(None)
                    child.deleteLater()

        tool_inst = self.get_tool_by_id(
            tool_id=tool_id, package_name=package_name, do_reload=do_reload, debug=debug, *args, **kwargs)
        if not tool_inst:
            return None

        self.launch_tool(tool_inst, *args, **kwargs)

        return tool_inst

    def reload_tool(self, tool_id):
        """
        Reloads tool with given id
        :param tool_id: str
        """

        all_tools = self.get_registered_tools()
        if not all_tools:
            return

        tool_ids = all_tools.keys()
        if tool_id not in tool_ids:
            return

        self.reload_plugin(tool_id)

    def reload_tools(self):
        """
        Reload all available tools
        :return:
        """

        all_tools = self.get_registered_tools()
        if not all_tools:
            return
        tool_ids = all_tools.keys()
        for tool_id in tool_ids:
            self.reload_plugin(tool_id)

    # ============================================================================================================
    # CONFIGS
    # ============================================================================================================

    def get_tool_config(self, tool_id, package_name=None):
        """
        Returns config applied to given tool
        :param tool_id: str
        :param package_name: str
        :return: Theme
        """

        if not package_name:
            package_name = tool_id.replace('.', '-').split('-')[0]

        if package_name not in self._plugins:
            tp.logger.warning(
                'Impossible to retrieve tool config for "{}" in package "{}"! Package not registered.'.format(
                    tool_id, package_name))
            return None

        if tool_id not in self._plugins[package_name]:
            tp.logger.warning(
                'Impossible to retrieve tool config for "{}" in package "{}"! Tool not found'.format(
                    tool_id, package_name))
            return None

        config = self._plugins[package_name][tool_id].get('config', None)

        return config

    # ============================================================================================================
    # THEMES
    # ============================================================================================================

    def get_tool_theme(self, tool_id, package_name=None):
        """
        Returns theme applied to given tool
        :param tool_id: str
        :param package_name: str
        :return: Theme
        """

        found_tool = self.get_tool_by_id(tool_id, package_name=package_name)
        if not found_tool:
            return None

        theme_name = found_tool.settings.get('theme', 'default')
        return tp.ResourcesMgr().theme(theme_name)


@decorators.Singleton
class ToolsManagerSingleton(ToolsManager, object):
    """
    Singleton class that holds preferences manager instance
    """

    def __init__(self, ):
        ToolsManager.__init__(self)


register.register_class('ToolsMgr', ToolsManagerSingleton)
