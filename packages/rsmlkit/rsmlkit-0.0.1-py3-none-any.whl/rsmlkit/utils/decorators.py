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

import functools
import collections
import threading
import contextlib


__all__ = ['decorator_with_optional_args',
           'synchronized']

def decorator_with_optional_args(func=None, *, is_method=False):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if is_method:
                if len(args) == 1:
                    return f(*args, **kwargs)
                elif len(args) == 2:
                    return f(args[0], **kwargs)(args[1])
                else:
                    raise ValueError('Decorator supports 0 or 1 positional arguments as the function to be wrapped.')
            else:
                if len(args) == 0:
                    return f(**kwargs)
                elif len(args) == 1:
                    return f(**kwargs)(args[0])
                else:
                    raise ValueError('Decorator supports 0 or 1 positional arguments as the function to be wrapped.')
        return wrapped

    if func is not None:
        return wrapper(func)
    else:
        return wrapper

@decorator_with_optional_args
def synchronized(mutex=None):
    if mutex is None:
        mutex = threading.Lock()

    def wrapper(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            with mutex:
                return func(*args, **kwargs)
        wrapped_func.__sync_mutex__ = mutex
        return wrapped_func

    return wrapper