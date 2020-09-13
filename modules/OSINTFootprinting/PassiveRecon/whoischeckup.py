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
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Perform a WhoIS lookup on the target."
searchinfo = "WhoIS Lookup"
properties = {}

def whoischeckup(web):
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
    #print(R+'\n   =========================')
    #print(R+'    W H O I S   L O O K U P')
    #print(R+'   =========================\n')
    from core.methods.print import posintpas
    posintpas("whois lookup")
    time.sleep(0.4)
    print('' + GR + color.BOLD + ' [!] Looking Up for WhoIS Information...')
    time.sleep(0.4)
    print(""+ GR + color.BOLD + " [~] Result: \n"+ color.END)
    domains = [web]
    for dom in domains:
        text = requests.get('http://api.hackertarget.com/whois/?q=' + dom).text
        res = str(text)
        if 'error' not in res:
            print(color.END+ res+C)
            save_data(database, module, lvl1, lvl2, lvl3, name, res)
        else:
            print(R+' [-] Outbound Query Exception!')
            time.sleep(0.8)

def attack(web):
    web = web.fullurl
    whoischeckup(web)