#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search


def sophos(headers, content):
    detect = False
    detect |= search(r"Powered by UTM Web Protection", content) is not None
    if detect:
        return "UTM Web Protection (Sophos)"
