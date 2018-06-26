#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This script is a part of TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import sys
import platform
import os
import time
import random
import subprocess
from random import *
from time import sleep
sys.path.append('modules/ScanEnum/')

from finscan import *
from servicedetect import *
#from nullscan import *
#from tcpack import *
from simpleport import *
from scanenumban1 import *
from tcpconnectscan import *
from tcpstealthscan import *
from scanenumban import *
#from tcpwindows import *
#from udpscan import *
from xmasscan import *
from colors import *
from scenum_dup import scenum_dup
from portscanban import *

def portscan(web):

	time.sleep(0.3)
	print W+' [!] Module Selected : Port Scanning'
	time.sleep(0.4)
	portscanban() 
	v = raw_input(O+' [#] TID :> ')

	if v == '1':
	    print B+' [!] Module Selected :'+C+' Simple Port Scan'
	    simpleport(web)
	    time.sleep(1)
	    portscan(web)

	elif v == '2':
	    print B+' [!] Module Selected :'+C+' TCP Connect Scan'
	    tcpconnectscan(web)
	    time.sleep(1)
	    portscan(web)

#	elif v == '3':
#	    print B+' [!] Module Selected :'+C+' TCP ACK Scan'
#	    tcpack(web)
#	    time.sleep(1)
#	    portscan(web)

	elif v == '4':
	    print B+' [!] Module Selected :'+C+' TCP Stealth Scan'
	    tcpstealthscan(web)
	    time.sleep(1)
	    portscan(web)

#	elif v == '5':
#	    print B+' [!] Module Selected :'+C+' UDP Scan'
#	    udpscan(web)
#	    time.sleep(1)
#	    portscan(web)

	elif v == '6':
	    print B+' [!] Module Selected :'+C+' XMAS Scan'
	    xmasscan(web)
	    time.sleep(1)
	    portscan(web)

#	elif v == '7':
#	    print B+' [!] Module Selected :'+C+' NULL Scan'
#	    nullscan(web)
#	    time.sleep(1)
#	    portscan(web)

	elif v == '8':
	    print B+' [!] Module Selected :'+C+' FIN Scan'
	    finscan(web)
	    time.sleep(1)
	    portscan(web)

	elif v == '9':
	    print B+' [!] Module Selected :'+C+' Service Detector'
	    servicedetect(web)
	    time.sleep(1)
	    portscan(web)

#	elif v == '10':
#	    print B+' [!] Module Selected :'+C+' TCP Windows'
#	    tcpwindowsscan(web)
#	    time.sleep(1)
#	    portscan(web)

	elif v == 'A':
	    print '\n [!] Module Automater Initialized...'
	    sleep(0.5)
	    print B+' [*] Initializing Scan Type :'+C+' Simple Port Scan'
	    simpleport(web)
	    print B+' [!] Scan Type Completed :'+C+' Simple Port Scan\n'
	    sleep(0.5)
	    print B+' [!] Initializing Scan Type :'+C+' TCP Connect Scan'
	    tcpconnectscan(web)
	    print B+' [!] Scan Type Completed :'+C+' TCP Connect\n'
	    sleep(0.5)
#	    print B+' [!] Initializing Scan Type :'+C+' TCP ACK Scan'
#	    tcpack(web)
#	    print B+' [!] Scan Type Completed :'+C+' TCP ACK Scan\n'
#	    sleep(0.5)
	    print B+' [!] Initializing Scan Type :'+C+' TCP Stealth Scan'
	    tcpstealthscan(web)
	    print B+' [!] Scan Type Completed :'+C+' TCP Stealth Scan\n'
	    sleep(0.5)
#	    print B+' [!] Initializing Scan Type :'+C+' UDP Scan'
#	    udpscan(web)
#	    print B+' [!] Scan Type Completed :'+C+' UDP Scan\n'
#	    sleep(0.5)
	    print B+' [!] Initializing Scan Type :'+C+' XMAS Scan'
	    xmasscan(web)
	    print B+' [!] Scan Type Completed :'+C+' XMAS Scan\n'
	    sleep(0.5)
#	    print B+' [!] Initializing Scan Type :'+C+' NULL Scan'
#	    nullscan(web)
#	    print B+' [!] Scan Type Completed :'+C+' NULL Scan\n'
#	    sleep(0.5)
	    print B+' [!] Initializing Scan Type :'+C+' FIN Scan'
	    finscan(web)
	    print B+' [!] Scan Type Completed :'+C+' FIN Scan\n'
	    sleep(0.5)
	    print B+' [!] Initializing Scan Type :'+C+' Service Detection'
	    servicedetect(web)
	    print B+' [!] Scan Type Completed :'+C+' Service Detection\n'
	    sleep(0.5)
	    print B+' [!] All scantypes have been tested on target...'
	    sleep(2)
	    print C+' [!] Going back to menu...'
	    sleep(3)
	    scanenumban1()
	    scenum_dup(web)

	elif v == '99':
	    print GR+' [*] Going back...'
	    scanenumban1()
	    time.sleep(0.5)
	    scenum_dup(web) 

	else:
	    dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
	    print dope[randint(0,3)]
	    time.sleep(0.7)
	    portscan(web)

