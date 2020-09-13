#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import time
from core.methods.tor import session
import urllib.parse
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Apache server status hunter."
searchinfo = "Apache Status Hunter"
properties = {}

def apachestat(web):
    name = targetname(web)
    requests = session()
    lvl2 = "apachestat"
    module = "ReconANDOSINT"
    lvl1 = "Active Reconnaissance"
    lvl3 = ""
    flag = 0x00
    time.sleep(0.7)
    #print(R+'\n    ===========================')
    #print(R+'     A P A C H E   S T A T U S ')
    #print(R+'    ===========================\n')

    from core.methods.print import posintact
    posintact("apache status") 

    print(C+' [*] Importing fuzz parameters...')
    time.sleep(0.7)
    print(GR+' [*] Initializing bruteforce...')
    with open('files/fuzz-db/apachestat_paths.lst','r') as paths:
        for path in paths:
            path = path.replace('\n','')
            url = web + path
            print(B+' [+] Trying : '+C+url)
            resp = requests.get(url, allow_redirects=False, verify=False, timeout=7)
            if resp.status_code == 200 or resp.status_code == 302:
                print(O+' [+] Apache Server Status Enabled at :'+C+color.TR3+C+G+url+C+color.TR2+C)
                flag = 0x01
                save_data(database, module, lvl1, lvl2, lvl3, name, url)

    if flag == 0x00:
        save_data(database, module, lvl1, lvl2, lvl3, name, "No server status enabled.")
        print(R+' [-] No server status enabled!')

    print(C+' [+] Apache server status completed!\n')

def attack(web):
    web = web.fullurl
    apachestat(web)