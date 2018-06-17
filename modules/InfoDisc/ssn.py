#!/usr/bin/env python2
# coding: utf-8
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#
#
#Author : @_tID (the-Infected-Drake)
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import re
import sys
sys.path.append('files/')
import time
import requests
from colors import *

def ssn0x00(url):

    print R+'\n    ================================='
    print R+'     SOCIAL SECURITY INFO DISCLOSURE'
    print R+'    =================================\n'
    time.sleep(0.5)
    print GR+' [*] Making the request...'
    req = requests.get(url, verify=False)
    print O+' [*] Final social security numbers...'
    time.sleep(0.5)
    search = re.findall(r'(((?!000)(?!666)(?:[0-6]\d{2}|7[0-2][0-9]|73[0-3]|7[5-6][0-9]|77[0-2]))-((?!00)\d{2})-((?!0000)\d{4}))', req.content)

    for i in search:
        print G+" [+] US Social Security Number found : "+O, str(i)

def ssn(web):

	print GR+' [*] Loading module...'
	time.sleep(0.6)
	ssn0x00(web)
