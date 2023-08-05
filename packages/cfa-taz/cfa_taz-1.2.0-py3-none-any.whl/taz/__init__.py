#!/usr/bin/env python3
# coding: utf8
# -----------------------------------------------------------------
# hermes: __init__.py
#
# Copyright (C) 2018-2019, Christophe Fauchard
# -----------------------------------------------------------------
"""
Module: taz

Trivial Azure API

Copyright (C) 2018-2019, Christophe Fauchard
"""

import sys
from taz._version import __version__, __version_info__

__author__ = "Christophe Fauchard <christophe.fauchard@gmail.com>"

if sys.version_info < (3, 6):
    raise RuntimeError('You need Python 3.6+ for this module.')
