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

def osdetect(web):

    time.sleep(0.4)
    print R+'\n      =================================='
    print R+'      O S   F I N G E R P R I N T I N G'
    print R+'     ===================================\n'
    web = web.replace('http://','')
    web = web.replace('https://','')
    ip_addr = socket.gethostbyname(web)
    print G+' [+] Website IP : ' + str(ip_addr)
    time.sleep(0.5)
    print GR+' [*] Trying to identify operating system...'
    time.sleep(0.5)
    try:
        result = br.open('https://www.censys.io/ipv4/%s/raw' % ip_addr).read()
        match = search(r'&#34;os_description&#34;: &#34;[^<]*&#34;', result)
        if match:
            print G+' [+] Operating System Identified : ' + O + match.group().split('n&#34;: &#34;')[1][:-5]
	else:
	    print R+' [-] Could not identify OS...'
    except Exception as e:
        print R+' [-] Some error occured.'
	print R+' [-] Error : '+str(e)
	pass

