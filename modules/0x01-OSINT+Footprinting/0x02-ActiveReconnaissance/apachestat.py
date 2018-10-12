#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework

from __future__ import print_function
import os
import time
import requests
import urlparse
from colors import *

def apachestat(web):

    flag = 0x00
    print(GR+' [*] Loading module...')
    time.sleep(0.7)
    print(R+'\n    ===========================')
    print(R+'     A P A C H E   S T A T U S ')
    print(R+'    ===========================\n')
    print(O+' [*] Importing fuzz parameters...')
    time.sleep(0.7)
    print(GR+' [*] Initializing bruteforce...')
    with open('files/fuzz-db/apachestat_paths.lst','r') as paths:
        for path in paths:
            path = path.replace('\n','')
            url = web + path
            print(B+' [+] Trying : '+C+url)
            resp = requests.get(url, allow_redirects=False, verify=False, timeout=7)
            if resp.status_code == 200 or resp.status_code == 302:
                print(G+' [+] Apache Server Status Enabled at : '+O+url)
                flag = 0x01

    if flag == 0x00:
        print(R+' [-] No server status enabled!')
    print(G+' [+] Apache server status completed!\n')
