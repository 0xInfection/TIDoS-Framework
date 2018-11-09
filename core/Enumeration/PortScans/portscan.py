#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This script is a part of TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import sys
import os
import time
import random
from random import *
from time import sleep
sys.path.append('modules/0x02-Scanning+Enumeration/0x01-PortScanning/')

from finscan import *
from servicedetect import *
#from nullscan import *
#from tcpack import *
from simpleport import *
from tcpconnectscan import *
from tcpstealthscan import *
#from tcpwindows import *
#from udpscan import *
from xmasscan import *
from core.Core.colors import *
from core.Enumeration.PortScans.portscanban import *

def portscan(web):

    time.sleep(0.3)
    print(W+' [!] Module Selected : Port Scanning')
    time.sleep(0.4)
    portscanban()
    v = raw_input (GR+'  [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)

    if v.strip() == '1':
        print(B+' [!] Module Selected :'+C+' Simple Port Scan')
        simpleport(web)
        time.sleep(1)
        portscan(web)

    elif v.strip() == '2':
        print(B+' [!] Module Selected :'+C+' TCP Connect Scan')
        tcpconnectscan(web)
        time.sleep(1)
        portscan(web)

#       elif v.strip() == '3':
#           print B+' [!] Module Selected :'+C+' TCP ACK Scan'
#           tcpack(web)
#           time.sleep(1)
#           portscan(web)

    elif v.strip() == '4':
        print(B+' [!] Module Selected :'+C+' TCP Stealth Scan')
        tcpstealthscan(web)
        time.sleep(1)
        portscan(web)

#       elif v.strip() == '5':
#           print B+' [!] Module Selected :'+C+' UDP Scan'
#           udpscan(web)
#           time.sleep(1)
#           portscan(web)

    elif v.strip() == '6':
        print(B+' [!] Module Selected :'+C+' XMAS Scan')
        xmasscan(web)
        time.sleep(1)
        portscan(web)

#       elif v.strip() == '7':
#           print B+' [!] Module Selected :'+C+' NULL Scan'
#           nullscan(web)
#           time.sleep(1)
#           portscan(web)

    elif v.strip() == '8':
        print(B+' [!] Module Selected :'+C+' FIN Scan')
        finscan(web)
        time.sleep(1)
        portscan(web)

    elif v.strip() == '9':
        print(B+' [!] Module Selected :'+C+' Service Detector')
        servicedetect(web)
        time.sleep(1)
        portscan(web)

#       elif v.strip() == '10':
#           print B+' [!] Module Selected :'+C+' TCP Windows'
#           tcpwindowsscan(web)
#           time.sleep(1)
#           portscan(web)

    elif v.strip() == 'A':
        print('\n [!] Module Automater Initialized...')
        sleep(0.5)
        print(B+' [*] Initializing Scan Type :'+C+' Simple Port Scan')
        simpleport(web)
        print(B+' [!] Scan Type Completed :'+C+' Simple Port Scan\n')
        sleep(0.5)
        print(B+' [!] Initializing Scan Type :'+C+' TCP Connect Scan')
        tcpconnectscan(web)
        print(B+' [!] Scan Type Completed :'+C+' TCP Connect\n')
        sleep(0.5)
#           print B+' [!] Initializing Scan Type :'+C+' TCP ACK Scan'
#           tcpack(web)
#           print B+' [!] Scan Type Completed :'+C+' TCP ACK Scan\n'
#           sleep(0.5)
        print(B+' [!] Initializing Scan Type :'+C+' TCP Stealth Scan')
        tcpstealthscan(web)
        print(B+' [!] Scan Type Completed :'+C+' TCP Stealth Scan\n')
        sleep(0.5)
#           print B+' [!] Initializing Scan Type :'+C+' UDP Scan'
#           udpscan(web)
#           print B+' [!] Scan Type Completed :'+C+' UDP Scan\n'
#           sleep(0.5)
        print(B+' [!] Initializing Scan Type :'+C+' XMAS Scan')
        xmasscan(web)
        print(B+' [!] Scan Type Completed :'+C+' XMAS Scan\n')
        sleep(0.5)
#           print B+' [!] Initializing Scan Type :'+C+' NULL Scan'
#           nullscan(web)
#           print B+' [!] Scan Type Completed :'+C+' NULL Scan\n'
#           sleep(0.5)
        print(B+' [!] Initializing Scan Type :'+C+' FIN Scan')
        finscan(web)
        print(B+' [!] Scan Type Completed :'+C+' FIN Scan\n')
        sleep(0.5)
        print(B+' [!] Initializing Scan Type :'+C+' Service Detection')
        servicedetect(web)
        print(B+' [!] Scan Type Completed :'+C+' Service Detection\n')
        sleep(0.5)
        print(B+' [!] All scantypes have been tested on target...')
        print(C+' [!] Going back to menu...')
        sleep(3)
        portscan(web)

    elif v.strip() == '99':
        print(GR+' [*] Going back...')
        time.sleep(0.5)
        os.system('clear')

    else:
        dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
        print(dope[randint(0,3)])
        time.sleep(0.7)
        portscan(web)
