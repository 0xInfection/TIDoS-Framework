#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import os
import time
import requests
from colors import *
links = []

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
		res = result.splitlines()
		for r in res:
			print GR+' [+] Received : '+O+r
			time.sleep(0.04)
			links.append(r)

		if 'http://' in web:
			po = web.replace('http://','')
		elif 'https://' in web:
			po = web.replace('https://','')
		p = 'tmp/logs/'+po+'-logs/'+str(po)+'-reverse-dns.lst'
		open(p,'w+')
		print B+' [!] Saving links...'
		time.sleep(1)
		for m in links:
		    m = m + '\n'
		    ile = open(p,"a")
		    ile.write(m)
		    ile.close()
		pa = os.getcwd()
		print G+' [+] Links saved under '+pa+'/'+p+'!'
		print ''

	elif 'No results found' in result:
		print R+' [-] No result found!'
	else:
		print R+' [-] Outbound Query Exception!'
		time.sleep(0.8)

