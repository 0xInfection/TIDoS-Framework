#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search, I


def yunsuo(headers, content):
    detect = False
    detect |= search('<img class=\"yunsuologo\"', content) is not None
    if 'cookie' in headers.keys():
        detect |= search('yunsuo_session', headers['cookie'], I) is not None
    if detect:
        return "Yunsuo Web Application Firewall (Yunsuo)"
