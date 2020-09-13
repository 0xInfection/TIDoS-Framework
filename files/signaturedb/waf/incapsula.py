#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search, I


def incapsula(headers, content):
    detect = False
    for header in headers.items():
        detect |= search(r'incap_ses|visid_incap', header[1], I) is not None
        detect |= search(r'incapsula', header[1], I) is not None
        if detect: break
    detect |= search(r'Incapsula incident ID', content) is not None
    if detect:
        return "Incapsula Web Application Firewall (Incapsula/Imperva)"
