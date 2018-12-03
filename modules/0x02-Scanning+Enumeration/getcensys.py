#!/usr/bin/env python
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import re
import requests
import socket
import cookielib
import subprocess
import time
from getports import *
from core.Core.colors import *

def getos0x00(web):

    global flag
    flag = 0x00
    ip_addr = socket.gethostbyname(web)
    print(C+' [*] Querying Reverse DNS...')
    time.sleep(0.7)
    print(G+' [+] Website IP : ' +O+ str(ip_addr))
    time.sleep(0.5)
    print(GR+' [*] Trying to identify operating system...')
    time.sleep(0.5)
    print(O+' [!] Configuring requests...')
    result = requests.get('https://www.censys.io/ipv4/%s/raw' % ip_addr).text
    print(GR+' [*] Getting raw data...')
    time.sleep(0.8)
    print(R+' [*] Analysing responses...')
    try:
        match = re.search(r'&#34;os_description&#34;: &#34;[^<]*&#34;', result)
        if match:
            flag = 0x01
            print(B+' [+] Operating System Identified : ' + C+ match.group().split('n&#34;: &#34;')[1][:-5])
        else:
            print(R+' [-] No exact Operating System matches for '+O+web+'...')
            flag = 0x00
        return flag
    except Exception as e:
        print(R+' [-] Unhandled Exception : '+str(e))
