#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import sys, platform, subprocess, time, os
from subprocess import call
sys.path.append('modules/VulnLysis/SerioBugs')

from serbugsban import *
from lfi import *
from rfi import *
from rce import *
from csrf import *
from vulnban1 import *
from vuln_alt import vuln_alt
from sqli import *
from crlf import *
from hhi import *
from vulnban import *
from shellshock import *
from colors import *
#from xss import *
from openredirect import *
from pathtrav import * 

def serbugs(web):

      while True:
	    print GR+'\n [*] Type Selected : '+C+'Serious Web Vulnerabilities'
	    serbugsban()
	    v = raw_input(O+' \033[4mTID\033[1;0m '+GR+':> ' + color.END)
	    print ''
	    if v == '1':
		print C+' [!] Type Selected : LFI'
		lfi(web)
		time.sleep(2)	
		serbugs(web)

	    elif v == '2':
		print C+' [!] Type Selected : RFI'
		rfi(web)
		time.sleep(2)	
		serbugs(web)

	    elif v == '3':
		print C+' [!] Type Selected : RCE'
		rce(web)	
		time.sleep(2)	
		serbugs(web)

	    elif v == '4':
		print C+' [!] Type Selected : Path Traversal'
		pathtrav(web)	
		time.sleep(2)	
		serbugs(web)

	    elif v == '5':
		print C+' [!] Type Selected : CSRF'
		csrf(web)
		time.sleep(2)	
		serbugs(web)

	 #   elif v == '6':
	#	print C+' [!] Type Selected : XSS'
	#	xss(web)	
	#	time.sleep(2)	
	#	serbugs(web)

	    elif v == '7':
		print C+' [!] Type Selected : SQLi'
		sqli(web)	
		time.sleep(2)	
		serbugs(web)

	    elif v == '8':
		print C+' [!] Type Selected : HTTP Response Splitting'
		crlf(web)
		time.sleep(2)	
		serbugs(web)

	    elif v == '9':
		print C+' [!] Type Selected : Host Header Injection'
		hhi(web)	
		time.sleep(2)	
		serbugs(web)

	    elif v == '10':
		print C+' [!] Type Selected : Shellshock'
		shellshock(web)
		time.sleep(2)	
		serbugs(web)

	    elif v == '11':
		print C+' [!] Type Selected : URL Validation'
		redirect(web)
		time.sleep(2)	
		serbugs(web)

	    elif v == 'A':
		print ' [!] Type Selected : All Modules'
		time.sleep(0.5)

		print ' [*] Firing up module --> LFI'
		lfi(web)
		print ' [!] Module Completed --> LFI\n'
		time.sleep(1)

		print ' [*] Firing up module --> RFI '
		rfi(web)
		print ' [!] Module Completed --> RFI \n'
		time.sleep(1)

		print ' [*] Firing up module --> RCE'
		rce(web)
		print ' [!] Module Completed --> RCE\n'
		time.sleep(1)

		print ' [*] Firing up module --> Path Traversal'
		pathtrav(web)
		print ' [!] Module Completed --> Path Traversal\n'
		time.sleep(1)

		print ' [*] Firing up module --> CSRF'
	 	csrf(web)
		print ' [!] Module Completed --> CSRF\n'
		time.sleep(1)

	#	print ' [*] Firing up module --> XSS '
	#	xss(web)
	#	print ' [!] Module Completed --> XSS \n'
	#	time.sleep(1)

		print ' [*] Firing up module --> SQLi'
		sqli(web)
		print ' [!] Module Completed --> SQLi\n'
		time.sleep(1)

		print ' [*] Firing up module --> CRLF'
		crlf(web)
		print ' [!] Module Completed --> CRLF\n'
		time.sleep(1)

		print ' [*] Firing up module --> Host Header Injection'
		hhi(web)
		print ' [!] Module Completed --> Host Header Injection\n'
		time.sleep(0.5)

		print ' [*] Firing up module --> ShellShock'
		shellshock(web)
		print ' [!] Module Completed --> ShellShock\n'
		time.sleep(1)

		print ' [*] Firing up module --> URL Forwards'
		redirect(web)
		print ' [!] Module Completed --> Url Forwards\n'
		time.sleep(0.5)
		print G+' [+] All modules successfully completed!'
		time.sleep(4)
		vulnban1()
		vuln_alt(web)

	    elif v == '99':
		print '[!] Back'
		time.sleep(0.7)
		vulnban1()
		vuln_alt(web)

	    else:
		print ''
		dope = ['You high dude?','Hey there! Enter a valid option','Whoops! Thats not an option','Sorry fam! You just typed shit']
		print dope[randint(0,3)]
		time.sleep(0.7)
		os.system('clear')
		
		time.sleep(1)	
		serbugs(web)

