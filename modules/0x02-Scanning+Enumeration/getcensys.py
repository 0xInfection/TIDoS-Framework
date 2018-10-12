#!/usr/bin/env python
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework

from __future__ import print_function
import re
import mechanize
import socket
import cookielib
import subprocess
import time
from re import search
from getports import *
from core.Core.colors import *

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [
    ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def getos0x00(web):

    global flag
    flag = 0x00
    ip_addr = socket.gethostbyname(web)
    print(GR+' [*] Getting ip address...')
    time.sleep(0.7)
    print(G+' [+] Website IP : ' +O+ str(ip_addr))
    time.sleep(0.5)
    print(GR+' [*] Trying to identify operating system...')
    time.sleep(0.5)
    print(O+' [!] Configuring requests...')
    result = br.open('https://www.censys.io/ipv4/%s/raw' % ip_addr).read()
    print(GR+' [*] Getting raw data...')
    time.sleep(0.8)
    print(R+' [*] Analysing responses...')
    try:
        match = search(r'&#34;os_description&#34;: &#34;[^<]*&#34;', result) # regex forked from Striker
        if match:
            flag = 0x01
            print(B+' [+] Operating System Identified : ' + C+ match.group().split('n&#34;: &#34;')[1][:-5])

        else:
            print(R+' [-] No exact OS match for '+O+web+'...')
            flag = 0x00
        return flag

    except Exception as e:
        print(R+' [-] Unhandled Exception : '+str(e))
