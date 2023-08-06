#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains DCC functionality for 3ds Max
"""

from __future__ import print_function, division, absolute_import

import MaxPlus

import tpDcc
from tpDcc import register
from tpDcc.abstract import dcc as abstract_dcc

from tpDcc.dccs.max.core import gui, helpers, scene, directory, viewport


class MaxDcc(abstract_dcc.AbstractDCC, object):

    @staticmethod
    def get_name():
        """
        Returns the name of the DCC
        :return: str
        """

        return tpDcc.Dccs.Max

    @staticmethod
    def get_extensions():
        """
        Returns supported extensions of the DCC
        :return: list(str)
        """

        return ['.max']

    @staticmethod
    def get_version():
        """
        Returns version of the DCC
        :return: int
        """

        return int(helpers.get_max_version())

    @staticmethod
    def get_version_name():
        """
        Returns version of the DCC
        :return: str
        """

        return str(helpers.get_max_version())

    @staticmethod
    def get_main_window():
        """
        Returns Qt object that references to the main DCC window
        :return:
        """

        return gui.get_max_window()

    @staticmethod
    def clear_selection():
        """
        Clears current scene selection
        """

        MaxPlus.SelectionManager.ClearNodeSelection()

    @staticmethod
    def new_file(force=True):
        """
        Creates a new file
        :param force: bool
        """

        scene.new_scene(force=force)

    @staticmethod
    def select_file_dialog(title, start_directory=None, pattern=None):
        """
        Shows select file dialog
        :param title: str
        :param start_directory: str
        :param pattern: str
        :return: str
        """

        return directory.get_file(caption=title, start_directory=start_directory, filters=pattern)

    @staticmethod
    def refresh_viewport():
        """
        Refresh current DCC viewport
        """

        viewport.force_redraw()

    @staticmethod
    def enable_undo():
        """
        Enables undo functionality
        """

        return False

    @staticmethod
    def disable_undo():
        """
        Disables undo functionality
        """

        return False


register.register_class('Dcc', MaxDcc)
