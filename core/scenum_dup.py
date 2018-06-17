#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This script is a part of TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import sys
import subprocess
import time
import os
from subprocess import call
sys.path.append('modules/ScanEnum/')

from nmapmain import *
from crawlers import *
from colors import *
from scanenumban import *
from scanenumban1 import *
from portscan import *

def scenum_dup(web):
    v = raw_input('' + O + ' \x1b[4mTID\x1b[1;0m ' + GR + ':> ' + color.END)
    print '\n'
    if v == '1':
        print B + ' [!] Type Selected :' + C + ' WAF Analysis'
        os.system('wafw00f ' + web)
        time.sleep(0.9)
        scanenumban1()
        scenum_dup(web)
    elif v == '2':
        print B + ' [!] Type Selected :' + C + ' Port Scanning'
        portscan(web)
        time.sleep(0.9)
        scanenumban1()
        scenum_dup(web)
    elif v == '3':
        print B + ' [!] Type Selected :' + C + ' Interactive NMap'
        nmapmain(web)
        time.sleep(0.9)
        scanenumban1()
        scenum_dup(web)
    elif v == '4':
        print B + ' [!] Type Selected :' + C + ' Crawlers'
        crawlers(web)
        time.sleep(0.9)
        scanenumban1()
        scenum_dup(web)
    elif v == 'A':
        print ' [!] Type Selected : All Modules'
        time.sleep(0.5)
        print B + ' [*] Firing up module -->' + C + ' WAF Analysis'
        os.system('wafw00f ' + web)
        print B + ' [!] Module Completed -->' + C + ' WAF Analysis\n'
        time.sleep(1)
        print B + ' [*] Firing up module -->' + C + ' Port Scanning '
        portscan(web)
        print B + ' [!] Module Completed -->' + C + ' Port Scanning \n'
        time.sleep(1)
        print B + ' [*] Firing up module -->' + C + ' Interactive NMap'
        nmapmain(web)
        print B + ' [!] Module Completed -->' + C + ' NMap\n'
        time.sleep(1)
        print B + ' [*] Firing up module -->' + C + ' Crawlers'
        crawlers(web)
        print B + ' [!] Module Completed -->' + C + ' Crawlers\n'
        time.sleep(0.5)
        print G + ' [+] All modules successfully completed!'
        time.sleep(0.5)
        print GR + ' [*] Going back...'
    elif v == '99':
        print '[!] Back'
        time.sleep(0.7)
    else:
        dope = ['You high dude?',
         'Hey there! Enter a valid option',
         'Whoops! Thats not an option',
         'Sorry fam! You just typed shit']
        print dope[randint(0, 3)]
        time.sleep(0.7)
        os.system('clear')
        scanenumban1()
        scenum_dup(web)

