#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework


def wallarm(headers, content):
    detect = False
    detect |= headers['server'] == 'nginx-wallarm'
    if detect:
        return "Wallarm Web Application Firewall (Wallarm)"
