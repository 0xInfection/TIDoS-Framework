#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


import shodan
import socket
import json
import time
import sys
sys.path.append('files/')
from core.Core.colors import *
from files.API_KEYS import SHODAN_API_KEY

info = "Bannergrabbing using Shodan API."
searchinfo = "Bannergrab module"
properties = {}

def grab(web):

    api = shodan.Shodan(SHODAN_API_KEY)
    print(GR+' [*] Resolving hostnames...')
    time.sleep(0.7)
    try:
        print(C+' [!] Parsing information...')
        hostIP = socket.gethostbyname(web)

        print(C+' [!] Setting query parameters...')
        host = api.host(hostIP)

        for item in host['data']:
            print(GR+'\n [+] Port : '+C+ str(item['port']))
            print(G+' [+] Banner :'+C+color.TR2+C+' \n')
            for q in str(item['data']).splitlines():
                if ':' in q:
                    print(O+'    '+q.split(':')[0]+' :'+C+color.TR3+C+G+q.split(':')[1].strip()+C+color.TR2+C)
                else:
                    print(C+'    '+q)
                    time.sleep(0.02)

    except KeyboardInterrupt:
        print(R+' [-] An error occured...\n')

def bannergrab(web):

    #print(R+'\n    ===============================')
    #print(R+'     B A N N E R   G R A B B I N G')
    #print(R+'    ===============================\n')
    from core.methods.print import pscan
    pscan("banner grabbing")

    print(GR+' [*] Parsing Url...')
    web = web.replace('http://','')
    web = web.replace('https://','')
    grab(web)
    print(G+'\n [+] Banner Grabbing Done!'+C+color.TR2+C)

def attack(web):
    web = web.fullurl
    bannergrab(web)