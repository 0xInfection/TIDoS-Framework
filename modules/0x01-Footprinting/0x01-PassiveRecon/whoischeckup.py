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

def whoischeckup(web):

    web = web.replace('http://','')
    web = web.replace('https://','')
    print R+'\n   ========================='
    print R+'    W H O I S   L O O K U P'
    print R+'   =========================\n'
    time.sleep(0.4)
    print('' + GR + color.BOLD + ' [!] Looking Up for WhoIS Information...')
    time.sleep(0.4)
    print(""+ GR + color.BOLD + " [~] Result: \n"+ color.END)
    domains = [web]
    for dom in domains:
        text = requests.get('http://api.hackertarget.com/whois/?q=' + dom).text
	nping = str(text)
	if 'error' not in nping:
		print G+ nping
	else:
		print R+' [-] Outbound Query Exception!'
		time.sleep(0.8)
