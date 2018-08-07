#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import sys
import socket
import time
import os
from colors import *

def inputin():

	try:
		web = raw_input(''+O+' [#] Target web address :> '+C+'')
		global web
		if 'http' not in str(web):
			mo = raw_input(GR+' [#] Does this website use SSL? (y/n) :> ')
			if mo == 'y' or mo == 'Y':
				web = 'https://'+web
			elif mo == 'n':
				web = 'http://'+web
		if 'http://' in web:
			po = web.replace('http://','')
		elif 'https://' in web:
			po = web.replace('https://','')
		if str(web).endswith('/'):
			web = po[:-1]
			po = po[:-1]
		print GR+' [*] Checking server status...'
		time.sleep(0.6)

		try:
			ip = socket.gethostbyname(po)
			print G+' [+] Site seems to be up...'
			time.sleep(0.5)
			print G+' [+] IP Detected : '+O+ip
			time.sleep(0.5)
			print ''
			os.system('cd tmp/logs/ && rm -rf '+po+'-logs && mkdir '+po+'-logs')
			return web

		except socket.gaierror:
			print R+' [-] Site seems to be down...'
			sys.exit(1)

	except KeyboardInterrupt:
		print R+' [-] Exiting...'
		time.sleep(0.7)
		print C+' [#] Alvida, my friend!'
		sys.exit(1)
	
