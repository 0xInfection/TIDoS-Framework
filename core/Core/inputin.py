#!/usr/bin/env python
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import sys
import socket
import time
import os
from core.Core.colors import *

def inputin():

    try:
        global web
        web = raw_input(''+O+' [#] Target web address :> '+C)
        if 'exit' == web:
            print(R+' [-] Exiting...')
            print(C+' [#] Alvida, my friend!')
            sys.exit(1)
        if not str(web).startswith('http'):
            mo = raw_input(GR+' [#] Does this website use SSL? (y/n) :> ')
            if mo == 'y' or mo == 'Y':
                web = 'https://'+web
            elif mo == 'n':
                web = 'http://'+web
        if 'http://' in web:
            po = web.split('//')[1]
        elif 'https://' in web:
            po = web.split('//')[1]
        if str(web).endswith('/'):
            web = po[:-1]
            po = po[:-1]
        print(GR+' [*] Checking server status...')

        try:
            ip = socket.gethostbyname(po)
            print(G+' [+] Site seems to be up...')
            print(G+' [+] IP Detected : '+O+ip)
            print('')
            os.system('cd tmp/logs/ && rm -rf '+po+'-logs && mkdir '+po+'-logs/')
            return web

        except socket.gaierror:
            print(R+' [-] Site seems to be down...')
            sys.exit(1)

    except KeyboardInterrupt:
        print(R+' [-] Exiting...')
        print(C+' [#] Alvida, my friend!')
        sys.exit(1)
