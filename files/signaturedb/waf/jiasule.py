#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID (Modified version from wascan)
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

from re import search, I


def jiasule(headers, content):
    detect = False
    for header in headers.items():
        detect |= search(r'__jsluid=|jsl_tracking', header[1], I) is not None
        detect |= search(r'jiasule-waf', header[1], I) is not None
        if detect: break
    detect |= search(r'static\.jiasule\.com/static/js/http_error\.js', content) is not None
    if detect:
        return "Jiasule Web Application Firewall (Jiasule)"
