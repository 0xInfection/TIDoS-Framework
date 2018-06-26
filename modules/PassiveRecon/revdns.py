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
from colors import *

def revdns(web):

    web = web.replace('http://','')
    web = web.replace('https://','')
    print R+'\n   ====================================='
    print R+'    R E V E R S E   D N S   L O O K U P'
    print R+'   =====================================\n'
    time.sleep(0.4)
    print('' + GR + color.BOLD + ' [!] Looking Up for Reverse DNS Info...')
    time.sleep(0.4)
    print(""+ GR + color.BOLD + " [~] Result: \n"+ color.END)
    domains = [web]
    for dom in domains:
        text = requests.get('http://api.hackertarget.com/reversedns/?q=' + dom).text
	result = str(text)
	if 'error' not in result:
		print G+ result
	elif 'No results found' in result:
		print R+' [-] No result found!'
	else:
		print R+' [-] Outbound Query Exception!'
		time.sleep(0.8)
