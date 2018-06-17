#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import sys, platform, subprocess, time, os
from random import randint
from subprocess import call
sys.path.append('modules/PassiveRecon/')

from dnschk import *
from passiveban import *
from piweb import *
from geoIP import *
from revip import *
from revdns import *
from subdom import *
from links import *
from footprint_dup import *
from googledorker import *
from googleSearch import *
from footprintban1 import *
from footprintban import *
from whoischeckup import *
from colors import *

def passiveo(web):

    print " [!] Module Selected : Passive Reconnaissance\n"
    passiveban()
    v = raw_input (''+GR+'  [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
    print '\n\n'
    if v == '1':
	print C+' [!] Type Selected '+B+': Ping Check'
	piweb(web)
	os.system('clear')
	time.sleep(1)
	passiveo(web)

    elif v == '2':
	print C+' [!] Type Selected '+B+': WhoIS Checkup'
	whoischeckup(web) 
	os.system('clear')
	time.sleep(1)
	passiveo(web)

    elif v == '3':
	print C+' [!] Type Selected '+B+': GeoIP Lookup'
	geoip(web)
	os.system('clear')
	time.sleep(1)
	passiveo(web)

    elif v == '4':
	print C+' [!] Type Selected '+B+': DNS Lookup'
	dnschk(web)
	os.system('clear')
	time.sleep(1)
	passiveo(web)

    elif v == '5':
	print C+' [!] Type Selected '+B+': Subdomain Scan'
	subdom(web)
	os.system('clear')
	time.sleep(1)
	passiveo(web)

    elif v == '6':
	print C+' [!] Type Selected '+B+': Reverse DNS Lookup'
	revdns(web)
	os.system('clear')
	time.sleep(1)
	passiveo(web)

    elif v == '7':
	print C+' [!] Type Selected '+B+': Reverse IP Lookup'
	revip(web)
	os.system('clear')
	time.sleep(1)
	passiveo(web)

    elif v == '8':
	print C+' [!] Type Selected '+B+': Page Links'
	links(web)
	os.system('clear')
	time.sleep(1)
	passiveo(web)

    elif v == '9':
	print C+' [!] Type Selected '+B+': Google Search'
	googleSearch()
	os.system('clear')
	time.sleep(1)
	passiveo(web)

    elif v == '10':
	print C+' [!] Type Selected '+B+': Google Dorker'
	googledorker(web)
	os.system('clear')
	time.sleep(1)
	passiveo(web)

    elif v == '99':
	print C+' [*] Back!'
	os.system('clear')
	footprintban1()
	footprint_dup(web)

    elif v == 'A':
	print C+' [!] Type Selected '+B+': All Modules\n'
	time.sleep(0.5)

	print C+' [*] Firing up module -->'+O+' Ping Check'
	piweb(web)
	print C+'\n [!] Module Completed -->'+O+' Piweb\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+O+' WHOIS '
	whoischeckup(web)
	print C+'\n [!] Module Completed -->'+O+' WHOIS\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+O+' GeoIP Lookup '
	geoIP(web)
	print C+'\n [!] Module Completed -->'+O+' GeoIP\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+O+' DNS Enumeration '
	dnschk(web)
	print C+'\n [!] Module Completed -->'+O+' DNS Enum\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+O+' Subdomain Scan '
	subdom(web)
	print C+'\n [!] Module Completed -->'+O+' Subdom\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+O+' Reverse DNS Lookup '
	revdns(web)
	print C+'\n [!] Module Completed -->'+O+' RevDNS\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+O+' Reverse IP Lookup '
	revip(web)
	print C+'\n [!] Module Completed -->'+O+' RevIP\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+O+' Web Links '
	links(web)
	print C+'\n [!] Module Completed -->'+O+' Web Links\n'
	time.sleep(1)

	print C+' [!] Firing up module -->'+O+' Google Search'
	googleSearch()
	print C+'\n [!] Module Completed -->'+O+' GSearch\n'
	time.sleep(1)

	print C+' [*] Firing up module -->'+O+' Google Dorker'
	googledorker(web)
	print C+'\n [!] Module Completed -->'+O+' GDorker\n'
	time.sleep(1)

	print G+' [+] All modules successfully completed!'
	time.sleep(3)
	print GR+' [*] Going back...'
	os.system('clear')
	footprintban1()
	footprint_dup(web)

    else:
	dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
	print dope[randint(0,3)] 
	os.system('clear')
	passiveo(web)

		
