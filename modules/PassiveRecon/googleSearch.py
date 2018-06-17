#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import time
import sys, platform
import os
import urllib2
try:
	from google import search
except:
	from googlesearch import search
from time import sleep
from colors import *

def googleSearch():

    try:
	time.sleep(0.4)
	print R+'\n   ==========================='
	print R+'    G O O G L E   S E A R C H'
	print R+'   ===========================\n'
	lol = raw_input(O+ " [#] QUERY :> " + color.END)
	time.sleep(0.8)
	m = raw_input(O+' [#] Search limit (not recommended above 30) :> ') 
	print G+ " [!] Below are the list of websites with info on '" +lol+ "'"
	x = search(lol, tld='com', lang='es', stop=int(m))
	for url in x:
		print(""+O+color.BOLD+"   [!] Site Found :> "+W + url)
		os.system('rm -f .google-cookie')
    except urllib2.HTTPError:
	print R+' [-] You have used google many times.'
	print R+' [-] Service temporarily unavailable.'
