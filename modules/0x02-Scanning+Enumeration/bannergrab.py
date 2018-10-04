#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

from __future__ import print_function
import shodan
import requests
import socket
import json
import time
import sys
sys.path.append('files/')
from colors import *
from files.API_KEYS import SHODAN_API_KEY

def grab(web):

    	api = shodan.Shodan(SHODAN_API_KEY)
    	print(GR+' [*] Resolving hostnames...')
    	time.sleep(0.7)
    	dnsResolve = 'https://api.shodan.io/dns/resolve?hostnames=' + web + '&key=' + SHODAN_API_KEY

    	try:
		resolved = requests.get(dnsResolve)
		print(O+' [!] Parsing information...')
		hostIP = resolved.json()[web]

		print(O+' [!] Setting query parameters...')
		host = api.host(hostIP)

		for item in host['data']:
		    	print(GR+'\n [+] Port : '+O+ str(item['port']))
		    	print(B+' [+] Banner : \n')
		    	for q in str(item['data']).splitlines():
		    		if ':' in q:
					print(G+'    '+q.split(':')[0]+' : '+O+q.split(':')[1].strip())
				else:
					print(C+'    '+q)
					time.sleep(0.02)

    	except KeyboardInterrupt:
        	print(R+' [-] An error occured...\n')

def bannergrab(web):

	print(R+'\n    ===============================')
	print(R+'     B A N N E R   G R A B B I N G')
	print(R+'    ===============================\n')

	print(GR+' [*] Parsing Url...')
	web = web.replace('http://','')
	web = web.replace('https://','')
	grab(web)
	print(G+'\n [+] Banner Grabbing Done!')
