#!/usr/bin/env python2
# -*- coding : utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This script is a part of TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import sys
import platform
import os
import time
import random
import subprocess
from random import *
sys.path.append('modules/ScanEnum/')

from crawler1 import *
from crawler2 import *
from crawler3 import *
from scanenum_dup import scanenum_dup
from scanenumban1 import *
from crawlersban import *
from colors import *

def crawlers_hunt(web):

	time.sleep(0.3)
	print ' [!] Module Selected : Crawlers'
	time.sleep(0.4)
	crawlersban() 
	v = raw_input(O+' [#] TID :> ')
	if v.strip() == '1':
	    print B+' [!] Module Selected :'+C+' Crawler (Depth 1)'
	    crawler1(web)
	    time.sleep(1)
	    crawlers_hunt(web)

	elif v.strip() == '2':
	    print B+' [!] Module Selected :'+C+' Crawler (Depth 2)'
	    crawler2(web)
	    time.sleep(1)
	    crawlers_hunt(web)

	elif v.strip() == '3':
	    print B+' [!] Module Selected :'+C+' Crawler (Depth 3)'
	    crawler3(web)
	    time.sleep(1)
	    crawlers_hunt(web)

	elif v.strip() == '99':
	    print GR+'\n [*] Back...'
	    scanenumban1()
	    scanenum_dup(web)

	elif v.strip() == 'A':
	    print W+'\n [!] Module Automater Initialized...'
	    sleep(0.5)
	    print B+' [*] Initializing Scan Type :'+C+' Crawler (depth 1)'
	    crawler1(web)
	    print B+'\n [!] Scan Type Completed :'+C+' Crawler 1\n'
	    sleep(0.5)
	    print B+' [!] Initializing Scan Type :'+C+' Crawler (depth 2)'
	    crawler2(web)
	    print B+'\n [!] Scan Type Completed :'+C+' Crawler 2\n'
        	
	    print B+' [!] Initializing Scan Type :'+C+' Crawler (Depth 3)'
	    crawler3(web)
	    print B+'\n [!] Scan Type Completed :'+C+' Crawler 3\n'
	    print G+' [+] All modules successfully completed!'
	    sleep(2)
	    scanenumban1()

	else:
	    dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
	    print dope[randint(0,3)]
	    sleep(1)
	    crawlers_hunt(web)
