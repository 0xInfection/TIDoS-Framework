#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import time
import os
import requests
from colors import *

final_links = []

def links(web):

    print R+'\n   ====================='
    print R+'    P A G E   L I N K S '
    print R+'   =====================\n'
    time.sleep(0.4)
    print('' + GR + color.BOLD + ' [!] Fetching links to the website...')
    time.sleep(0.4)
    print(""+ GR + color.BOLD + " [~] Result: "+ color.END)
    web0 = web.strip('http://')
    domains = [web]
    for dom in domains:
        text = requests.get('http://api.hackertarget.com/pagelinks/?q=' + dom).text
	result = str(text)
	if 'error' not in result and 'no links found' not in result:

		woo = result.split('\n')
		for w in woo:
			if str(web0).lower() in w.lower():
				final_links.append(w)

		print O+'\n [!] Receiving links...'
		for p in final_links:
			print G+' [+] Found link : '+O+p
			time.sleep(0.15)

		w = raw_input(GR+"\n [*] Save this as a output file? (y/n) :> ")
		if 'http://' in web:
			po = web.replace('http://','')
		elif 'https://' in web:
			po = web.replace('https://','')
		p = str(po) + '-links.lst'
		open(p, 'w+')
		if w == "y":
			print''+B+' [!] Generating output...'
			time.sleep(1)
			for m in final_links:
			    m = m + '\n'
			    ile = open(p,"a")
			    ile.write(m)
			    ile.close()
			o = 'mv '+p+' files/'
			os.system(o)
			print G+' [+] Successfully saved under "files/'+p+'!'
			print ''
		else:
			    print ''+B+' [*] Okay :)'

	else:
		print R+' [-] Outbound Query Exception!'
		time.sleep(0.8)

