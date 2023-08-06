#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains implementation for DCC menus
"""

from functools import partial

import tpDcc as tp
import tpDcc.register
from tpDcc.libs.python import decorators
from tpDcc.libs.qt.core import qtutils, menu


class MenusManager(object):
    def __init__(self, parent=None):
        super(MenusManager, self).__init__()

        self._parent = parent or tp.Dcc.get_main_window()
        self._menus = dict()
        self._menu_names = dict()
        self._object_menu_names = dict()

        # ============================================================================================================
        # MENUS
        # ============================================================================================================

    def get_menu(self, menu_name, package_name=None):
        """
        Returns menu object if exists
        :param package_name: str
        :param menu_name: str
        :return: QMenu
        """

        for pkg_name, menu in self._menus.items():
            if package_name and pkg_name != package_name:
                continue
            # if menu_name == self._menu.objectName():
            #     return self._menus[menu_name]

        return self._menus.get(package_name, dict()).get(menu_name, None)

    def create_main_menu(self, package_name, force_creation=True):
        """
        Creates main menu for given package
        :param package_name: str
        :param force_creation: bool
        """

        if not package_name:
            return None

        if package_name in self._menus and self._menus.get(package_name, None):
            if not force_creation:
                return self._menus[package_name]
            self.remove_previous_menus(package_name=package_name)

        object_menu_name = self._object_menu_names[
            package_name] if package_name in self._object_menu_names else '{}_Menu'.format(package_name)
        menu_name = self._menu_names[package_name] if package_name in self._menu_names else package_name

        parent_menu_bar = qtutils.get_window_menu_bar(tp.Dcc.get_main_window())
        if not parent_menu_bar:
            tp.logger.warning(
                'Impossible to create Tools main menu for "{}" because not found menu bar to attach menu to!'.format(
                    package_name))
            return None
        main_menu = menu.SearchableMenu(objectName=object_menu_name, title=menu_name, parent=parent_menu_bar)
        parent_menu_bar.addMenu(main_menu)
        main_menu.setObjectName(object_menu_name)
        main_menu.setTearOffEnabled(True)

        return main_menu

    def create_menus(self, package_name):
        """
        Loops through all loaded plugins and creates a menu/action for each one.
        Function that should be implemented in specific DCC Menu Managers to create proper menu
        """

        self.remove_previous_menus(package_name=package_name)
        self.create_main_menu(package_name=package_name)

    def get_tools_menus(self):
        """
        Returns dictionary with the menu info for all the registered tools
        :return: dict
        """

        tool_menus = dict()

        for package_name, package_data in tp.ToolsMgr().plugins.items():
            for tool_name, tool_data in package_data.items():
                tool_config = tool_data['config']
                if not tool_config:
                    continue
                menu_data = tool_config.data.get('menu', None)
                if not menu_data:
                    continue
                if package_name not in tool_menus:
                    tool_menus[package_name] = dict()

                tool_menus[package_name][tool_name] = menu_data

        return tool_menus

    def remove_previous_menus(self, package_name=None):
        """
        Removes any DCC tool menu from DCC by iterating through the children of the main window looking for any widget
        with proper objectName
        """

        tp.logger.info('Closing menus for: {}'.format(package_name))

        deleted_menus = list()

        object_menu_name = self._object_menu_names[
            package_name] if package_name in self._object_menu_names else '{}_Menu'.format(package_name)

        if not self._parent:
            return

        for child_widget in self._parent.menuBar().children():
            child_name = child_widget.objectName()
            for pkg_name, menu in self._menus.items():
                if package_name and pkg_name != package_name:
                    continue
                if child_name == menu.objectName():
                    child_widget.deleteLater()
                    self._menus.pop(package_name)
                    deleted_menus.append(child_name)
            if child_name == object_menu_name and child_name not in deleted_menus:
                child_widget.deleteLater()

    def _menu_creator(self, parent_menu, data, package_name, dev=False):
        """
        Internal function that manages the creation of the menus
        :param parent_menu: QWidget
        :param data:
        :param package_name: str
        :param dev: bool
        :return:
        """

        if 'label' not in data:
            return
        menu = self.get_menu(data['label'], package_name=package_name)
        if menu is None and data.get('type', '') == 'menu':
            only_dev = data.get('only_dev', False)
            if only_dev and dev:
                return
            menu = parent_menu.addMenu(data['label'])
            menu.setObjectName(data['label'])
            menu.setTearOffEnabled(True)
            if package_name not in self._menus:
                self._menus[package_name] = dict()
            self._menus[package_name][data['label']] = menu

        if 'children' not in data:
            return

        for i in iter(data['children']):
            action_type = i.get('type', 'command')
            only_dev = i.get('only_dev', False)
            if only_dev and not self._project.is_dev():
                continue
            if action_type == 'separator':
                self._menu.addSeparator()
                continue
            elif action_type == 'group':
                sep = self._menu.addSeparator()
                sep.setText(i['label'])
                continue
            elif action_type == 'menu':
                self._menu_creator(menu, i, package_name=package_name, dev=dev)
                continue
            self._add_action(i, menu)

    def _add_action(self, item_info, parent):

        item_type = item_info.get('type', 'tool')
        if item_type == 'tool':
            self._add_tool_action(item_info, parent)
        else:
            self._add_menu_item_action(item_info, parent)

    def _add_menu_item_action(self, item_info, parent):
        menu_item_id = item_info.get('id', None)

        menu_item_ui = item_info.get('ui', None)
        if not menu_item_ui:
            tp.logger.warning('Menu Item "{}" has not a ui specified!. Skipping ...'.format(menu_item_id))
            return
        menu_item_command = item_info.get('command', None)
        if not menu_item_command:
            tp.logger.warning(
                'Menu Item "{}" does not defines a command to execute. Skipping ...'.format(menu_item_id))
            return
        menu_item_language = item_info.get('language', 'python')

        menu_item_icon_name = menu_item_ui.get('icon', 'artella')
        menu_item_icon = tp.ResourcesMgr().icon(menu_item_icon_name)
        menu_item_label = menu_item_ui.get('label', 'No_label')
        is_checkable = menu_item_ui.get('is_checkable', False)
        is_checked = menu_item_ui.get('is_checked', False)
        tagged_action = menu.SearchableTaggedAction(label=menu_item_label, icon=menu_item_icon, parent=self._parent)
        if is_checkable:
            tagged_action.setCheckable(is_checkable)
            tagged_action.setChecked(is_checked)
            tagged_action.connect(partial(self._launch_command, menu_item_command, menu_item_language))
            tagged_action.toggled.connect(partial(self._launch_command, menu_item_command, menu_item_language))
            if menu_item_ui.get('load_on_startup', False):
                self._launch_command(menu_item_command, menu_item_language, is_checked)
        else:
            tagged_action.triggered.connect(partial(self._launch_command, menu_item_command, menu_item_language))
            if menu_item_ui.get('load_on_startup', False):
                self._launch_command(menu_item_command, menu_item_language)

        tagged_action.tags = set(item_info.get('tags', []))

        parent.addAction(tagged_action)

    def _add_tool_action(self, item_info, parent):
        tool_id = item_info.get('id', None)
        tool_type = item_info.get('type', 'tool')

        tool_data = tp.ToolsMgr().get_plugin_data_from_id(tool_id)
        if tool_data is None:
            tp.logger.warning('Menu : Failed to find Tool: {}, type {}'.format(tool_id, tool_type))
            return

        tool_icon = None
        tool_icon_name = tool_data['config'].data.get('icon', None)
        if tool_icon_name:
            tool_icon = tp.ResourcesMgr().icon(tool_icon_name)
        tool_menu_ui_data = tool_data['config'].data.get('menu_ui', {})
        label = tool_menu_ui_data.get('label', 'No_label')
        tagged_action = menu.SearchableTaggedAction(label=label, icon=tool_icon, parent=self._parent)
        is_checkable = tool_menu_ui_data.get('is_checkable', False)
        is_checked = tool_menu_ui_data.get('is_checked', False)
        if is_checkable:
            tagged_action.setCheckable(is_checkable)
            tagged_action.setChecked(is_checked)
            tagged_action.connect(partial(self._launch_tool, tool_data))
            tagged_action.toggled.connect(partial(self._launch_tool_by_id, tool_id))
        else:
            tagged_action.triggered.connect(partial(self._launch_tool_by_id, tool_id))

        icon = tool_menu_ui_data.get('icon', None)
        if icon:
            pass

        tagged_action.tags = set(tool_data['config'].data.get('tags', []))

        parent.addAction(tagged_action)

    def _launch_tool_by_id(self, tool_id, **kwargs):
        """
        Internal function that launch a tool by its ID
        :param tool_id: str
        :param kwargs: dict
        """

        do_reload = kwargs.get('do_reload', False)

        tpDcc.ToolsMgr().launch_tool_by_id(tool_id, do_reload=do_reload)

    def _launch_command(self, command, language='python', *args, **kwargs):
        """
        Internal function that launches the given command
        :param command: str
        :param args: list
        :param kwargs: dict
        """

        if language == 'python':
            exec(command)
        else:
            raise NotImplementedError('Commands of of language "{}" are not supported!'.format(language))


@decorators.Singleton
class MenusManagerSingleton(MenusManager, object):
    def __init__(self):
        MenusManager.__init__(self)


tpDcc.register.register_class('MenusMgr', MenusManagerSingleton)
