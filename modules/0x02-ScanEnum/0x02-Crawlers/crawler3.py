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
import time
sys.path.append('files/')
import requests
from lxml import etree
from collections import OrderedDict
from urlparse import urljoin
from colors import *

global actual_uri
actual_uri = []

def crawler20x00(url, count):

	visited_urls = set()
	queued_urls = OrderedDict({ url: '' })

	while len(queued_urls) > 0:
	    (u, i) = queued_urls.popitem(last=False)
	    try:
		req = requests.get(u, timeout=5)
		res = req.status_code
		root = etree.HTML(req.content, base_url=u)
	    except requests.ConnectionError as e:
		res = e
		continue
	    except requests.Timeout as e:
		res = e
		continue
	    except requests.TooManyRedirects as e:
		res = e
		continue
	    except ValueError as e:
		res = e
		continue
	    finally:
		visited_urls.add(u)
		pfx = "{}[{}]".format(i, len(visited_urls))
		if res == 200:
			print B+' [+] Crawling : '+GR+pfx+'  '+C+u+G+'  ('+str(res)+')'
			actual_uri.append(u)
		elif res == 404:
			print B+' [+] Crawling : '+GR+pfx+'  '+C+u+R+'  ('+str(res)+')'
		else:
			print B+' [+] Crawling : '+GR+pfx+'  '+C+u+O+'  ('+str(res)+')'

	    if root is None: continue

	    for a in root.xpath('//a'):
		if (len(visited_urls) + len(queued_urls) >= count):
		    break
		href = a.get('href')
		if href is None: continue
		(uj, sep, ui) = urljoin(a.base, href).partition('#')
		if uj not in visited_urls and uj not in queued_urls:
		    if uj.startswith('http'): 
			queued_urls[uj] = pfx
		if (len(visited_urls) >= count):
			break

def out(web, list0):
	
	web = web.replace('http://','')
	web = web.replace('https://','')
	print GR+' [*] Writing found URLs to a file...'
	if os.path.exists('tmp/logs/'+web+'-logs/'+web+'-links.lst'):		
		fil = open('tmp/logs/'+web+'-logs/'+web+'-links.lst','w+')
		print O+' [!] Sorting only scope urls...'
		time.sleep(1)
		for lists in list0:
		    if str(web) in lists:
			fil.write("%s\n" % lists)
	else:
		fil = open('tmp/logs/'+web+'-logs/'+web+'-links.lst','a')
		print O+' [!] Sorting only scope urls...'
		time.sleep(1)
		for lists in list0:
		    if str(web) in lists:
			fil.write("%s\n" % lists)

def crawler3(web):

    try:
	print GR+' [*] Loading (Level 3) crawler...'
	time.sleep(0.5)

	print R+'\n    =========================='
	print R+'     C R A W L E R  (Depth 3)'
	print R+'    =========================='
	time.sleep(0.7)
	print O+' [This crawler will recursively crawl'
	print O+' all the links of the website as well as all'
	print O+'   links within each of the pages]\n'
	time.sleep(0.7)
	print R+'  WARNING : Use this with CAUTION!\n'
	m = raw_input(GR+' [#] No. of links to be crawled (eg 100) :> ')
	print O+' [!] Crawling limit set to : '+C+str(m)
	w = int(m)
	crawler20x00(web, w)
	out(web, actual_uri)

    except Exception as e:
	print R+' [-] Further crawl aborted due to Exception!'
	print R+' [-] Exception : '+str(e)
	time.sleep(0.7)
	print GR+' [*] Saving the links obtained...'
	out(web, actual_uri)
	print G+' [+] Saved!'

