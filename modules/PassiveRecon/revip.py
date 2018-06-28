#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import time
import requests
from colors import *

def revip(web):

    web = web.replace('http://','')
    web = web.replace('https://','')
    print R+'\n   ==================================='
    print R+'    R E V E R S E   I P   L O O K U P'
    print R+'   ===================================\n'
    time.sleep(0.4)
    print('' + GR + color.BOLD + ' [!] Looking Up for Reverse IP Info...')
    time.sleep(0.4)
    print(""+ GR + color.BOLD + " [~] Result : \n"+ color.END)
    domains = [web]
    for dom in domains:
        text = requests.get('http://api.hackertarget.com/reverseiplookup/?q=' + dom).text
	result = str(text)
	res = result.splitlines()
	if 'error' not in result:
	    for r in res:
		print O+' [+] Site :> '+G+r

	elif 'error' in result:
		print R+' [-] Outbound Query Exception!'
		time.sleep(0.8)
