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
import os
from os import system
from colors import *

def sharedns(web):

    web = web.split('//')[1]
    print R+'\n    ========================================='
    print R+'     S H A R E D   D N S   H O S T N A M E S '
    print R+'    =========================================\n'
    print O+' [!] Looking up for name servers on which website is hosted...\n'+G
    time.sleep(0.7)
    system('dig +nocmd '+web+' ns +noall +answer')
    h = raw_input(O+'\n [*] Enter any DNS Server from above :> ') 
    time.sleep(0.4)
    print('' + GR + ' [!] Discovering hosts on same DNS Server...')
    time.sleep(0.4)
    print(""+ GR +" [~] Result: \n"+ color.END)
    domains = [h]
    for dom in domains:
        text = requests.get('http://api.hackertarget.com/findshareddns/?q=' + dom).text
	dns = str(text)
        if 'error' in dns:
	    print R+' [-] Outbound Query Exception!\n'
	    time.sleep(0.8)
	elif 'No results found' in dns:
	    print R+' [-] No shared DNS nameserver hosts...'
        else:
	    p = dns.splitlines()
	    for i in p:
		print O+' [+] Site found :> '+G+i
		time.sleep(0.02)


