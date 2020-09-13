#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


from core.methods.tor import session
import time
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Ping the target using an external API."
searchinfo = "Ping Check"
properties = {}

def piweb(web):
    requests = session()
    name = targetname(web)
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl3=''
    lvl2=inspect.stack()[0][3]
    dom = web.split('//')[1]
    if "@" in dom:
        dom = dom.split("@")[1]
    #print(R+'\n   =====================')
    #print(R+'    P I N G   C H E C K ')
    #print(R+'   =====================\n')
    from core.methods.print import posintpas
    posintpas("ping check")
    time.sleep(0.4)
    print(GR + color.BOLD + ' [!] Pinging website using external APi...')
    time.sleep(0.4)
    print(GR + color.BOLD + " [~] Result: "+ color.END)
    text = requests.get('http://api.hackertarget.com/nping/?q=' + dom).text
    nping = str(text)
    if 'null' not in nping:
        save_data(database, module, lvl1, lvl2, lvl3, name, nping)
        print(color.END+ nping+C)
    else:
        print(R+' [-] Outbound Query Exception!')
        time.sleep(0.8)

def attack(web):
    web = web.fullurl
    piweb(web)
