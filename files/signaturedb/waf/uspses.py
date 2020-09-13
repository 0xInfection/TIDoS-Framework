#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework


def uspses(headers, content):
    detect = False
    detect |= headers['server'] == 'Secure Entry Server'.lower()
    if detect:
        return "USP Secure Entry Server (United Security Providers)"
