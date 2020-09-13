#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search


def secureiis(headers, content):
    detect = False
    detect |= search(r"SecureIIS[^<]+Web Server Protection", content) is not None
    detect |= search(r"http://www.eeye.com/SecureIIS/", content) is not None
    detect |= search(r"\?subject=[^>]*SecureIIS Error", content) is not None
    if detect:
        return "SecureIIS Web Server Security (BeyondTrust)"
