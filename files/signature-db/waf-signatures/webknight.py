#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID (Modified version from wascan)
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from re import search,I

def webknight(headers,content):
    detect = False
    detect |= headers['server'] == 'WebKnight'.lower()
    if detect :
        return "WebKnight Application Firewall (AQTRONIX)"
