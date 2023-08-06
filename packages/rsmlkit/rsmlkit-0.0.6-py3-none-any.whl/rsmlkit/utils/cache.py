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


import threading
import collections
import functools
import os.path as osp

from rsmlkit.utils.decorators import synchronized
from rsmlkit.logging import get_logger
logger = get_logger(__file__)

__all__ = ['cached_result', 'cached_property']

def cached_result(func):
    def impl():
        nonlocal impl
        ret = func()
        impl = lambda: ret
        return ret

    @synchronized()
    @functools.wraps(func)
    def f():
        return impl()

    return f

class cached_property:
    def __init__(self, fget):
        self.fget = fget
        self.__module__ = fget.__module__
        self.__name__ = fget.__name__
        self.__doc__ = fget.__doc__
        self.__cache_key = '__result_cache_{}_{}'.format(
            fget.__name__, id(fget))
        self.__mutex = collections.defaultdict(threading.Lock)

    def __get__(self, instance, owner):
        with self.__mutex[id(instance)]:
            if instance is None:
                return self.fget
            v = getattr(instance, self.__cache_key, None)
            if v is not None:
                return v
            v = self.fget(instance)
            assert v is not None
            setattr(instance, self.__cache_key, v)
            return v
