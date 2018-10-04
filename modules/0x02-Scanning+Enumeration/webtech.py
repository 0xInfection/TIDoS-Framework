#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework

from __future__ import print_function
import builtwith
import json
from bs4 import BeautifulSoup
import time
import requests
from colors import *

def check0x00(domain):

       	print(O+" [+] Domain : "+GR+domain) 
	print(B+' [*] Fingerprinting web technologies...') 
       	resp = builtwith.parse(domain)
	print(O+' [*] Parsing raw-data...')
	time.sleep(0.7)
       	res = json.dumps(resp)
	r = json.loads(res)
	print(G+' [+] Result : \n')
	try:

		if "cdn" in r:
			print(G+' [+] Content Delivery Network:')
			for p in r["cdn"]:
				print(C+'      '+p)
			print('')
			time.sleep(0.7)

		if "font-scripts" in r:
			print(G+' [+] Font-Script Source:')
			for p in r["font-scripts"]:
				print(C+'      '+p)
			print('')
			time.sleep(0.7)

		if "widgets" in r:
			print(G+' [+] Widgets:')
			for p in r["widgets"]:
				print(C+'      '+p)
			print('')
			time.sleep(0.7)

		if "web-frameworks" in r:
			print(G+' [+] Web Frameworks:')
			for p in r["web-frameworks"]:
				print(C+'      '+p)
			print('')
			time.sleep(0.7)

		if "programming-languages" in r:
			print(G+' [+] Front-End Programming Languages:')
			for p in r["programming-languages"]:
				print(C+'      '+p)
			print('')
			time.sleep(0.7)

		if "marketing-automation" in r:
			print(G+' [+] Marketing Automation Source:')
			for p in r["marketing-automation"]:
				print(C+'      '+p)
			print('')
			time.sleep(0.7)

		if "mobile-frameworks" in r:
			print(G+' [+] Mobile Frameworks:')
			for p in r["mobile-frameworks"]:
				print(C+'      '+p)
			print('')
			time.sleep(0.7)

		if "video-players" in r:
			print(G+' [+] In-Built Video Players:')
			for p in r["video-players"]:
				print(C+'      '+p)
			print('')
			time.sleep(0.7)

	except Exception as e:
		print(R+' [-] Exception : '+str(e))

def apircv(web):

	try:
		domain = web.replace('http://','')
		domain = web.replace('https://','')
		html = requests.get('http://w3techs.com/siteinfo.html?fx=y&url=' + domain).text
		soup = BeautifulSoup(html, 'lxml')
		table = soup.findAll('table', attrs={'class':'w3t_t'})[0]
		trs = table.findAll('tr')

		for tr in trs:
			th = tr.find('th')
			td = tr.find('td').text
			
			if td[-7:] == 'more...':
				td = td[:-9]
			
			print(G+' [+] '+th.text+': ')
			print(C+'      '+td+'\n')
			time.sleep(0.7)
	except:
		print(R+' [-] Outbound Query Exception!')

def webtech(web):

    	print(R+'\n    =================================')
    	print(R+'     W E B   T E C H N O L O G I E S')
    	print(R+'    =================================\n')

    	check0x00(web)
	apircv(web)
	print(O+' [+] Fingerprinting Done!')

