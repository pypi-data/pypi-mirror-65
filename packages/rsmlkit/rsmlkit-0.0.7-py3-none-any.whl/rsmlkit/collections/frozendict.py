#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: ${FILE_NAME}
# Author: Raeid Saqur
# Email: rsaqur@cs.princeton.edu
# Created on: 13/04/2018
#
# This file is part of RSMLKit
# Distributed under terms of the MIT License

import sys
import collections
from collections import Mapping
import operator
import functools

from rsmlkit.logging import get_logger
logger = get_logger(__file__)

try:
    from collections import OrderedDict
except ImportError as ie:  # python < 2.7
    OrderedDict = NotImplemented
    logger.warning("OrderedDict can't be imported")


iteritems = getattr(dict, 'iteritems', dict.items)

class frozendict(Mapping):
    """
    Implements the :py:class:`collections.Mapping` interface for
    creating immutable Dictionaries (for hashing).
    """
    dict_cls = dict

    def __init__(self, *args, **kwargs):
        self._dict = self.dict_cls(*args, **kwargs)
        self._hash = None

    def __hash__(self):
        if self._hash is None:
            h = 0
            for key, value in iteritems(self._dict):
                h ^= hash((key, value))
            self._hash = h
        return self._hash

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def copy(self, **add_or_replace):
        return self.__class__(self, **add_or_replace)

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self._dict)



class FrozenOrderedDict(frozendict):
    """
    A frozendict subclass that maintains key order
    """
    dict_cls = OrderedDict


if OrderedDict is NotImplemented:
    del FrozenOrderedDict


