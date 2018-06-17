#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import re
import sys
sys.path.append('files/')
import time
import requests
from colors import *

def credit0x00(url):

    print R+'\n     ========================'
    print R+'      CREDIT CARD DISCLOSURE'
    print R+'     ========================\n'

    print O+' [*] Making the request...'
    req = requests.get(url, verify=False)
    req_read = str(req).split()
    print GR+' [*] Reading response...'
    time.sleep(1)
    append_name = str("".join(req_read))
    AMEX = re.match(r"^3[47][0-9]{13}$", append_name)
    VISA = re.match(r"^4[0-9]{12}(?:[0-9]{3})?$", append_name)
    MASTERCARD = re.match(r'^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$', append_name)
    DISCOVER = re.match(r"^6(?:011|5[0-9]{2})[0-9]{12}$", append_name)
    EXPRESS = re.match(r'^[34|37][0-9]{14}$', append_name)
    VISA_MASTERCARD = re.match(r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})$', append_name)

    try:
	print GR+' [*] Trying to find out existing American Express Cards...'
	time.sleep(1)
        if EXPRESS.group():
            print G+" [+] Website has American Express Cards!"
            print O+' [!] Card : ' + GR+EXPRESS.group()

    except:
        print R+" [-] No American Express Cards found!"

    try:
	print GR+' [*] Trying to find out existing Visa-Master Cards...'
	time.sleep(1)
        if VISA_MASTERCARD.group():
            print G+" [+] Website has a Visa-Master Card!"
            print O+' [!] Card : ' + GR+VISA_MASTERCARD.group()

    except:
        print R+" [-] No Visa-MasterCard found!"

    try:
	print GR+' [*] Trying to find out existing MasterCards...'
	time.sleep(1)
        if MASTERCARD.group():
            print G+" [+] Website has a Master Card!"
            print O+' [!] Card : ' + GR+MASTERCARD.group()

    except:
        print R+" [-] No MasterCard found!"

    try:
	print GR+' [*] Trying to find out existing VISA credit cards...'
	time.sleep(1)
        if VISA.group():
            print G+" [+] Website has a VISA card!"
            print O+' [!] Card : ' + GR+VISA.group()

    except:
        print R+" [-] No VISA Cards found!"

    try:
	print GR+' [*] Trying to find out existing AMEX Cards...'
	time.sleep(1)
        if AMEX.group():
            print G+" [+] Website has a AMEX card!"
            print O+' [!] Card : ' + GR+AMEX.group()

    except:
        print R+" [-] No Amex Cards found!"

    try:
	print GR+' [*] Trying to find out existing Discover Cards...'
	time.sleep(1)
        if DISCOVER.group():
            print G+" [+] Website has a DISCOVER card!"
            print O+' [!] Card : ' + GR+DISCOVER.group()

    except:
        print R+" [-] No Discover Cards found!"

def credit(web):
	
	print GR+' [*] Initiating module...'
	time.sleep(0.5)
	credit0x00(web)

