#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions and classes related with directories and files in 3ds Max
"""

from __future__ import print_function, division, absolute_import

import MaxPlus


def get_file(caption='Select File', filters='*', start_directory=''):
    try:
        result = MaxPlus.Core.EvalMAXScript('getOpenFileName \
            caption:"{}" \
            filename:"{}" \
            types:"{}";'.format(caption, start_directory, filters)).Get()
        return result
    except Exception:
        return None
