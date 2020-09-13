#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search, I


def teros(headers, content):
    detect = False
    detect |= search(r'st8\(id|_wat|_wlf\)', str(headers.values()), I) is not None
    if detect:
        return "Teros/Citrix Application Firewall Enterprise (Teros/Citrix Systems)"
