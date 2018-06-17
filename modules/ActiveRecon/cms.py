#!/usr/bin/env python2
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import mechanize
import re
from re import *
import cookielib
import requests
import time
from time import sleep
from colors import *
import urllib2
from urllib2 import urlparse

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


def cms(web):

	print R+'\n   ========================='	
 	print R+'    C M S   D E T E C T O R'
	print R+'   =========================\n'
	time.sleep(0.4)
	print GR+' [*] Parsing the web URL... '
	time.sleep(0.4)
	if 'http' in web:
		domain = web
	else:
	    domain = web
	    try:
	        br.open('http://' + web)
	        web = 'http://' + web
	    except:
	        web = 'https://' + web
	print O+' [!] URL successfully parsed !'
	time.sleep(0.2)
	print GR+' [*] Looking up for the CMS the website is using...'
	time.sleep(1)
        result = br.open('https://whatcms.org/?s=' + domain).read()
        detect = search(r'">[^<]*</a><a href="/New-Detection', result)
        WordPress = False

        try:
            r = br.open(web + '/robots.txt').read()
            if "wp-admin" in str(r):
                WordPress = True
        except:
            pass

	try:
	    r = requests.get(web+'/wp-login.php')
	    if str(r.status_code) == '200':
	        WordPress = True
	    else:
		WordPress = False

	except Exception as e:
		print R+' [-] Exception handling failed!'
		print R+' [-] Error : '+str(e)

        if detect:
            print G+" [+] CMS Detected : " + detect.group().split('">')[1][:-27]
            detect = detect.group().split('">')[1][:-27]

        elif WordPress == True:
	    print O+' [!] Website seems to use Wordpress...'
	    time.sleep(0.2)
            print G+" [+] CMS Detected : WordPress"

        else:
            print R+" [-] "+O + domain+R + " doesn't seem to use a CMS"

