#!/usr/bin/env python3
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
from core.methods.tor import session
from time import sleep
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Enumerate subnets of the target's network."
searchinfo = "Subnet Enumeration"
properties = {}

def subnet(web):
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
    time.sleep(0.4)
    #print(R+'\n   ====================================')
    #print(R+'    S U B N E T  E N U M E R A T I O N')
    #print(R+'   ====================================\n')
    from core.methods.print import posintpas
    posintpas("subnet enumeration")
    print(GR + ' [!] Enumerating subnets in network...')
    time.sleep(0.4)
    print(GR+' [*] Getting subnet class infos...\n')
    domains = [web]
    for dom in domains:
        text = requests.get('http://api.hackertarget.com/subnetcalc/?q=' + dom).text
        #text = requests.get('https://steakovercooked.com/api/ping/?host=' + dom).text
        http = str(text)

        if 'error' not in http:
            result = http.splitlines()
            for r in result:
                print(O+' '+r.split('=')[0]+C+color.TR3+C+G+'='+r.split('=')[1]+C+color.TR2+C)
            save_data(database, module, lvl1, lvl2, lvl3, name, http)
        elif 'No results found' in http:
            print(R+' [-] No results found!')
            save_data(database, module, lvl1, lvl2, lvl3, name, "No results found.")
        else:
            print(R+' [-] Outbound Query Exception!')

def attack(web):
    web = web.fullurl
    subnet(web)
