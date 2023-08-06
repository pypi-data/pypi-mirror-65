#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains classes to create plugins
"""

from __future__ import print_function, division, absolute_import

import os
import time
import inspect

import tpDcc as tp
from tpDcc.libs.python import importer, modules


class Plugin(object):
    """
    Base class for plugins
    """

    ID = ''
    VERSION = None
    PACKAGE = None

    def __init__(self, manager=None):
        self._manager = manager
        self._stats = PluginStats(self)

    @property
    def manager(self):
        return self._manager

    @property
    def stats(self):
        return self._stats


class PluginStats(object):
    def __init__(self, plugin):
        self._plugin = plugin
        self._id = self._plugin.ID
        self._start_time = 0.0
        self._end_time = 0.0
        self._execution_time = 0.0

        self._info = dict()

        self._init()

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        self._end_time = value

    @property
    def execution_time(self):
        return self._execution_time

    def _init(self):
        """
        Internal function that initializes info for the plugin and its environment
        """

        self._info.update({
            'name': self._plugin.__class__.__name__,
            'creator': self._plugin.creator,
            'module': self._plugin.__class__.__module__,
            'filepath': inspect.getfile(self._plugin.__class__),
            'id': self._id,
            'application': tp.Dcc.get_name()
        })

    def start(self):
        """
        Starts the execution of the plugin
        """

        self._start_time = time.time()

    def finish(self, trace=None):
        """
        Function that is called when plugin finishes its execution
        :param tb: str or None
        """

        self._end_time = time.time()
        self._execution_time = self._end_time - self._start_time
        self._info['executionTime'] = self._execution_time
        self._info['lastUsed'] = self._end_time
        if trace:
            self._info['traceback'] = trace


class PluginImporter(importer.Importer, object):
    def __init__(self, plugin_package, debug=False):

        self.plugin_path = plugin_package.filename

        super(PluginImporter, self).__init__(module_name=plugin_package.fullname, debug=debug)

    def get_module_path(self):
        """
        Returns path where module is located
        :return: str
        """

        return self.plugin_path


class PluginsManager(object):

    INTERFACE = Plugin
    VARIABLE_NAME = 'ID'

    def __init__(self):
        self._plugins = dict()
        self._base_paths = list()

    @property
    def plugins(self):
        return self._plugins

    def register_plugin(self, class_obj, package_name):
        """
        Registers a plugin instance to the manager
        :param class_obj:
        :param package_name: str
        :return: Plugin
        """

        if not issubclass(class_obj, self.INTERFACE):
            return None

        plugin_id = getattr(
            class_obj, self.VARIABLE_NAME) if hasattr(class_obj, self.VARIABLE_NAME) else class_obj.__name__

        if package_name not in self._plugins:
            self._plugins[package_name] = dict()
        else:
            if plugin_id in self._plugins[package_name]:
                return None

        self._plugins[package_name][plugin_id] = class_obj

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

    def get_plugin_data_from_name(self, plugin_name, as_dict=False, package_name=None):
        """
        Returns registered plugin from its name
        :param plugin_name: str
        :return:
        """

        if not plugin_name:
            return None

        if package_name and package_name not in self._plugins:
            tp.logger.error('Impossible to retrieve data from name: package "{}" not registered!'.format(package_name))
            return None

        for plugin_id, plugin_data in self._plugins[package_name].items():
            current_name = plugin_data.get('name', None)
            if current_name == plugin_name:
                if as_dict:
                    return {
                        plugin_id: self._plugins[package_name][plugin_id]
                    }
                else:
                    return self._plugins[package_name][plugin_id]

        return None

    def get_plugin_data_from_plugin_instance(self, plugin, as_dict=False, package_name=None):
        """
        Returns registered plugin data from a plugin object
        :return: dict
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
            return self._plugins[package_name].get(plugin.ID, None)

        return None

    def register_plugin_by_package(self, module_path, package_name, do_reload=False):
        """
        Registers a module by searching all class members of the package. This operation can be extensive.
        :param module_path: str
        :param package_name: str
        :param do_reload: bool
        :return:
        """

        for sub_module in modules.iterate_modules(module_path):
            file_name = os.path.splitext(os.path.basename(sub_module))[0]
            if file_name.startswith('__') or sub_module.endswith('.pyc'):
                continue
            module_path = modules.convert_to_dotted_path(os.path.normpath(sub_module))
            try:
                sub_module_obj = modules.import_module(module_path)
                if do_reload and sub_module_obj:
                    reload(sub_module_obj)
            except Exception as exc:
                tp.logger.error('Error while importing module: {} | {}'.format(module_path, exc))
                continue
            if not sub_module_obj:
                return
            for member in modules.iterate_module_members(sub_module_obj, predicate=inspect.isclass):
                self.register_plugin(member[1], package_name=package_name)

    def register_plugin_by_module(self, module, package_name):
        """
        Registers a module by searching all class members of the module and registers any class that is an instance of
        the plugin class
        :param module: str, module path to register separated by . (for example, tpDcc.tools.renamer.widgets)
        :param package_name: str
        """

        if inspect.ismodule(module):
            for member in modules.iterate_module_members(module, predicate=inspect.isclass):
                self.register_plugin(member[1], package_name=package_name)

    def register_path(self, module_path, package_name, do_reload=False):
        imported_module = None
        if os.path.isdir(module_path):
            self.register_plugin_by_package(module_path, package_name, do_reload=do_reload)
            return None
        elif os.path.isfile(module_path):
            try:
                imported_module = modules.import_module(modules.convert_to_dotted_path(os.path.normpath(module_path)))
            except Exception as exc:
                tp.logger.error('Failed to import Plugin module: {} | {}!'.format(module_path, exc), exc_info=True)
                return None
        elif modules.is_dotted_module_path(module_path):
            try:
                imported_module = modules.import_module(os.path.normpath(module_path))
            except Exception as exc:
                tp.logger.error('Failed to import Plugin module: {} | {}!'.format(module_path, exc), exc_info=True)
                return None
        if imported_module:
            self.register_plugin_by_module(imported_module)

        return imported_module

    def register_paths(self, paths_to_register, package_name, do_reload=False):
        self._base_paths.extend(paths_to_register)
        visited = set()
        for path_to_register in paths_to_register:
            if not path_to_register:
                continue
            if os.path.isfile(path_to_register):
                base_name = os.extsep.join(path_to_register.split(os.extsep)[:-1])
            else:
                base_name = path_to_register
            if base_name in visited:
                continue
            visited.add(base_name)
            self.register_path(path_to_register, package_name=package_name, do_reload=do_reload)
