#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID (Modified version from wascan)
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from re import search,I

def radware(headers,content):
    detect = False
    for header in headers.items():
        detect |= header[0] == "x-sl-compstate"
        if detect:break
    detect |= search(r'Unauthorized Activity Has Been Detected.+Case Number:',content) is not None
    if detect :
        return "AppWall (Radware)"
