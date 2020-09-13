#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search, I


def anquanboa(headers, content):
    detect = False
    for header in headers.items():
        detect |= search(r'x-powered-by-anquanbao', header[1], I) is not None
        if detect: break
    if detect:
        return "Anquanbao Web Application Firewall (Anquanbao)"
