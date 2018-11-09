#!/usr/bin/env python
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import requests, time
from time import sleep
from core.Core.colors import *

def subnet(web):

    web = web.replace('http://','')
    web = web.replace('https://','')
    time.sleep(0.4)
    print(R+'\n   ====================================')
    print(R+'    S U B N E T  E N U M E R A T I O N')
    print(R+'   ====================================\n')
    print(GR + ' [!] Enumerating subnets in network...')
    time.sleep(0.4)
    print(GR+' [*] Getting subnet class infos...\n')
    domains = [web]
    for dom in domains:
        text = requests.get('http://api.hackertarget.com/subnetcalc/?q=' + dom).text
        http = str(text)

        if 'error' not in http:
            result = http.splitlines()
            for r in result:
                print(G+' '+r.split('=')[0]+'='+O+r.split('=')[1])

        elif 'No results found' in http:
            print(R+' [-] No results found!')
        else:
            print(R+' [-] Outbound Query Exception!')
