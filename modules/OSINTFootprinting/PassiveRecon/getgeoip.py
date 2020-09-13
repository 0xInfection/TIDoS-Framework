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
import socket
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Find out where the target server is located."
searchinfo = "GeoIP Lookup"
properties = {}

def getgeoip(web):
    name = targetname(web)
    requests = session()
    web = web.replace('http://','')
    web = web.replace('https://','')
    if "@" in web:
        web = web.split("@")[1]
    #print(R+'\n   =========================')
    #print(R+'    G E O I P   L O O K U P')
    #print(R+'   =========================\n')
    from core.methods.print import posintpas
    posintpas("geoip lookup")
    time.sleep(0.4)
    print(GR+' [!] Looking Up for WhoIS Information...')
    time.sleep(0.4)
    print(GR+" [~] Found GeoIp Location: \n")
    domains = socket.gethostbyname(web)
    time.sleep(0.6)
    text = requests.get('http://api.hackertarget.com/geoip/?q=' + domains).text
    result = str(text)
    if 'error' not in result and 'invalid' not in result:
        res = result.splitlines()
        for r in res:
            print(O+' [+] ' + r.split(':')[0].strip() + ''+C+color.TR3+C+G+ r.split(':')[1].strip()+C+color.TR2+C)
            time.sleep(0.1)

    else:
        print(R+' [-] Outbound Query Exception!')
        time.sleep(0.8)
     
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl2 = inspect.stack()[0][3]
    lvl3 = ""
    data = result
    save_data(database, module, lvl1, lvl2, lvl3, name, data)

def attack(web):
    web = web.fullurl
    getgeoip(web)
    #print(inspect.stack()[0][3])  --> attack
