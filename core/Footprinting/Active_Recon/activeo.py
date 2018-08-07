#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import sys
import os
import time
import subprocess
import random
from random import randint
sys.path.append('modules/0x01-Footprinting/0x02-ActiveRecon/')

from piwebenum import *
from grabhead import *
from httpmethods import *
from robot import *
from apachestat import *
from dav import *
from sharedns import *
from commentssrc import *
from sslcert import *
from activeban import *
from filebrute import *
from traceroute import *
from phpinfo import *
from cms import *
from serverdetect import *
from altsites import *
from colors import *

def activeo(web):

    print " [!] Module Selected : Active Reconnaissance\n\n"
    activeban()
    print ''
    time.sleep(0.3)
    v = raw_input (''+GR+'  [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
    print ''
    if v.strip() == '1':
	print C+' [!] Type Selected : Ping/NPing Enumeration'
	piwebenum(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '2':
	print C+' [!] Type Selected : Grab HTTP Headers'
	grabhead(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '3':
	print C+' [!] Type Selected : HTTP Allowed Methods'
	httpmethods(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '4':
	print C+' [!] Type Selected : robots.txt and sitemap.xml Hunt'
	robot(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '5':
	print C+' [!] Type Selected : Scrape Comments'
	commentssrc(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '6':
	print C+' [!] Type Selected '+B+': Traceroute'
	traceroute(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '7':
	print C+' [!] Type Selected : DNS Hosts'
	sharedns(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '8':
	print C+' [!] Type Selected : SSL Certificate'
	sslcert(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '9':
	print C+' [!] Type Selected : CMS Detection'
	cms(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '10':
	print C+' [!] Type Selected : Apache Status'
	apachestat(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '11':
	print C+' [!] Type Selected : WebDAV HTTP Enumeration'
	dav(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '12':
	print C+' [!] Type Selected : PHPInfo Enumeration'
	phpinfo(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '13':
	print C+' [!] Type Selected : Server Detection'
	serverdetect(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '14':
	print C+' [!] Type Selected : Alternate Sites '
	altsites(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == '15':
	print C+' [!] Type Selected : File Bruteforcers'
	filebrute(web)
	print '\n\n'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	activeo(web)

    elif v.strip() == 'A':
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

	print C+' [*] Firing up module -->'+B+' Comments Scraper'
	commentssrc(web)
	print C+'\n [!] Module Completed -->'+B+' Comments Src\n'
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

	print C+' [*] Firing up module -->'+B+' WebDAV HTTP Profiling'
	dav(web)
	print C+'\n [!] Module Completed -->'+B+' WebDAV HTTP Profiling\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+B+' Apache Status'
	apachestat(web)
	print C+'\n [!] Module Completed -->'+B+' Apache Status\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+B+' PHPInfo'
	phpinfo(web)
	print C+'\n [!] Module Completed -->'+B+' PHPInfo\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+B+' OS Fingerprinting'
	osdetect(web)
	print C+'\n [!] Module Completed -->'+B+' OS Detect\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+B+' File bruteforcer'
	filebrute(web)
	print C+'\n [!] Module Completed -->'+B+' File Bruteforcer\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+B+' Server Detection'
	serverdetect(web)
	print C+'\n [!] Module Completed -->'+B+' Server Detect\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+B+' Alt. Sites'
	altsites(web)
	print C+'\n [!] Module Completed -->'+B+' Alt. Sites\n'
	time.sleep(1)

	print C+'\n [!] All scantypes have been tested on target...'
	raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
	print C+' [*] Going back to menu...'
	time.sleep(3)
	os.system('clear')
	activeo(web)

    elif v.strip() == '99':
	print C+' [*] Back to the menu !'
	os.system('clear')

    else:
	dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
	print dope[randint(0,3)]
	time.sleep(0.7)
	os.system('clear')
	activeo(web)

