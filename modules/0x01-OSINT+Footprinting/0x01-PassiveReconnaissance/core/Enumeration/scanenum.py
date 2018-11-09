#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This script is a part of TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import sys
import time
import os
sys.path.append('modules/0x02-Scanning+Enumeration/')

from nmapmain import *
from webscan import *
from bannergrab import *
from osdetect import *
from webtech import *
from waf import *
from ssltlsscan import *
from core.Core.colors import *
from core.Enumeration.scanenumban import *
from core.Enumeration.Crawling.crawlers import *
from core.Enumeration.PortScans.portscan import *

def scanenum(web):

    print(B+' [+] Module Selected : '+C+'Scanning and Enumeation')
    scanenumban()
    v = raw_input(''+O+' \033[4mTID\033[1;0m '+GR+':> ' + color.END)
    print('\n')
    if v.strip() == '1':
        print(B+' [!] Type Selected :'+C+' WAF Analysis'+O)
        waf(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        scanenum(web)

    elif v.strip() == '2':
        print(B+' [!] Type Selected :'+C+' Port Scanning')
        portscan(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        scanenum(web)

    elif v.strip() == '3':
        print(B+' [!] Type Selected :'+C+' Interactive NMap')
        nmapmain(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        scanenum(web)

    elif v.strip() == '4':
        print(B+' [!] Type Selected :'+C+' WebTech Fingerprinting')
        webtech(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        scanenum(web)

    elif v.strip() == '5':
        print(B+' [!] Type Selected :'+C+' SSL Enumeration')
        ssltlsscan(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        scanenum(web)

    elif v.strip() == '6':
        print(B+' [!] Type Selected :'+C+' OS Fingerprinting')
        osdetect(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        scanenum(web)

    elif v.strip() == '7':
        print(B+' [!] Type Selected :'+C+' Banner Grab')
        bannergrab(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        scanenum(web)

    elif v.strip() == '8':
        print(B+' [!] Type Selected :'+C+' IP Crawler')
        webscan(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        scanenumban()
        scanenum(web)

    elif v.strip() == '9':
        print(B+' [!] Type Selected :'+C+' Web Crawlers')
        crawlers(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        scanenum(web)

    elif v.strip() == 'A':
        print(' [!] Type Selected : All Modules')
        time.sleep(0.5)

        print(B+' [*] Firing up module -->'+C+' WAF Analysis'+O)
        waf(web)
        print(B+' [!] Module Completed -->'+C+' WAF Analysis\n')
        time.sleep(1)

        print(B+' [*] Firing up module -->'+C+' Port Scanning ')
        portscan(web)
        print(B+' [!] Module Completed -->'+C+' Port Scanning \n')
        time.sleep(1)

        print(B+' [*] Firing up module -->'+C+' Interactive NMap')
        nmapmain(web)
        print(B+' [!] Module Completed -->'+C+' NMap\n')
        time.sleep(1)

        print(B + ' [*] Firing up module -->' + C + ' WebTech Fingerprinting')
        webtech(web)
        print(B + ' [!] Module Completed -->' + C + ' WebTech\n')
        time.sleep(1)

        print(B + ' [*] Firing up module -->' + C + ' SSL Enumeration')
        ssltlsscan(web)
        print(B + ' [!] Module Completed -->' + C + ' SSL Enumeration\n')
        time.sleep(1)

        print(B + ' [*] Firing up module -->' + C + ' OS Detect')
        osdetect(web)
        print(B + ' [!] Module Completed -->' + C + ' OS Detect\n')
        time.sleep(1)

        print(B + ' [*] Firing up module -->' + C + ' Banner Grabbing')
        bannergrab(web)
        print(B + ' [!] Module Completed -->' + C + ' Banner Grabbing\n')
        time.sleep(1)

        print(B + ' [*] Firing up module -->' + C + ' Webserver Scanning')
        webscan(web)
        print(B + ' [!] Module Completed -->' + C + ' Webserver Scanning\n')
        time.sleep(1)

        print(B+' [*] Firing up module -->'+C+' Crawlers')
        crawlers(web)
        print(B+' [!] Module Completed -->'+C+' Crawlers\n')
        time.sleep(0.5)

        print(G+' [+] All modules successfully completed!')
        time.sleep(0.5)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        print(GR+' [*] Going back...')

    elif v.strip() == '99':
        print('[!] Back')
        time.sleep(0.7)

    else:
        dope = ['You high dude?','Hey there! Enter a valid option','Whoops! Thats not an option','Sorry fam! You just typed shit']
        print(dope[randint(0,3)])
        time.sleep(0.7)
        os.system('clear')
        scanenum(web)
