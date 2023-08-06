#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains implementation for preferences manager
"""

from __future__ import print_function, division, absolute_import

import os

import metayaml

import tpDcc as tp
from tpDcc import register
from tpDcc.core import config
from tpDcc.libs.python import decorators, folder


class ConfigsManager(object):

    EXTENSION = 'yml'

    def __init__(self):
        self._package_configs = dict()

    # ============================================================================================================
    # BASE
    # ============================================================================================================

    def register_package_path(self, package_name, module_name, config_path, environment='development'):
        """
        Registers configurations path for given package
        :param package_name: str, name of the package configuration files belong to
        :param module_name: str, name of the module this configuration belongs to
        :param config_path: str, path where configuration file is located
        """

        if not config_path or not os.path.isdir(config_path):
            tp.logger.warning(
                'Configuration Path "{}" for package "{}" does not exists!'.format(config_path, package_name))
            return

        if environment:
            config_path = os.path.join(config_path, environment.lower())
            if not os.path.isdir(config_path):
                tp.logger.warning(
                    'Configuration Folder for environment "{}" and package "{}" does not exists "{}"'.format(
                        environment, package_name, config_path))
                return

        dcc_name = tp.Dcc.get_name()
        dcc_version = tp.Dcc.get_version_name()

        base_config = os.path.join(config_path, module_name)
        dcc_config_path = os.path.join(config_path, dcc_name, module_name)
        dcc_version_config_path = os.path.join(config_path, dcc_name, dcc_version, module_name)

        if package_name not in self._package_configs:
            self._package_configs[package_name] = dict()
        if module_name not in self._package_configs[package_name]:
            self._package_configs[package_name][module_name] = dict()

        config_extension = self.EXTENSION
        if not config_extension.startswith('.'):
            config_extension = '.{}'.format(config_extension)

        self._package_configs[package_name][module_name][environment] = {
            'base': '{}{}'.format(base_config, config_extension),
            'dcc': '{}{}'.format(dcc_config_path, config_extension),
            'dcc_version': '{}{}'.format(dcc_version_config_path, config_extension)
        }

    def register_package_configs(self, package_name, config_path):
        """
        Tries to find and registers all configuration paths of given path and in the given path
        :param package_name: str
        :param config_path: str
        """

        config_extension = self.EXTENSION
        if not config_extension.startswith('.'):
            config_extension = '.{}'.format(config_extension)

        if not config_path or not os.path.isdir(config_path):
            return

        for environment in ['development', 'production']:
            config_files = folder.get_files(
                config_path, full_path=False, recursive=True, pattern='*{}'.format(config_extension))
            if not config_files:
                continue
            module_names = [os.path.splitext(file_path)[0] for file_path in config_files]
            for module_name in module_names:
                self.register_package_path(
                    package_name=package_name, config_path=config_path,
                    module_name=module_name, environment=environment)

    def get_config(self, config_name, package_name=None, root_package_name=None,
                   environment=None, config_dict=None, parser_class=None, extra_data=None):
        """
        Returns configuration
        :param package_name:
        :param root_package_name:
        :param config_name:
        :param environment:
        :param config_dict:
        :return:
        """

        if config_dict is None:
            config_dict = dict()
        if extra_data is None:
            extra_data = dict()

        if not parser_class:
            parser_class = config.YAMLConfigurationParser

        if not package_name:
            package_name = config_name.replace('.', '-').split('-')[0]

        config_data = self._get_config_data(
            package_name=package_name, config_name=config_name,
            config_dict=config_dict, root_package_name=root_package_name, environment=environment)
        if config_data is None:
            config_data = dict()

        parsed_data = parser_class(config_data).parse()
        extra_data.update(parsed_data)
        new_config = config.DccConfig(config_name=config_name, environment=environment, data=extra_data)

        return new_config

    def _get_all_package_configs(self, package_name, root_package_name=None, environment=None, skip_non_existent=True):
        """
        Internal function that returns a list with all configuration files of given package
        :param package_name: str
        :param root_package_name: str
        :param environment: str
        :param skip_non_existent: bool
        :return: list(dict)
        """

        module_paths = dict()

        if root_package_name and root_package_name not in self._package_configs:
            tp.logger.warning(
                'Impossible to retrieve package configs because root package: "{}" does not exist!'.format(
                    root_package_name))
            return module_paths

        if package_name not in self._package_configs:
            tp.logger.warning(
                'Impossible to retrieve package configs because package: "{}" does not exist!'.format(
                    root_package_name))
            return module_paths

        packages_to_loop = list()
        if root_package_name:
            packages_to_loop = [root_package_name]
        packages_to_loop.append(package_name)

        for package_name in packages_to_loop:
            for module_name, env_dicts in self._package_configs[package_name].items():
                for env_name, module_dict in env_dicts.items():
                    base_path = module_dict.get('base', None)
                    dcc_path = module_dict.get('dcc', None)
                    dcc_version_path = module_dict.get('dcc_version', None)
                    found_paths = list()

                    if environment and environment.lower() != env_name.lower():
                        continue

                    if skip_non_existent:
                        if base_path and os.path.isfile(base_path):
                            found_paths.append(base_path)
                        if dcc_path and os.path.isfile(dcc_path):
                            found_paths.append(dcc_path)
                        if dcc_version_path and os.path.isfile(dcc_version_path):
                            found_paths.append(dcc_version_path)
                    else:
                        if base_path:
                            found_paths.append(base_path)
                        if dcc_path:
                            found_paths.append(dcc_path)
                        if dcc_version_path:
                            found_paths.append(dcc_version_path)
                    if not found_paths:
                        continue
                    if module_name not in module_paths:
                        module_paths[module_name] = list()

                    module_paths[module_name].extend(found_paths)

        return module_paths

    def _get_config_data(self, package_name, config_name, config_dict, root_package_name=None, environment=None):
        """
        Intgernal function that returns data of the given configuration
        :param package_name: str
        :param config_name: str
        :param config_dict: dict
        :param root_package_name: str
        :param environment: str
        :return:
        """

        if not package_name:
            tp.logger.error('Impossible to find configuration if package is not given!')
            return None
        if not config_name:
            tp.logger.error('Impossible to to find configuration if configuration name is not given!')
            return None

        if package_name not in self._package_configs:
            tp.logger.error('No configurations find for package "{}"'.format(package_name))
            return None

        config_extension = self.EXTENSION
        if not config_extension.startswith('.'):
            config_extension = '.{}'.format(config_extension)

        valid_package_configs = self._get_all_package_configs(
            package_name=package_name, root_package_name=root_package_name, environment=environment)
        if not valid_package_configs or config_name not in valid_package_configs:
            # tp.logger.info(
            #     'Impossible to load configuration "{}" for package "{}" because it does not exists in '
            #     'configuration folders!'.format(config_name, package_name))
            return

        module_configs = valid_package_configs[config_name]

        # We read the last configuration found: dcc_version > dcc > base
        config_path = module_configs[-1]
        config_data = metayaml.read(module_configs, config_dict)
        if not config_data:
            raise RuntimeError('Configuration file "{}" is empty!'.format(config_path))

        # We store path where configuration file is located in disk
        if 'config' in config_data and 'path' in config_data['config']:
            raise RuntimeError('Configuration file cannot contains section with path attribute! {}'.format(
                self, config_path))
        if 'config' in config_data:
            config_data['config']['path'] = config_path
        else:
            config_data['config'] = {'path': config_path}

        return config_data


@decorators.Singleton
class ConfigsManagerSingleton(ConfigsManager, object):
    """
    Singleton class that holds preferences manager instance
    """

    def __init__(self):
        ConfigsManager.__init__(self)


register.register_class('ConfigsMgr', ConfigsManagerSingleton)
