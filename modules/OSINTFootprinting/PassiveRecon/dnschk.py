#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


import re
import time
import os
import sys
from core.Core.colors import *
sys.path.append('files/')
from core.lib.dnsdump_mod.DNSDumpsterAPI import *

info = "Lookup DNS records and generate DNS Map."
searchinfo = "DNS Lookup Module"
properties = {}

def dnschk(domain):

    #print(R+'\n   =====================')
    #print(R+'    D N S   L 0 0 K U P')
    #print(R+'   =====================\n')
    from core.methods.print import posintpas
    posintpas("dns lookup")

    domain = domain.split('//')[1]
    res = DNSDumpsterAPI(False).search(domain)
    try:
        print(G+'\n [+] DNS Records'+C+color.TR2+C)
        for entry in res['dns_records']['dns']:
            print(''+O+("{domain} ({ip}) {as} {provider} {country}".format(**entry))+C)
        for entry in res['dns_records']['mx']:
            print(G+"\n [+] MX Records"+C+color.TR2+C)
            print(''+O+("{domain} ({ip}) {as} {provider} {country}".format(**entry))+C)
        print(G+"\n [+] Host Records (A)"+C+color.TR2+C)
        for entry in res['dns_records']['host']:
            if entry['reverse_dns']:
                print((O+"{domain} ({reverse_dns}) ({ip}) {as} {provider} {country}".format(**entry))+C)
            else:
                print(O+("{domain} ({ip}) {as} {provider} {country}".format(**entry))+C)
        print(G+'\n [+] TXT Records:'+C+color.TR2+C)
        for entry in res['dns_records']['txt']:
            print(''+O+entry+C)
        print(GR+'\n [*] Preparing DNS Map...')
        time.sleep(0.5)
        url = 'https://dnsdumpster.com/static/map/' + str(domain) + '.png'
        print(P+' [!] Fetching map...'+C)
        try:
            os.system('wget -q ' + url)
        except:
            print(R+' [-] Map generation failed!')
            sys.exit(1)
        st = str(domain) + '.png'
        st1 = str(domain)+'-dnsmap.jpg'
        p = 'mv '+st+' '+ st1
        os.system(p)
        mov = 'mv '+ st1 + ' tmp/'
        os.system(mov)
        print(C+' [+] Map saved under "tmp/' + st1 + '"')
        try:
            print(GR+' [!] Trying to open DNS Map...')
            os.system('xdg-open tmp/'+st1)
        except:
            print(R+' [-] Failed to open automatically.')
            print(GR+' [!] Please view the map manually.')
    except TypeError:
        print(R+' [-] No standard publicly recorded DNS records found.\n')

def attack(web):
    dnschk(web)