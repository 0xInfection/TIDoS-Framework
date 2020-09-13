#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search, I


def urlscan(headers, content):
    detect = False
    detect |= search('rejected-by-urlscan', str(headers.values()), I) is not None
    detect |= search(r'Rejected-By-UrlScan', content, I) is not None
    if detect:
        return "UrlScan (Microsoft)"
