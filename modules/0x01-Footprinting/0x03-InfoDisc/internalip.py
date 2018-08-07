#!/usr/bin/env python2
# coding: utf-8
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#
#
#Author : @_tID (theInfectedDrake)
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import re
import time
import requests
from colors import *

def internalip0x00(url):

    print R+'\n    ========================'
    print R+'     INTERNAL IP DISCLOSURE'
    print R+'    ========================\n'
    time.sleep(0.5)
    print GR+' [*] Making the request...'
    req = requests.get(url, verify=False)
    print O+' [*] Finding internal IP addresses...'
    time.sleep(0.5)
    print GR+' [*] Covering both IPv4 and IPv6 internal addresses...'
    time.sleep(0.8)
    search = re.findall(r'/(^127\.)|(^192\.168\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^::1$)|(^[fF][cCdD])/', req.content)
    if search:
    	for i in search:
        	print G+" [+] Internal IP found : "+O, str(i)
    else:
	print R+' [-] Nothing found... '

def internalip(web):

	print GR+' [*] Loading module...'
	time.sleep(0.6)
	internalip0x00(web)

