#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


from core.methods.tor import session
import time
from core.Core.colors import *

info = "Ping the target using an external API."
searchinfo = "Ping Check"
properties = {}

def piweb(web):
    requests = session()
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
        print(color.END+ nping+C)
    else:
        print(R+' [-] Outbound Query Exception!')
        time.sleep(0.8)

def attack(web):
    web = web.fullurl
    piweb(web)