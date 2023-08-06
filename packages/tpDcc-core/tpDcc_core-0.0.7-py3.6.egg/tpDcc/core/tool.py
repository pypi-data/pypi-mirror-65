#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains classes to create editor tools inside Qt apps
"""

from __future__ import print_function, division, absolute_import

import os
import sys
import copy
import time
import traceback
from functools import partial

from Qt.QtCore import *

import tpDcc as tp
from tpDcc.core import plugin
from tpDcc.libs.python import decorators


class DccTool(plugin.Plugin, object):
    """
    Base class used by all editor tools
    """

    FILE_NAME = ''
    FULL_NAME = ''

    def __init__(self, manager, config=None, settings=None, *args, **kwargs):
        super(DccTool, self).__init__(manager=manager)

        self._tool = list()
        self._config = config
        self._bootstrap = list()
        self._attacher = None
        self._settings = settings

    @property
    def config(self):
        return self._config

    @property
    def settings(self):
        return self._settings

    @property
    def attacher(self):
        return self._attacher

    @decorators.abstractmethod
    def creator(self):
        """
        Creator function of the tool
        """

        pass

    @decorators.abstractmethod
    def launch(self, *args, **kwargs):
        """
        Function that launches the tool
        """

        pass

    @staticmethod
    def icon():
        """
        Returns the icon of the tool
        :return: QIcon or None
        """

        return None

    @classmethod
    def config_dict(cls, file_name=None):
        """
        Returns internal tool configuration dictionary
        :return: dict
        """

        file_name = file_name or ''

        return {
            'name': 'DccTool',
            'id': 'tpDcc-tools-tool',
            'supported_dccs': [],
            'creator': 'Tomas Poveda',
            'icon': 'tpdcc',
            'tooltip': '',
            'help_url': 'www.tomipoveda.com',
            'tags': ['tpDcc', 'dcc', 'tool'],
            'logger_dir': os.path.join(os.path.expanduser('~'), 'tpDcc', 'logs', 'tools'),
            'logger_level': 'INFO',
            'resources_path': os.path.join(file_name, 'resources'),
            'logging_file': os.path.join(file_name, '__logging__.ini'),
            'is_checkable': False,
            'is_checked': False,
            'frameless': {
                'enabled': True,
                'force': False
            },
            'dock': {
                'dockable': True,
                'tabToControl': ('AttributeEditor', -1),
                'floating': False,
                'multiple_tools': False
            },
            'menu_ui': {
                'label': 'tpDcc',
                'load_on_startup': False,
                'color': '',
                'background_color': ''
            },
            'menu': [
                {
                    'type': 'menu',
                    'children': [
                        {
                            'id': 'tpDcc-tools-tool',
                            'type': 'tool'
                        }
                    ]
                }
            ],
            'shelf': [
                {
                    'name': 'tpDcc',
                    'children': [
                        {
                            'id': 'tpDcc-tools-tool',
                            'display_label': False,
                            'type': 'tool'
                        }
                    ]
                }
            ]
        }

    def unique_name(self):
        """
        Returns unique name of the tool
        When a tool is not singleton, we need to store separate data for each instance.
        We use unique identifier for that
        :return: str
        """

        return '{}::{}'.format(self.NAME, str(self.ID))

    def frameless_window_toggle(self):
        """
        Returns current framelessWindowToggle plugin
        :return:
        """

        frameless_toggle = tp.ToolsMgr().get_tool_by_id('tpDcc-tools-frameless_toggle')
        if not frameless_toggle:
            return False

        return frameless_toggle.state

    def launch_frameless(self, *args, **kwargs):
        """
        Laucnhes the tool and applies frameless functionality to it
        :param args: tuple, dictionary of arguments to launch the tool
        :param kwargs: dict
        :return: dict
        """

        launch_frameless = kwargs.get('launch_frameless', None)
        default_frameless = self.frameless_window_toggle()
        frameless_active = launch_frameless if launch_frameless is not None else default_frameless

        tool = self.run_tool(frameless_active, kwargs)

        ret = {'tool': tool, 'bootstrap': None}
        if hasattr(tool, 'closed'):
            self._settings.set('dockable', not frameless_active)
            self._tool.append(ret)
            tool.closed.connect(partial(self._on_tool_closed, ret))

        return ret

    def run_tool(self, frameless_active=True, tool_kwargs=None, attacher_class=None):
        """
        Function that launches current tool
        :param frameless_active: bool, Whether the tool will be launch in frameless mode or not
        :param tool_kwargs: dict, dictionary of arguments to launch tool with
        :return:
        """

        tool_config_dict = self.config_dict()
        tool_name = tool_config_dict.get('name', None)
        tool_id = tool_config_dict.get('id', None)
        if not tool_name or not tool_id:
            tp.logger.warning('Impossible to run tool "{}" with id: "{}"'.format(tool_name, tool_id))
            return None

        toolset_class = tp.ToolsetsMgr().toolset(tool_id)
        if not toolset_class:
            tp.logger.warning('Impossible to run tool! No toolset found with id: "{}"'.format(tool_id))
            return None
        toolset_data_copy = copy.deepcopy(self._config.data)
        toolset_data_copy.update(toolset_class.CONFIG.data)
        toolset_class.CONFIG.data = toolset_data_copy

        if tool_kwargs is None:
            tool_kwargs = dict()

        tool_kwargs['collapsable'] = False
        tool_kwargs['show_item_icon'] = False
        toolset_inst = toolset_class(**tool_kwargs)
        toolset_inst.pre_content_setup()
        toolset_contents = toolset_inst.contents()
        for toolset_widget in toolset_contents:
            toolset_inst.add_stacked_widget(toolset_widget)
        toolset_inst.post_content_setup()
        toolset_inst.update_display_button()
        toolset_inst.expand()

        if not attacher_class:
            attacher_class = tp.Window

        self._attacher = attacher_class(
            id=tool_id, title=tool_name, config=toolset_class.CONFIG, settings=self.settings,
            show_on_initialize=True, frameless=frameless_active, dockable=True, toolset=toolset_inst)
        self._attacher.main_layout.setAlignment(Qt.AlignTop)
        toolset_inst.set_attacher(self._attacher)
        self._attacher.setWindowIcon(toolset_inst.get_icon())
        self._attacher.setWindowTitle('{} - {}'.format(self._attacher.windowTitle(), self.VERSION))
        self._attacher.show()

        return self._attacher

    def latest_tool(self):
        """
        Returns latest added tool
        """

        try:
            return self._tool[-1]['tool']
        except IndexError:
            return None

    def set_frameless(self, tool, frameless):
        pass

    def cleanup(self):
        """
        Internal function that clears tool data
        """

        try:
            self.cleanup()
        except RuntimeError:
            tp.logger.error('Failed to cleanup plugin: {}'.format(self.ID), exc_info=True)
        finally:
            try:
                for widget in self._bootstrap:
                    widget.close()
            except RuntimeError:
                tp.logger.error('Tool Widget already deleted: {}'.format(self._bootstrap), exc_info=True)
            except Exception:
                tp.logger.error('Failed to remove tool widget: {}'.format(self._bootstrap), exc_info=True)

    def _launch(self, *args, **kwargs):
        """
        Internal function for launching the tool
        :return:
        """

        self._stats.start_time = time.time()
        exc_type, exc_value, exc_tb = None, None, None
        try:
            kwargs['settings'] = self._settings
            kwargs['config'] = self._config
            tool_data = self.launch(*args, **kwargs)
            if tool_data and tool_data.get('tool') is not None:
                tool_data['tool'].ID = self.ID
                tool_data['tool'].PACKAGE = self.PACKAGE
                if self._settings.get('dockable', False):
                    uid = None
                    # TODO: Add option in settings to check if a tool can be opened multiple times or not
                    # TODO: Make this piece of code DCC agnostic
                    # if multiple_tools:
                    #     uid = "{0} [{1}]".format(self.uiData["label"], str(uuid.uuid4()))
                    ui_label = self._config.get('name', '')
                    ui_icon = self._config.get('icon', 'tpdcc')
                    from tpDcc.dccs.maya.ui import window
                    bootstrap_widget = window.BootStrapWidget(
                        tool_data['tool'], title=ui_label, icon=tp.ResourcesMgr().icon(ui_icon), uid=uid)
                    tool_data['bootstrap'] = bootstrap_widget
                    tool_data['bootstrap'].show(
                        retain=False, dockable=True, tabToControl=('AttributeEditor', -1), floating=False)
                    self._bootstrap.append(bootstrap_widget)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_tb)
            raise
        finally:
            tb = None
            if exc_type and exc_value and exc_tb:
                tb = traceback.format_exception(exc_type, exc_value, exc_tb)
            self._stats.finish(tb)

    def _on_tool_closed(self, tool):
        """
        Internal callback function that is called when a tool is closed
        :param tool:
        :return:
        """

        pass
