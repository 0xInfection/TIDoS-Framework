#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework

import os
import time
import sslyze
import requests
from colors import *
from sslyze.plugins.certificate_info_plugin import CertificateInfoScanCommand
from sslyze.plugins.heartbleed_plugin import HeartbleedScanCommand
from sslyze.plugins.http_headers_plugin import HttpHeadersScanCommand
from sslyze.plugins.openssl_cipher_suites_plugin import Tlsv10ScanCommand, Tlsv11ScanCommand, Tlsv12ScanCommand
from sslyze.server_connectivity_tester import ServerConnectivityTester
from sslyze.synchronous_scanner import SynchronousScanner
domains = []

def ssltlsscan(web):

	target = web.split('//')[1]
	print R+'\n    ==============================='
	print R+'     S S L   E N U M E R A T I O N'
	print R+'    ===============================\n'
	print GR+' [*] Testing server SSL status...'
	try:
		req = requests.get('https://'+target)
		print G+' [+] SSL Working Properly...'
		time.sleep(0.6)
	  	print O+" [!] Running SSL Enumeration...\n"
	  	try:
	    		server_tester = ServerConnectivityTester(hostname=target)
	    		server_info = server_tester.perform()
	    		scanner = SynchronousScanner()

	    		command = Tlsv10ScanCommand()
	    		scan_result = scanner.run_scan_command(server_info, command)
	    		print G+" [+] Available TLS v1.0 Ciphers:"
	    		for cipher in scan_result.accepted_cipher_list:
	      			print C+'    {}'.format(cipher.name)
			print ''

	    		command = Tlsv11ScanCommand()
	    		scan_result = scanner.run_scan_command(server_info, command)
	    		print G+" [+] Available TLS v1.1 Ciphers:"
	    		for cipher in scan_result.accepted_cipher_list:
	      			print C+'    {}'.format(cipher.name)
			print ''

	    		command = Tlsv12ScanCommand()
	    		scan_result = scanner.run_scan_command(server_info, command)
	    		print G+" [+] Available TLS v1.2 Ciphers:"
	    		for cipher in scan_result.accepted_cipher_list:
	      			print C+'    {}'.format(cipher.name)
			print ''

	    		command = CertificateInfoScanCommand()
	    		scan_result = scanner.run_scan_command(server_info, command)
			print G+' [+] Certificate Information:'
	    		for entry in scan_result.as_text():
				if entry != '':
					if 'certificate information' in entry.lower():
						pass
					elif ':' in entry:
			      			print GR+'    [+] '+entry.strip().split(':', 1)[0].strip()+' : '+C+entry.strip().split(':', 1)[1].strip()
					else:
						print O+'\n  [+] ' +entry.strip()
			print ''

	    		command = HttpHeadersScanCommand()
	    		scan_result = scanner.run_scan_command(server_info, command)
			print G+' [+] HTTP Results:'
	    		for entry in scan_result.as_text():
				if 'http security' not in entry.strip().lower() and entry != '':
					if '-' in entry:
			    			print GR+'    [+] '+entry.split('-',1)[0].strip()+' - '+C+entry.split('-',1)[1].strip()
					elif ':' in entry:
			      			print GR+'    [+] '+entry.strip().split(':', 1)[0].strip()+' : '+C+entry.strip().split(':', 1)[1].strip()
					else:
						print O+'\n  [+] ' +entry.strip()					
			print ''

	  	except Exception as e:
	    		print R+' [-] Unhandled SSL Runtime Exception : '+str(e)
	    		pass

	except requests.exceptions.SSLError as e:
		print R+' [-] Distant Server SSL not working : '+str(e)

	print G+' [+] SSlScan Module Completed!'

