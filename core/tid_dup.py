#!/usr/bin/env python2

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This script is a part of TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import sys
import platform
import os
import subprocess
import logging
import time
import scapy
from scapy.all import *
from impo import *
from footprintban import *
from footprint import *
from scanenumban import *
from vulnban import *
from vuln import vuln
from exploitsban import *
from exploits import exploits
from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)

def tid_dup(web):

    while True:

        try:

	    dispmenu()
	    zop = raw_input(''+GR+' [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)

	    if zop == '1':

		print '\n'
        	print G+' [+] Module loaded : Reconnaissance'
        	footprintban()
		footprint(web)

	    elif zop == '2':

		print '\n'
	        print G+' [+] Module loaded : Scanning & Enumeration'
    		scanenumban()
		scanenum_dup(web)

	    elif zop == '3':

		print '\n'
		vulnban()
		vuln(web)

	    elif zop == '4':

		print '\n'
		exploitsban()
		exploits(web)
	
        except KeyboardInterrupt:
                print R+"\n [!] " + color.UNDERLINE+ "User Interruption detected!"+color.END
                print GR+' [!] Stopping jobs...'
		time.sleep(0.4)
		print C+' [!] Goodbye, see ya!\n'
		sys.exit(0)

	#except Exception as e:
		print R+' [-] Something happened! :('
		print R+' [!] Error : '+str(e)

