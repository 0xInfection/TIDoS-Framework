#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/VainlyStrain/TIDoS

from re import search, I


def blockdos(headers, content):
    detect = False
    for header in headers.items():
        detect |= search(r'blockdos\.net', header[1], I) is not None
        if detect:
            break
    if detect:
        return "BlockDos"
