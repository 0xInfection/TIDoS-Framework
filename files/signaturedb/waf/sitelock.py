#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search


def sitelock(headers, content):
    detect = False
    detect |= search(r"SiteLock Incident ID", content) is not None
    if detect:
        return "TrueShield Web Application Firewall (SiteLock)"
