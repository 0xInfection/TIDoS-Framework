#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import re
import mechanize
import socket
import cookielib
import subprocess
import time
from re import search
from getports import *
from colors import *
from getcensys import getos0x00

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [
    ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	     
def port0x00(web):

    time.sleep(0.7)
    print O+' [!] Moving on to the second phase...'
    time.sleep(0.8)
    print O+' [*] Initiating port scan (TCP+UDP)...'

    try:
	getports(web)

    except Exception as e:
	print R+' [-] Exception : '+str(e)

    print GR+' [*] Initiating OS detection response analysis...'
    response = subprocess.check_output(['nmap','-Pn','-O','-sSU','-F','--osscan-guess','-T4', web])
    if "No OS matches for host".lower() not in response.lower():
	if 'running:' in response.lower():
	    	regex = re.compile("Running:(.*)")
	    	result = regex.findall(response)
		print C+' [+] OS Running Matched : '+B+result[0].strip()

	if 'os cpe:' in response.lower():
	    	regex = re.compile("OS CPE:(.*)")
	    	result = regex.findall(response)
		print C+' [+] OS CPE Detected : '+B+result[0].strip() 

	if 'os details:' in response.lower():
	    	regex = re.compile("OS details:(.*)")
	    	result = regex.findall(response)
		print C+' [+] Operating System Details : '+B+result[0].strip() 
    else:
	print R+' [-] No exact matches for OS via port scan...'
    print G+' [+] Done!'

def osdetect(web):

    try:
	    time.sleep(0.4)
	    print R+'\n     ==================================='
	    print R+'      O S   F I N G E R P R I N T I N G'
	    print R+'     ===================================\n'
	    web = web.replace('http://','')
	    web = web.replace('https://','')
	    print GR+' [*] Initialising Module [1]...'
	    fl = getos0x00(web)
	    print G+'\n [+] Module [1] Completed!'
	    if flag == 0x01:
		q = raw_input(O+' [#] OS Identified!\n [#] Move on to to module [2]? (y/N) :> ')
		if q == 'Y'or q == 'y':
		    print GR+'\n [*] Initialising Module [2]...'
		    port0x00(web)
		elif q == 'N' or q == 'n':
		    print G+' [+] Done!'
	    elif flag == 0x00:
		    print GR+' [*] Initialising Module [2]...'
		    port0x00(web)
	    else:
		print R+' [-] Fuck, something went wrong!'
		print flag

    except Exception as e:
        print R+' [-] Unhandled Exception occured...'
	print R+' [-] Exception : '+str(e)
	pass

