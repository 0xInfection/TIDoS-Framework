#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search, I


def stingray(headers, content):
    detect = False
    detect |= search(r'X-Mapping-', str(headers.keys()), I) is not None
    if detect:
        return "Stingray Application Firewall (Riverbed / Brocade)"
