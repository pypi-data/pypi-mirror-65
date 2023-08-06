#!/usr/bin/env python
"""
Library for handling the NexSON format for phylogenetic trees used by the phylesystem
portion of the Open Tree of Life project
"""
# Some imports to help our py2 code behave like py3
from __future__ import absolute_import, print_function, division

__version__ = '0.0.2'  # sync with setup.py
__all__ = ['syntax',
           'validation',
           'proxy']

from .validation import validate_nexson
from .proxy import NexsonProxy

