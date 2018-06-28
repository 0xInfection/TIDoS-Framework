#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import re
import mechanize
import socket
import cookielib
import subprocess
import time
from re import search
from colors import *

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

global flag
flag = 0x00

def osdetect(web):

    try:
	    time.sleep(0.4)
	    print R+'\n     ==================================='
	    print R+'      O S   F I N G E R P R I N T I N G'
	    print R+'     ===================================\n'
	    web = web.replace('http://','')
	    web = web.replace('https://','')
	    print GR+' [*] Initialising Module [1]...'
	    getos0x00(web)
	    print G+' [+] Module [1] Completed!'
	    if flag == True:
		q = raw_input(O+' [#] OS Identified!\n [#] Move on to to module [2]? (y/N) :> ')
		if q == 'Y'or q == 'y':
		    print GR+' [*] Initialising Module [2]...'
		    port0x00(web)
		elif q == 'N' or q == 'n':
		    print G+' [+] Done!'
	    elif flag == False:
		    print GR+' [*] Initialising Module [2]...'
		    port0x00(web)
	    else:
		print R+' [-] Fuck something went wrong!'
		print flag

    except Exception as e:
        print R+' [-] Unhandled Exception occured...'
	print R+' [-] Exception : '+str(e)
	pass

def getos0x00(web):

    ip_addr = socket.gethostbyname(web)
    print GR+' [*] Getting ip address...'
    time.sleep(0.7)
    print G+' [+] Website IP : ' +O+ str(ip_addr)
    time.sleep(0.5)
    print GR+' [*] Trying to identify operating system...'
    time.sleep(0.5)
    print O+' [!] Configuring requests...'
    result = br.open('https://www.censys.io/ipv4/%s/raw' % ip_addr).read()
    print GR+' [*] Getting raw data...'
    time.sleep(0.8)
    print R+' [*] Analysing responses...'
    try:
        match = search(r'&#34;os_description&#34;: &#34;[^<]*&#34;', result)
        if match:
	    flag = True
            print B+' [+] Operating System Identified : ' + C+ match.group().split('n&#34;: &#34;')[1][:-5]
	    
	else:
	    print R+' [-] No exact OS match for '+O+web+'...'
	    flag = False

    except Exception as e:
	print R+' [-] Unhandled Exception : '+str(e)
	     
def port0x00(web):

    time.sleep(0.7)
    print O+' [!] Moving on to the second phase...'
    time.sleep(0.8)
    print GR+' [*] Initiating port scan (TCP+UDP)...'
    response = subprocess.check_output(['nmap','-Pn','-O','-sSU','-F','--osscan-guess', web])
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

