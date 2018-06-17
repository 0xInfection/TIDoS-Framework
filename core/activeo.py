#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import sys
import os
import time
import subprocess
import random
from random import randint
sys.path.append('modules/ActiveRecon/')

from piwebenum import *
from grabhead import *
from robot import *
from sharedns import *
from subnet import *
from sslcert import *
from activeban import *
from traceroute import *
from footprint import *
from footprintban import *
from footprintban1 import *
from cms import *
from serverdetect import *
from osdetect import *
from colors import *

def activeo(web):

    print " [!] Module Selected : Active Reconnaissance\n\n"
    activeban()
    print ''
    time.sleep(0.3)
    v = raw_input (''+GR+'  [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
    print ''
    if v == '1':
	print C+' [!] Type Selected : Ping/NPing Enumeration'
	piwebenum(web)
	print '\n\n'
	os.system('clear')
	time.sleep(1)
	activeo(web)

    elif v == '2':
	print C+' [!] Type Selected : Grab HTTP Headers'
	grabhead(web)
	print '\n\n'
	os.system('clear')
	time.sleep(1)
	activeo(web)

    elif v == '3':
	print C+' [!] Type Selected : robots.txt and sitemap.xml Hunt'
	robot(web)
	print '\n\n'
	os.system('clear')
	time.sleep(1)
	activeo(web)

    elif v == '4':
	print C+' [!] Type Selected : Subnet Enumeration'
	subnet(web)
	print '\n\n'
	os.system('clear')
	time.sleep(1)
	activeo(web)

    elif v == '5':
	print C+' [!] Type Selected '+B+': Traceroute'
	traceroute(web)
	print '\n\n'
	os.system('clear')
	time.sleep(1)
	activeo(web)

    elif v == '6':
	print C+' [!] Type Selected : DNS Hosts'
	sharedns(web)
	print '\n\n'
	os.system('clear')
	time.sleep(1)
	activeo(web)

    elif v == '7':
	print C+' [!] Type Selected : SSL Certificate'
	sslcert(web)
	print '\n\n'
	os.system('clear')
	time.sleep(1)
	activeo(web)

    elif v == '8':
	print C+' [!] Type Selected : CMS Detection'
	cms(web)
	print '\n\n'
	os.system('clear')
	time.sleep(1)
	activeo(web)

    elif v == '9':
	print C+' [!] Type Selected : Server Detection'
	serverdetect(web)
	print '\n\n'
	os.system('clear')
	time.sleep(1)
	activeo(web)

    elif v == '10':
	print C+' [!] Type Selected : Operating System Fingerprinting'
	osdetect(web)
	print '\n\n'
	os.system('clear')
	time.sleep(1)
	activeo(web)

    elif v == 'A':
	print C+' [!] Type Selected : All Modules'
	time.sleep(0.5)
	print C+' [*] Firing up module -->'+B+' Ping Enum'
	piwebenum(web)
	print C+' [!] Module Completed -->'+B+' PIng\n'

	time.sleep(1)
	print C+' [*] Firing up module -->'+B+' Grab Headers'
	grabhead(web)
	print C+'\n [!] Module Completed -->'+B+' Grabhead\n'
	
	time.sleep(1)
	print C+' [*] Firing up module -->'+B+' Robots.txt Hunter'
	robot(web)
	print C+'\n [!] Module Completed -->'+B+' Robot Hunter\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+B+' Subnet Enumeration'
	subnet(web)
	print C+'\n [!] Module Completed -->'+B+' Subnet Enumeration\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+B+' Traceroute'
	traceroute(web)
	print C+'\n [!] Module Completed -->'+B+' Traceroute\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+B+' Shared DNS Servers'
	sharedns(web)
	print C+'\n [!] Module Completed -->'+B+' Shared DNS Servers\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+B+' SSl Certificate Info'
	sslcert(web)
	print C+'\n [!] Module Completed -->'+B+' SSl Cert\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+B+' CMS Detection'
	cms(web)
	print C+'\n [!] Module Completed -->'+B+' CMS Detect\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+B+' Server Detection'
	serverdetect(web)
	print C+'\n [!] Module Completed -->'+B+' Server Detect\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+B+' OS Fingerprinting'
	osdetect(web)
	print C+'\n [!] Module Completed -->'+B+' OS Detect\n'
	time.sleep(1)

	print C+'\n [!] All scantypes have been tested on target...'
	time.sleep(2)
	print C+' [*] Going back to menu...'
	time.sleep(3)
	os.system('clear')
	footprintban1()
	footprint(web)

    elif v == '99':
	print C+' [*] Back to the menu !'
	os.system('clear')
	footprintban1()
	footprint(web) 

    else:
	dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
	print dope[randint(0,3)]
	time.sleep(0.7)
	os.system('clear')
	activeo(web)

