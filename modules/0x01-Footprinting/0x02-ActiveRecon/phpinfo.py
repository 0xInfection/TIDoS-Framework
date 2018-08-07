#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework

import re
import time
import os
import requests
from colors import *
found = 0x00
from requests.packages.urllib3.exceptions import InsecureRequestWarning
pathsinfo = []
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def phpinfo(web):

	print R+'\n    ============================='
	print R+'     P H P I N F O   F I N D E R'
	print R+'    =============================\n'

	print GR+' [*] Importing file paths...'
	if os.path.exists('files/fuzz-db/phpinfo_paths.lst'):
		with open('files/fuzz-db/phpinfo_paths.lst','r') as paths:
			for path in paths:
				path = path.replace('\n','') + '/'
				pathsinfo.append(path)

		print O+' [!] Starting bruteforce...'
		for p in pathsinfo:
			web0x00 = web + p
			print B+' [*] Trying : '+C+web0x00
			req = requests.get(web0x00, allow_redirects=False, verify=False)
			if (req.status_code == 200 or req.status_code == 302) and search(r'\<title\>phpinfo()\<\/title\>|\<h1 class\=\"p\"\>PHP Version',req.content):
				found = 0x01
				print G+' [+] Found PHPInfo File At : '+O+web0x00
		if found == 0x00:
			print R+' [-] Did not find PHPInfo file...'

	else:
		print R+' [-] Bruteforce filepath not found!'

