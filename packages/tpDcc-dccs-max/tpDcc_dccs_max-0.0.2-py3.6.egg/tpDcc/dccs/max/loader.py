#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for tpDcc.dccs.max
"""

from __future__ import print_function, division, absolute_import

import os
import inspect
import logging

from tpDcc.libs.python import importer


class tpMaxLib(importer.Importer, object):
    def __init__(self, *args, **kwargs):
        super(tpMaxLib, self).__init__(module_name='tpDcc.dccs.max', *args, **kwargs)

    def get_module_path(self):
        """
        Returns path where tpDcc.dccs.maya module is stored
        :return: str
        """

        try:
            mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
        except Exception:
            try:
                mod_dir = os.path.dirname(__file__)
            except Exception:
                try:
                    import tpDcc.dccs.max
                    mod_dir = tpDcc.dccs.max.__path__[0]
                except Exception:
                    return None

        return mod_dir


def create_logger():
    """
    Returns logger of current module
    """

    logging.config.fileConfig(get_logging_config(), disable_existing_loggers=False)
    create_logger_directory()
    logger = logging.getLogger('tpDcc-dccs-max')

    return logger


def create_logger_directory():
    """
    Creates artellapipe logger directory
    """

    logger_path = os.path.normpath(os.path.join(os.path.expanduser('~'), 'tpDcc', 'logs'))
    if not os.path.isdir(logger_path):
        os.makedirs(logger_path)


def get_logging_config():
    """
    Returns logging configuration file path
    :return: str
    """

    create_logger_directory()

    return os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))


def init_dcc(do_reload=False):
    """
    Initializes module
    :param do_reload: bool, Whether to reload modules or not
    """

    from tpDcc.dccs.max import register
    from tpDcc.libs.qt.core import resource as resource_utils

    class tpMaxLibResource(resource_utils.Resource, object):
        RESOURCES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')

    logger = create_logger()

    max_importer = importer.init_importer(importer_class=tpMaxLib, do_reload=False)

    register.register_class('resource', tpMaxLibResource)
    register.register_class('logger', logger)

    max_importer.import_modules(skip_modules=['tpDcc.dccs.max.ui'])
    max_importer.import_packages(only_packages=True, skip_modules=['tpDcc.dccs.max.ui'])
    if do_reload:
        max_importer.reload_all()


def init_ui(do_reload=False):
    max_importer = importer.init_importer(importer_class=tpMaxLib, do_reload=False)

    max_importer.import_modules(skip_modules=['tpDcc.dccs.max.core'])
    max_importer.import_packages(only_packages=True, skip_modules=['tpDcc.dccs.max.core'])
    if do_reload:
        max_importer.reload_all()
