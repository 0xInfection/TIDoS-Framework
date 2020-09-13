#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import time
import sslyze
import requests
from core.Core.colors import *
from sslyze.plugins.certificate_info_plugin import CertificateInfoScanCommand
from sslyze.plugins.heartbleed_plugin import HeartbleedScanCommand
from sslyze.plugins.http_headers_plugin import HttpHeadersScanCommand
from sslyze.plugins.openssl_cipher_suites_plugin import Tlsv10ScanCommand, Tlsv11ScanCommand, Tlsv12ScanCommand
from sslyze.server_connectivity_tester import ServerConnectivityTester
from sslyze.synchronous_scanner import SynchronousScanner
domains = []

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "SSL Enumeration module."
searchinfo = "SSL Enumeration module"
properties = {}

def ssltlsscan(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = inspect.stack()[0][3]
    global module
    module = "ScanANDEnum"
    global lvl1
    lvl1 = "Scanning & Enumeration"
    global lvl3
    lvl3 = ""
    target = web.split('//')[1]
    #print(R+'\n    ===============================')
    #print(R+'     S S L   E N U M E R A T I O N')
    #print(R+'    ===============================\n')
    from core.methods.print import pscan
    pscan("ssl enumeration")
    print(GR+' [*] Testing server SSL status...')
    try:
        req = requests.get('https://'+target)
        print(G+' [+] SSL Working Properly...'+color.TR2+C)
        time.sleep(0.6)
        print(C+" [!] Running SSL Enumeration...\n")
        try:
            server_tester = ServerConnectivityTester(hostname=target)
            server_info = server_tester.perform()
            scanner = SynchronousScanner()

            command = Tlsv10ScanCommand()
            scan_result = scanner.run_scan_command(server_info, command)
            print(G+" [+] Available TLS v1.0 Ciphers:"+color.TR2+C)
            for cipher in scan_result.accepted_cipher_list:
                print(C+'    {}'.format(cipher.name))
            print('')
            data = "TLS 1.0 :> " + str(scan_result.accepted_cipher_list)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)

            command = Tlsv11ScanCommand()
            scan_result = scanner.run_scan_command(server_info, command)
            print(G+" [+] Available TLS v1.1 Ciphers:"+color.TR2+C)
            for cipher in scan_result.accepted_cipher_list:
                print(C+'    {}'.format(cipher.name))
            print('')
            data = "TLS 1.1 :> " + str(scan_result.accepted_cipher_list)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)

            command = Tlsv12ScanCommand()
            scan_result = scanner.run_scan_command(server_info, command)
            print(G+" [+] Available TLS v1.2 Ciphers:"+color.TR2+C)
            for cipher in scan_result.accepted_cipher_list:
                print(C+'    {}'.format(cipher.name))
            print('')
            data = "TLS 1.2 :> " + str(scan_result.accepted_cipher_list)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)

            command = CertificateInfoScanCommand()
            scan_result = scanner.run_scan_command(server_info, command)
            print(G+' [+] Certificate Information:'+color.TR2+C)
            for entry in scan_result.as_text():
                if entry != '':
                    if 'certificate information' in entry.lower():
                        pass
                    elif ':' in entry:
                        print(GR+'    [+] '+entry.strip().split(':', 1)[0].strip()+' : '+C+entry.strip().split(':', 1)[1].strip())
                    else:
                        print(C+'\n  [+] ' +entry.strip())
            print('')
            data = "Cert Info :> " + str(scan_result.as_text())
            save_data(database, module, lvl1, lvl2, lvl3, name, data)

            command = HttpHeadersScanCommand()
            scan_result = scanner.run_scan_command(server_info, command)
            print(G+' [+] HTTP Results:'+C+color.TR2+C)
            for entry in scan_result.as_text():
                if 'http security' not in entry.strip().lower() and entry != '':
                    if '-' in entry:
                        print(GR+'    [+] '+entry.split('-',1)[0].strip()+' - '+C+entry.split('-',1)[1].strip())
                    elif ':' in entry:
                        print(GR+'    [+] '+entry.strip().split(':', 1)[0].strip()+' : '+C+entry.strip().split(':', 1)[1].strip())
                    else:
                        print(C+'\n  [+] ' +entry.strip())
            print('')
            data = "HTTP :> " + str(scan_result.as_text())
            save_data(database, module, lvl1, lvl2, lvl3, name, data)

        except Exception as e:
            print(R+' [-] Unhandled SSL Runtime Exception : '+str(e))
            pass

    except requests.exceptions.SSLError as e:
        print(R+' [-] Distant Server SSL not working : '+str(e))

    print(G+' [+] SSlScan Module Completed!'+C+color.TR2+C)

def attack(web):
    web = web.fullurl
    ssltlsscan(web)