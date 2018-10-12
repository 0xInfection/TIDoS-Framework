#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework

from __future__ import print_function
import time
import requests
import socket
from core.Core.colors import *

def getgeoip(web):

    web = web.replace('http://','')
    web = web.replace('https://','')
    print(R+'\n   =========================')
    print(R+'    G E O I P   L O O K U P')
    print(R+'   =========================\n')
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
            print(G+' [+] ' + r.split(':')[0].strip() + ' : ' +O+ r.split(':')[1].strip())
            time.sleep(0.1)

    else:
        print(R+' [-] Outbound Query Exception!')
        time.sleep(0.8)
