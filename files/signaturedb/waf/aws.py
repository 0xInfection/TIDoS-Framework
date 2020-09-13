#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search, I


def aws(headers, content):
    detect = False
    for header in headers.items():
        detect |= search(r'\bAWS', header[1], I) is not None
    if detect:
        return "Amazon Web Services Web Application Firewall (Amazon)"
