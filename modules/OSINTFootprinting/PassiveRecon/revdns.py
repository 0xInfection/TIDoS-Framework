#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import time
from core.methods.tor import session
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect
links = []

info = "Perform a reverse DNS lookup using free API."
searchinfo = "Reverse DNS Lookup"
properties = {}

def revdns(web):
    name = targetname(web)
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl3=''
    lvl2=inspect.stack()[0][3]
    requests = session()
    web = web.split('//')[1]
    if "@" in web:
        web = web.split("@")[1]
    #print(R+'\n   =====================================')
    #print(R+'    R E V E R S E   D N S   L O O K U P')
    #print(R+'   =====================================\n')
    from core.methods.print import posintpas
    posintpas("reverse dns lookup")
    time.sleep(0.4)
    print('' + GR + color.BOLD + ' [!] Looking Up for Reverse DNS Info...')
    time.sleep(0.4)
    print(""+ GR + color.BOLD + " [~] Result: \n"+ color.END)
    text = requests.get('http://api.hackertarget.com/reversedns/?q=' + web)
    result = text.text
    if 'error' not in result and 'no result' not in result.lower():
        res = result.splitlines()
        for r in res:
            print(r)
            print(O+' [+] Received :'+C+color.TR3+C+G+r.split(',')[0].strip()+' => '+C+'('+r.split(',')[1].strip()+')'+C+color.TR2+C)
            time.sleep(0.04)
            links.append(r)

        data = result
        save_data(database, module, lvl1, lvl2, lvl3, name, data)

    else:
        print(R+' [-] No result found!')
        save_data(database, module, lvl1, lvl2, lvl3, name, "No result found.")
        time.sleep(0.8)

def attack(web):
    web = web.fullurl
    revdns(web)
