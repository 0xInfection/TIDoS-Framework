#!/usr/bin/env python2
# -*- coding : utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import requests
import mechanize
import cookielib
from urllib2 import urlparse
import time
from time import sleep
from colors import *

br = mechanize.Browser()

cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [
    ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

linksall = []
cis = []
crawled = []

def crawler10x00(web):

	time.sleep(0.5)
	print R+'\n    ==========================='
	print R+'     C R A W L E R  (Depth 1)'
	print R+'    ==========================\n'
	print O+' [This module will fetch all links'
	print O+' from an online API and then crawl '
	print O+'         them one by one]	'
	time.sleep(0.4)
	print ''+GR+' [*] Parsing the web URL... '
	time.sleep(0.3)
	print '' +B+ ' [!] URL successfully parsed...'
        print('' + GR+ ' [*] Getting links...')
        time.sleep(0.4)
        text = requests.get('http://api.hackertarget.com/pagelinks/?q=' + web).text
        lol = str(text)
        linksall = lol.splitlines()
        for m in linksall:
	    if 'http' in m and 'https' not in m:
	        cis.append(m)
	try:
            for x in cis:
            	print ''+G+' [+] Crawling link :> '+ O + str(x)
	    	br.open(x)
	    	crawled.append(x)	

	except Exception as e:
	    print R+' [!] Exception encountered!'
	    print R+' [-] Error : '+str(e)+'\n'
	    print O+' [+] Please use the second crawler... :)'

	return crawled

def out(web, list0):
	
	web = web.replace('http://','')
	web = web.replace('https://','')
	print GR+' [*] Writing found URLs to a file...'
	fil = open('tmp/'+web+'-links.lst','w+')
	for lists in list0:
	    if str(web) in lists:
		fil.write("%s\n" % lists)

def crawler1(web):

	print GR+' [*] Loading crawler...'
	time.sleep(0.5)
	q = crawler10x00(web)
	out(web, q)
	print G+' [+] Done!'

