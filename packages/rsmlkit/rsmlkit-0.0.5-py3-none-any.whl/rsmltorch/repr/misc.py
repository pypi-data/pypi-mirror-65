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

import time
import math
from typing import List, Any, Iterable
import torch
from torch.autograd import Variable

__all__ = ['time_since']

def make_onehot(cat, categories:List):
    ci = categories.index(cat)
    t = torch.zeros(1, len(categories))
    t[0][ci] = 1
    return Variable(t)

def time_since(t):
    now = time.time()
    s = now - t
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)