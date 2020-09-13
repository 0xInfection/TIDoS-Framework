#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search, I


def binarysec(headers, content):
    detect = False
    for header in headers.items():
        detect |= header[0].lower() == "x-binarysec-via"
        detect |= header[0].lower() == "x-binarysec-nocache"
        detect |= search(r'binarySec', header[1], I) is not None
        if detect: break
    if detect:
        return "BinarySEC Web Application Firewall (BinarySEC)"
