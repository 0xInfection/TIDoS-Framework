#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID (Modified version from wascan)
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from re import search,I

def sonicwall(headers,content):
    detect = False
    detect |= search(r"This request is blocked by the SonicWALL",content) is not None
    detect |= search(r"Web Site Blocked.+\bnsa_banner",content) is not None
    detect |= headers['server'] == 'sonicwall'
    if detect :
        return "SonicWALL (Dell)"
