#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search


def dotdefender(headers, content):
    detect = False
    for header in headers.items():
        detect |= header[0] == "x-dotdefender-denied"
        if detect: break
    detect |= search(r"dotDefender Blocked Your Request", content) is not None
    if detect:
        return "dotDefender (Applicure Technologies)"
