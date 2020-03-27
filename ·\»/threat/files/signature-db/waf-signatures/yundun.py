#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID (Modified version from wascan)
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from re import search,I

def yundun(headers,content):
    detect = False
    detect |= headers['server'] == 'YUNDUN'
    if 'x-cache' in headers.keys():
        detect |= headers['x-cache'] == 'YUNDUN'
    if detect :
        return "Yundun Web Application Firewall (Yundun)"
