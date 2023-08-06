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

__all__ = ['format_exception']

def format_exception(ei):
    import io
    import traceback

    sio = io.StringIO()
    tb = ei[2]
    # if getattr(self, 'fullstack', False):
    #     traceback.print_stack(tb.tb_frame.f_back, file=sio)
    traceback.print_exception(ei[0], ei[1], tb, None, sio)
    s = sio.getvalue()
    sio.close()
    if s[-1:] == "\n":
        s = s[:-1]
    return s
