#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import os
import time
import requests
from core.Core.colors import *
links = []

def revdns(web):

    web = web.split('//')[1]
    print(R+'\n   =====================================')
    print(R+'    R E V E R S E   D N S   L O O K U P')
    print(R+'   =====================================\n')
    time.sleep(0.4)
    print('' + GR + color.BOLD + ' [!] Looking Up for Reverse DNS Info...')
    time.sleep(0.4)
    print(""+ GR + color.BOLD + " [~] Result: \n"+ color.END)
    text = requests.get('http://api.hackertarget.com/reversedns/?q=' + web)
    result = text.text
    if 'error' not in result and 'no results' not in result.lower():
        res = result.splitlines()
        for r in res:
            print(B+' [+] Received : '+O+r.split(',')[0].strip()+' => '+C+'('+r.split(',')[1].strip()+')')
            time.sleep(0.04)
            links.append(r)

        p = 'tmp/logs/'+web+'-logs/'+web+'-reverse-dns.lst'
        open(p,'w+')
        print(B+' [!] Saving links...')
        time.sleep(1)
        for m in links:
            m = m + '\n'
            ile = open(p,"a")
            ile.write(m)
            ile.close()
        pa = os.getcwd()
        print(G+' [+] Links saved under '+pa+'/'+p+'!')
        print('')

    else:
        print(R+' [-] No result found!')
        time.sleep(0.8)

