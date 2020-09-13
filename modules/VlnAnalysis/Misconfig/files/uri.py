#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: 0xInfection (@_tID)
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import urllib.parse
import re
from core.Core.colors import *

info = ""
searchinfo = ""
properties = {}

def buildUrl(url, href):

    if re.search('logout',href) or re.search('action=out',href) or re.search('action=logoff', href) or re.search('action=delete',href) or re.search('UserLogout',href) or re.search('osCsid', href) or re.search('file_manager.php',href) or href=="http://localhost":#make exclusion list
        return ''

    parsed = urllib.parse.urlsplit(href)
    app=''

    if parsed[1] == urllib.parse.urlsplit(url)[1]:
        app=href

    else:
        if len(parsed[1]) == 0 and (len(parsed[2]) != 0 or len(parsed[3])!=0):
            domain = urllib.parse.urlsplit(url)[1]
            if re.match('/', parsed[2]):
                app = 'http://' + domain + parsed[2]
                if parsed[3]!='':
                    app += '?'+parsed[3]
            else:
                try:
                    app = 'http://' + domain + re.findall('(.*\/)[^\/]*', urllib.parse.urlsplit(url)[2])[0] + parsed[2]
                except IndexError:
                    app = 'http://' + domain + parsed[2]
                if parsed[3]!='':
                    app += '?'+parsed[3]
    #return '' for invalid url, url otherwise
    return app

def buildAction(url, action):

    print(GR+' [*] Parsing URL parameters...')
    if action!='' and not re.match('#',action):
        return buildUrl(url,action)
    else:
        return url
