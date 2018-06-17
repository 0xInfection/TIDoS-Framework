#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import re
import sys
sys.path.append('files/')
import time
import requests
from colors import *
from re import search
from error_patterns import patterns

def error0x00(content,url):

	for pattern in patterns:
		print C+' [!] Finding '+B+pattern+C+' ...'
		time.sleep(0.2)
		if search(pattern, content):
			print G+' [!] Possible error at '+O+url
			print G+" [+] Found : \"%s\" at %s" % (pattern,url)

def request(web):

	req = requests.get(web, verify=False)
	print GR+' [*] Parsing the content...'
	m = req.content
	error0x00(m,web)

def errors(web):

	print R+'\n       ========================='
	print R+'        E R R O R   H U N T E R '
	print R+'       ========================='
	print O+'   [This module covers up Full Path Disclosures]\n'
	print GR+' [*] Making the request...'
	time.sleep(0.5)
	request(web)

