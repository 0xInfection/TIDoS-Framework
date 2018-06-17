#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import socket
import time
import sys
import getopt
import httplib
from colors import *

def hostheader0x00(target):

	print R+'\n    =========================================='
	print R+'     H O S T  H E A D E R   I N J E C T I O N'
	print R+'    ==========================================\n'

	port = raw_input(O+' [#] Enter the port number to use :> ')

	if port == 443:
		print O+" [!] Using HTTPS <port 443>..."
		print GR+' [*] Setting headers...'
		headers = {
			'User-Agent': 'The Infected Drake [@_tID] on Systems (TIDoS)',
			'Content-Type': 'application/x-www-form-urlencoded',
			}

		print GR+' [*] Requesting response...'
		conn = httplib.HTTPSConnection(host)
		conn.request("GET", "/", "", headers)
		response = conn.getresponse()
		print ' [*] Reading the response...' 
		data = response.read()

		print O+' [!] Response : '+GR, response.status, response.reason
		print O+' [!] Data (raw) : \n'+GR
		print data + '\n'

	else:
		print GR+' [*] Setting buffers...'
		buffer1 = "TRACE / HTTP/1.1"
		buffer2 = "Test: <script>alert(tID)</script>"
		buffer3 = "Host: " + target
		buffer4 = "GET / HTTP/1.1"

		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print GR+' [*] Making the connection...'
		result=s.connect_ex((target,int(port)))
		s.settimeout(1.0)

		if result == 0:

			frame_inject = "codesploit"
			buffer1 = "GET / HTTP/1.1"
			buffer2 = "Host: https://teamcodesploit.gq"

			s.send(buffer1 + "\n")
			s.send(buffer2 + "\n\n")
			data1 = s.recv(1024)
			s.close()

			if frame_inject.lower() in data1.lower():
				print G+' [+] Site is vulnerable to Host Header Injection...'

			else:
				print R+' [-] Site is immune against Host Header Injection...'

			print ""
			print GR+' [*] Obtaining header dump data...'
			print ""
			print O+data1
			print ""

def hhi(web):

	print GR+' [*] Loading the module...'
	time.sleep(0.5)
	if 'http' in web:
		web = web.replace('http://','')
		web = web.replace('https://','')

	hostheader0x00(web)
 
