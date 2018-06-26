#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import time
import requests
import socket
from colors import *

def geoIP(web):

    web = web.replace('http://','')
    web = web.replace('https://','')
    print R+'\n   ========================='
    print R+'    G E O I P   L O O K U P'
    print R+'   =========================\n'
    time.sleep(0.4)
    print('' + GR + color.BOLD + ' [!] Looking Up for WhoIS Information...')
    time.sleep(0.4)
    print(""+ GR + color.BOLD + " [~] Found GeoIp Location: "+ color.END)
    domains = socket.gethostbyname(web)
    text = requests.get('http://api.hackertarget.com/geoip/?q=' + domains).text
    result = str(text)
    if 'error' not in result and 'invalid' not in result:
	res = result.splitlines()
	for r in res:
		print G+' ' + r
		time.sleep(0.1)

    else:
	print R+' [-] Outbound Query Exception!'
	time.sleep(0.8)

