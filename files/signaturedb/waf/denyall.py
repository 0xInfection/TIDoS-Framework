#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search, I


def denyall(headers, content):
    detect = False
    for header in headers.items():
        detect |= search(r'sessioncookie=', header[1], I) is not None
        if detect: break
    detect |= search(r"Condition Intercepted", content) is not None
    if detect:
        return "Deny All Web Application Firewall (DenyAll)"
