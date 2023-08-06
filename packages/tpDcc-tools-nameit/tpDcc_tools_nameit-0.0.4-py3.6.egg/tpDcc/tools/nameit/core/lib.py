#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains base naming library for tpDcc-tools-nameit
"""

from __future__ import print_function, division, absolute_import

from tpDcc.libs.python import decorators

from tpDcc.libs.nameit.core import namelib


@decorators.Singleton
class NameItLib(namelib.NameLib, object):
    pass
