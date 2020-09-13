#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
import os
import sys
sys.path.append('tmp/')
from core.methods.tor import session
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

final_links = []

info = "Find Links pointing to the target."
searchinfo = "Page Links"
properties = {}

def links(web):
    name = targetname(web)
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl3=''
    lvl2=inspect.stack()[0][3]
    requests = session()
    #print(R+'\n   =====================')
    #print(R+'    P A G E   L I N K S ')
    #print(R+'   =====================\n')
    from core.methods.print import posintpas
    posintpas("page links")
    time.sleep(0.4)
    print('' + GR + color.BOLD + ' [!] Fetching links to the website...')
    time.sleep(0.4)
    print(GR +" [~] Result: "+ color.END)


    if "https://" in web:
        web0 = web.replace('https://','')
    else:
        web0 = web.replace('http://','')
    if "@" in web:
        if "https" in web:
            web = "https://" + web.split("@")[1]
        else:
            web = "http://" + web.split("@")[1]
        web0 = web0.split("@")[1]

    domains = [web]
    for dom in domains:
        text = requests.get('http://api.hackertarget.com/pagelinks/?q=' + dom).text
        result = str(text)
        if 'null' not in result and 'no links found' not in result:

            woo = result.splitlines()
            for w in woo:
                if str(web0).lower() in w.lower():
                    final_links.append(w)

            print(C+'\n [!] Receiving links...')
            for p in final_links:
                print(O+' [+] Found link :'+C+color.TR3+C+G+p+C+color.TR2+C)
                time.sleep(0.06)

            save_data(database, module, lvl1, lvl2, lvl3, name, str(final_links))
            print('')

        else:
            print(R+' [-] Outbound Query Exception!')
            time.sleep(0.8)

def attack(web):
    web = web.fullurl
    links(web)