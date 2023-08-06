#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functionality for Maya windows
"""

from __future__ import print_function, division, absolute_import

from tpDcc import register
from tpDcc.libs.qt.core import window as core_window


class MaxWindow(core_window.MainWindow, object):
    def __init__(self, *args, **kwargs):
        super(MaxWindow, self).__init__(*args, **kwargs)


register.register_class('Window', MaxWindow)
register.register_class('DockWindow', MaxWindow)
register.register_class('SubWindow', MaxWindow)
