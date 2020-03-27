#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


import time
from core.methods.tor import session
from core.Core.colors import *

info = "Perform a WhoIS lookup on the target."
searchinfo = "WhoIS Lookup"
properties = {}

def whoischeckup(web):
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
        nping = str(text)
        if 'error' not in nping:
            print(color.END+ nping+C)
        else:
            print(R+' [-] Outbound Query Exception!')
            time.sleep(0.8)

def attack(web):
    whoischeckup(web)