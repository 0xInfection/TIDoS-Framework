#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search, I


def sucuri(headers, content):
    detect = False
    detect |= search(r"Questions\?.+cloudproxy@sucuri\.net", content) is not None
    detect |= search(r"Sucuri WebSite Firewall - CloudProxy - Access Denied", content) is not None
    detect |= search('sucuri/cloudproxy', str(headers.values()), I) is not None
    if detect:
        return "CloudProxy WebSite Firewall (Sucuri)"
