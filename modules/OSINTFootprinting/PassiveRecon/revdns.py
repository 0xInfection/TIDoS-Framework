#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


import os
import time
from core.methods.tor import session
from core.Core.colors import *
links = []

info = "Perform a reverse DNS lookup using free API."
searchinfo = "Reverse DNS Lookup"
properties = {}

def revdns(web):
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

        p = 'tmp/logs/'+web+'-logs/'+web+'-reverse-dns.lst'
        open(p,'w+')
        print(P+' [!] Saving links...'+C)
        time.sleep(1)
        for m in links:
            m = m + '\n'
            ile = open(p,"a")
            ile.write(m)
            ile.close()
        pa = os.getcwd()
        print(C+' [+] Links saved under '+pa+'/'+p+'!')
        print('')

    else:
        print(R+' [-] No result found!')
        time.sleep(0.8)

def attack(web):
    web = web.fullurl
    revdns(web)