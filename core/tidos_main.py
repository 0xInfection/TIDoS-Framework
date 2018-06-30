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
from os import path
from time import sleep
from impo import *
from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)
warnings.filterwarnings("ignore")

global vuln
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

	print O+' [+] Okay, so what to start with?\n'
	def tidosmain(web):

	    while True:
		try:
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

		    elif zop == '99':
			
			print R+'\n [-] Exiting...'
			time.sleep(0.5)
			print O+' [+] Goodluck mate, alvida!\n'
			sys.exit(0)
		
		except KeyboardInterrupt:
		        print R+"\n [-] " + color.UNDERLINE+ "User Interruption detected!"+color.END
		        print GR+' [!] Stopping jobs...'
			time.sleep(0.4)
			print C+' [+] Alvida, see ya!\n'
			sys.exit(0)

		except Exception:
			pass

	tidosmain(web)
