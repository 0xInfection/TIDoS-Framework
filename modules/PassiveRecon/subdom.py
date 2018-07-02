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

def subdom(web):

    web = web.replace('http://','')
    web = web.replace('https://','')
    print R+'\n   ==================================='
    print R+'    S U B D O M A I N S   L O O K U P'
    print R+'   ===================================\n'
    time.sleep(0.4)
    print('' + GR + color.BOLD + ' [!] Looking Up for subdomains...')
    time.sleep(0.4)
    print(""+ GR + color.BOLD + " [~] Result: "+ color.END)
    domains = [web]
    for dom in domains:
        text = requests.get('http://api.hackertarget.com/hostsearch/?q=' + dom).text
	result = str(text)
	if 'error' not in result:
		res = result.splitlines()
		for r in res:
			sub = r.split(',')[0]
			print B+' [+] Got subdomain :> '+C+sub
	else:
		print R+' [-] Outbound Query Exception!'
		time.sleep(0.8)

