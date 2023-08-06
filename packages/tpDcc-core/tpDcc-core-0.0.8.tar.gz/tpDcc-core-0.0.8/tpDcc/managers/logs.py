#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains implementation to handle DCC logs themes
"""

import os
import logging

import tpDcc
from tpDcc import register
from tpDcc.libs.python import decorators


class LogsManager(object):
    def __init__(self):
        super(LogsManager, self).__init__()

    def get_logger(self, tool_id=None):
        """
        Returns logger associated with given tool
        :param tool_id: str
        :return:
        """

        if not tool_id:
            return logging.getLogger('tpDcc')

        tool_data = tpDcc.ToolsMgr().get_plugin_data_from_id(tool_id)
        if not tool_data:
            return logging.getLogger('tpDcc')

        logging_file = tool_data.get('logging_file', None)
        if not logging_file:
            return logging.getLogger('tpDcc')

        logging.config.fileConfig(logging_file, disable_existing_loggers=False)
        # tool_logger_level_env = '{}_LOG_LEVEL'.format(pkg_loader.fullname.replace('.', '_').upper())
        return logging.getLogger(tool_id)


@decorators.Singleton
class LogsManagerSingleton(LogsManager, object):
    """
    Singleton class that holds logs manager instance
    """

    def __init__(self):
        LogsManager.__init__(self)


register.register_class('LogsMgr', LogsManagerSingleton)
