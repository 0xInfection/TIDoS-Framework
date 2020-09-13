#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import re
import time
import urllib.request
from re import search, I
from core.Core.colors import *

content_type = 'application/xml; charset="utf-8"'

info = "DAV HTTP Enumeration module."
searchinfo = "DAV HTTP Enumeration"
properties = {}

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

def htsearch(url, name):
    lvl2 = "dav"
    module = "ReconANDOSINT"
    lvl1 = "Active Reconnaissance"
    lvl3 = ""
    print(C+' [!] Setting headers...')
    time.sleep(0.7)
    headers = {'Content-Type' : content_type}
    print(C+' [!] Setting buffers...')
    content =  "<?xml version='1.0'?>\r\n"
    content += "<g:searchrequest xmlns:g='DAV:'>\r\n"
    content += "<g:sql>\r\n"
    content += "Select 'DAV:displayname' from scope()\r\n"
    content += "</g:sql>\r\n"
    content += "</g:searchrequest>\r\n"
    time.sleep(0.7)
    print(GR+' [*] Setting the parameters...')
    req = urllib.request.Request(url,headers=headers,data=content)
    req.get_method = lambda : sr
    try:
        time.sleep(0.7)
        print(GR+' [*] Making the request...')
        resp = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(R+' [-] Exception : '+str(e))

    print(C+' [+] Matching the signatures...')
    time.sleep(0.7)
    regexp = r'<a:response>|<a:status>|xmlns:a=\"DAV:\"'
    if re.search(regexp,resp.read()) and str(resp.code) == '200':
        print(G+' [+] HTTP Search Method found Enabled!'+C+color.TR2+C)
        print(O+' [+] DAV Directory Listing at :'+C+color.TR3+C+G+url+C+color.TR2+C)
        save_data(database, module, lvl1, lvl2, lvl3, name, "htsearch: "+url)
    else:
        print(R+' [-] No HTTP Searching Profiling Found...')
        save_data(database, module, lvl1, lvl2, lvl3, name, "No HTTP Searching Profiling Found.")

def profind(url, name):
    lvl2 = "dav"
    module = "ReconANDOSINT"
    lvl1 = "Active Reconnaissance"
    lvl3 = ""
    print(C+' [!] Setting headers...')
    headers = {'Depth' : 1,
               'Content-Type' : content_type}
    time.sleep(0.7)
    print(C+' [!] Setting buffers...')
    content = "<?xml version='1.0'?>\r\n"
    content += "<a:propfind xmlns:a='DAV:'>\r\n"
    content += "<a:prop>\r\n"
    content += "<a:displayname:/>\r\n"
    content += "</a:prop>\r\n"
    content += "</a:propfind>\r\n"
    time.sleep(0.7)
    print(GR+' [*] Setting the parameters...')
    req = urllib.request.Request(url,headers=headers,data=content)
    req.get_method = lambda : pro
    time.sleep(0.7)
    try:
        print(GR+' [*] Making the request...')
        resp = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(R+' [-] Exception : '+str(e))
    time.sleep(0.7)
    print(C+' [+] Matching the signatures...')
    if 'D:href' in resp.read() and resp.code == 200:
        print(G+' [+] HTTP Profind Method Found Enabled!'+C+color.TR2+C)
        print(O+' [+] DAV Directory Listing at :'+C+color.TR3+C+G+url+C+color.TR2+C)
        save_data(database, module, lvl1, lvl2, lvl3, name, "profind: "+url)
    else:
        print(R+' [-] No Profind HTTP Profiling Found...')
        save_data(database, module, lvl1, lvl2, lvl3, name, "No Profind HTTP Profiling Found.")

def dav(web):
    name = targetname(web)
    time.sleep(0.7)
    #print(R+'\n    =========================================')
    #print(R+'     D A V   H T T P   E N U M E R A T I O N')
    #print(R+'    =========================================\n')
    from core.methods.print import posintact
    posintact("dav http enumeration") 
    time.sleep(0.7)
    print(C+' [!] Loading HTTP methods...')
    global pro, sr
    pro = 'PROFIND'
    sr = 'SEARCH'
    print(GR+'\n [*] Initiating HTTP Search module...')
    htsearch(web, name)
    print(C+' [+] HTTP Search module Completed!')
    time.sleep(1)
    print(GR+'\n [*] Initiating HTTP Profind Moule...')
    profind(web, name)
    print(C+' [+] HTTP Profind Module Completed!')

    print(G+' [+] HTTP Profiling of DAV Completed!'+C+color.TR2+C+'\n')

def attack(web):
    web = web.fullurl
    dav(web)