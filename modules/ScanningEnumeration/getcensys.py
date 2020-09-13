#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import re
import requests
import socket
import http.cookiejar
import subprocess
import time
from modules.ScanningEnumeration.getports import getports
from core.Core.colors import *

info = "This module tries to determine the target's OS using censys."
searchinfo = "OS Identifier"
properties = {}

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

def getos0x00(web):
    name = targetname(web)
    lvl2 = "getcensys"
    module = "ScanANDEnum"
    lvl1 = "Scanning & Enumeration"
    lvl3 = ""
    global flag
    flag = 0x00
    ip_addr = socket.gethostbyname(web)
    print(C+' [*] Querying Reverse DNS...')
    time.sleep(0.7)
    print(O+' [+] Website IP :' +C+color.TR3+C+G+ str(ip_addr)+C+color.TR2+C)
    time.sleep(0.5)
    print(GR+' [*] Trying to identify operating system...')
    time.sleep(0.5)
    print(C+' [!] Configuring requests...')
    result = requests.get('https://www.censys.io/ipv4/%s/raw' % ip_addr).text
    print(GR+' [*] Getting raw data...')
    time.sleep(0.8)
    print(R+' [*] Analysing responses...')
    try:
        match = re.search(r'&#34;os_description&#34;: &#34;[^<]*&#34;', result)
        if match:
            flag = 0x01
            os = match.group().split('n&#34;: &#34;')[1][:-5]
            print(B+' [+] Operating System Identified : ' + C+ os)
            save_data(database, module, lvl1, lvl2, lvl3, name, os)
        else:
            print(R+' [-] No exact Operating System matches for '+O+web+C+'...')
            save_data(database, module, lvl1, lvl2, lvl3, name, "No exact Operating System matches for "+web)
            os = ""
            flag = 0x00
        return (flag, os)
    except Exception as e:
        print(R+' [-] Unhandled Exception : '+str(e))

def attack(web):
    web = web.fullurl
    getos0x00(web)