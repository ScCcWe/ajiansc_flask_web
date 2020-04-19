# !/usr/bin/env python 
# -*- coding: utf-8 -*-
# file_name: foo.py
# author: ScCcWe
# time: 2020/4/19 11:03


def sayhello(to=None):
    if to:
        return 'Hello, %s!' % to
    return 'Hello!'
