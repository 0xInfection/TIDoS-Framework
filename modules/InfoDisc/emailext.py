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
    req = requests.get(url, verify=False)
    print O+' [*] Harvesting emails...'
    time.sleep(1)
    search = re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", req.content)
    for i in search:
        print G+" [+] E-mail found : "+O, str(i)

def emailext(web):

	print GR+' [*] Loading module...'
	time.sleep(0.6)
	mail0x00(web)

