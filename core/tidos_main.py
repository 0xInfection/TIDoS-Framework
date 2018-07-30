#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS

import sys
import platform
import os
import time
import warnings
from random import randint
from os import path
from time import sleep
from impo import *
from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)
warnings.filterwarnings("ignore")

def tidos_main():

	try:
		agree()
		loadstyle()
		tid()
		banner()
		banner1()
		web = inputin()
	except Exception as e:
		print R+' [-] Exception encountered!'
		print R+' [-] Exception : '+str(e)
		sys.exit(1)

	print P+' [+] Okay, so what to start with?'
	time.sleep(1)
	def tidosmain(web):

	    while True:
		try:
		    os.system('clear')
		    dispmenu()
		    zop = raw_input(''+GR+' [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
		    zop = zop.strip()

		    if zop == '1':

			print G+"\n [+] Module loaded : Reconnaissance"
			footprintban()
			footprint(web)

		    elif zop == '2':

			print G+'\n [+] Module loaded : Scanning & Enumeration'
	    		scanenumban()
			scanenum(web)

		    elif zop == '3':

			print G+'\n [+] Module loaded : Vulnerability Analysis'
			vulnban()
			vuln(web)

		    elif zop == '4':

			print G+'\n [+] Module loaded : Exploits Castle'
			exploitsban()
			exploits(web)

		    elif zop == '5':

			print G+'\n [+] Module loaded : Auxillaries'
			auxilban()
			auxil(web)

		    elif zop == '99':
			
			print R+'\n [-] Exiting...'
			time.sleep(0.6)
			print O+' [+] Goodluck mate, Alvida!\n'
			sys.exit(0)

		    else:
        		dope = ['You high dude?', 'Sorry fam! You just typed shit']
        		print R+' [-] ' + dope[randint(0,1)]
			time.sleep(0.5)
			pass
		
		except KeyboardInterrupt:
		        print R+"\n [-] " + color.UNDERLINE+ "User Interruption detected!"+color.END
		        print GR+' [!] Stopping jobs...'
			time.sleep(0.4)
			print C+' [+] Alvida, see ya!\n'
			sys.exit(0)

		#except Exception:
			pass

	tidosmain(web)
