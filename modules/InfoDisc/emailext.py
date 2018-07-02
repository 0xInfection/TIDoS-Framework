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
import sys
sys.path.append('files/')
import time
import requests
from colors import *

def mail0x00(url):

    print R+'\n    ======================'
    print R+'     EMAIl INFO HARVESTER'
    print R+'    ======================\n'
    time.sleep(0.5)
    print GR+' [*] Making the request...'
    req = requests.get(url, allow_redirects=False)
    print O+' [*] Harvesting emails...'
    time.sleep(1)
    text = req.text
    patron = re.compile("[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+")
    mails = re.findall(patron,text)
    for mail in mails:
	print G+' [+] Found : '+O+mail
    url0 = url+'/contact'
    q = requests.get(url0, allow_redirects=False)
    if str(q.status_code) == '200':
    	    print O+' [*] Harvesting emails from '+url0+'...'
	    text = q.text
	    patron = re.compile("[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+")
	    mails = re.findall(patron,text)
	    for mail in mails:
		print G+' [+] Found : '+O+mail
    else:
	pass

def emailext(web):

    try:
	print GR+' [*] Loading module...'
	time.sleep(0.6)
	mail0x00(web)
	print G+'\n [+] Done!\n'

    except Exception as e:
	print R+' [-] Exception Encountered!'
	print R+' [-] Error: '+str(e)
	pass
