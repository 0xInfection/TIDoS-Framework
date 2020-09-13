#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
from core.methods.tor import session
import os
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect
links = []

info = "Perform a reverse IP lookup using a free API."
searchinfo = "Reverse IP Lookup"
properties = {}

def revip(web):
    name = targetname(web)
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl3=''
    lvl2=inspect.stack()[0][3]
    requests = session()
    web = web.replace('http://','')
    web = web.replace('https://','')
    if "@" in web:
        web = web.split("@")[1]
    #print(R+'\n   ===================================')
    #print(R+'    R E V E R S E   I P   L O O K U P')
    #print(R+'   ===================================\n')
    from core.methods.print import posintpas
    posintpas("reverse ip lookup")
    time.sleep(0.4)
    print('' + GR + color.BOLD + ' [!] Looking Up for Reverse IP Info...')
    time.sleep(0.4)
    print(""+ GR + color.BOLD + " [~] Result : \n"+ color.END)
    domains = [web]
    for dom in domains:
        text = requests.get('http://api.hackertarget.com/reverseiplookup/?q=' + dom).text
        result = str(text)
        res = result.splitlines()
        if 'error' not in result:
            for r in res:
                print(O+' [+] Site :>'+C+color.TR3+C+G+r+C+color.TR2+C)
                links.append(r)
                time.sleep(0.04)
            save_data(database, module, lvl1, lvl2, lvl3, name, result)

        elif 'error' in result:
            print(R+' [-] Outbound Query Exception!')
            time.sleep(0.8)

def attack(web):
    web = web.fullurl
    revip(web)
