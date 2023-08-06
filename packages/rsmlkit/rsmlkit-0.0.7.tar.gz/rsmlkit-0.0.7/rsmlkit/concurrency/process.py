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
import time
import multiprocessing as mp
import queue
import os

from rsmlkit.logging import get_logger
logger = get_logger(__file__)

__all__ = ['RSProcess']

class RSProcess(mp.Process):
    def __init__(self, *args, **kwargs):
        super().init(*args, **kwargs)

    def run(self) -> None:
        logger.critical(f'RSProcess: pid={os.getpid()}, ppid={os.getppid()}')
        super().run()

    def __call__(self):
        self.start()
        self.join()










