#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import os
import sys
import subprocess
import re
import time
from colors import *

def check0x00(web):

	try:
	    print GR+' [*] Analysing responses...'
	    response = subprocess.check_output(["wafw00f", web])
	    if "is behind a" in response:
	    	regex = re.compile("is behind a(.*)")
	    	result = regex.findall(response)
		print G+' [+] The website seems to be behind a WAF...'
		print B+' [+] Firewall Detected : '+C+result[0].strip() 

	    else:
		print R+' [+] Seems like there is no publicly known firewall...'
		time.sleep(0.6)
		print R+' [-] No WAF detected!'
 
	except OSError as e:
	    if e.errno == os.errno.ENOENT:
	        print R+' [-] Unknown Exception Encountered!'
	        print R+' [-] Exception : '+str(e)

	except Exception as e:
	    print R+' [-] Unknown Exception Encountered!'
	    print R+' [-] Exception : '+str(e)

def waf(web):

	print GR+' [*] Loading module...'
	time.sleep(0.7)
	print R+'\n    ==========================='
	print R+'     W A F   D E T E C T I O N'
	print R+'    ===========================\n'
	time.sleep(0.7)
	print O+' [*] Testing the firewall/loadbalancer...'
	time.sleep(1)
	check0x00(web)

