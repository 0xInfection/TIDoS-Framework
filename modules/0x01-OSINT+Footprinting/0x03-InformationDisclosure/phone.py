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

from __future__ import print_function
import re
import sys
sys.path.append('files/')
import time
import requests
from colors import *

def phone0x00(url):

    print(R+'\n    ========================')
    print(R+'     PHON3 NuMBER HARVESTER')
    print(R+'    ========================\n')
    time.sleep(0.5)
    print(GR+' [*] Making the request...')
    req = requests.get(url, verify=False)
    print(O+' [*] Harvesting phone numbers...')
    time.sleep(0.5)
    search = re.findall(r"\+\d{2}\s?0?\d{10}", req.content)
    for i in search:
        print(G+" [+] Phone found : "+O, str(i))

def phone(web):

	print(GR+' [*] Loading module...')
	time.sleep(0.6)
	phone0x00(web)
