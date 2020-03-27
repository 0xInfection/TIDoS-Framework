#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


import time
import os
import sys
sys.path.append('tmp/')
from core.methods.tor import session
from core.Core.colors import *

final_links = []

info = "Find Links pointing to the target."
searchinfo = "Page Links"
properties = {}

def links(web):
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

            if 'http://' in web:
                po = web.replace('http://','')
            elif 'https://' in web:
                po = web.replace('https://','')
            if "@" in po:
                po = po.split("@")[1]
            p = 'tmp/logs/'+po+'-logs/'+str(po)+'-links.lst'
            open(p, 'w+')
            print(B+' [!] Saving links...')
            time.sleep(1)
            for m in final_links:
                m = m + '\n'
                ile = open(p,"a")
                ile.write(m)
                ile.close()
            pa = os.getcwd()
            print(G+' [+] Links saved under '+pa+'/'+p+'!')
            print('')

        else:
            print(R+' [-] Outbound Query Exception!')
            time.sleep(0.8)

def attack(web):
    links(web)