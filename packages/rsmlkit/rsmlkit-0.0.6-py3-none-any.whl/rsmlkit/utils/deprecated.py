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
from rsmlkit.logging import get_logger
logger = get_logger(__file__)

__all__ = ['deprecated']

def deprecated(fn):
    @functools.wraps(fn)
    def new_fn(*args, **kwargs):
        if fn not in deprecated.recorded:
            deprecated.recorded.add(fn)
            logger.warning(fn.__doc__)
        return fn(*args, **kwargs)
    return new_fn

deprecated.recorded = set()
