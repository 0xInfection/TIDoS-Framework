#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import re
import time
import os
import sys
from core.Core.colors import *
sys.path.append('files/')
from core.lib.dnsdump_mod.DNSDumpsterAPI import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Lookup DNS records and generate DNS Map."
searchinfo = "DNS Lookup Module"
properties = {}

def dnschk(domain):
    name = targetname(domain)
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl3=''
    lvl2=inspect.stack()[0][3]
    #print(R+'\n   =====================')
    #print(R+'    D N S   L 0 0 K U P')
    #print(R+'   =====================\n')
    from core.methods.print import posintpas
    posintpas("dns lookup")

    domain = domain.split('//')[1]
    res = DNSDumpsterAPI(False).search(domain)
    try:
        dns = []
        mx = []
        host = []
        txt = []
        print(G+'\n [+] DNS Records'+C+color.TR2+C)
        for entry in res['dns_records']['dns']:
            print(''+O+("{domain} ({ip}) {as} {provider} {country}".format(**entry))+C)
            dns.append(entry)
        for entry in res['dns_records']['mx']:
            print(G+"\n [+] MX Records"+C+color.TR2+C)
            print(''+O+("{domain} ({ip}) {as} {provider} {country}".format(**entry))+C)
            mx.append(entry)
        print(G+"\n [+] Host Records (A)"+C+color.TR2+C)
        for entry in res['dns_records']['host']:
            if entry['reverse_dns']:
                print((O+"{domain} ({reverse_dns}) ({ip}) {as} {provider} {country}".format(**entry))+C)
            else:
                print(O+("{domain} ({ip}) {as} {provider} {country}".format(**entry))+C)
            host.append(entry)
        print(G+'\n [+] TXT Records:'+C+color.TR2+C)
        for entry in res['dns_records']['txt']:
            print(''+O+entry+C)
            txt.append(entry)
        
        data = {"DNS":dns, "MX":mx, "HOST":host, "TXT":txt}
        save_data(database, module, lvl1, lvl2, lvl3, name, str(data))
        print(GR+'\n [*] Preparing DNS Map...')
        time.sleep(0.5)
        url = 'https://dnsdumpster.com/static/map/' + str(domain) + '.png'
        print(P+' [!] Fetching map...'+C)
        try:
            os.system('wget -q ' + url)
        except Exception:
            print(R+' [-] Map generation failed!')
            sys.exit(1)
        st = str(domain) + '.png'
        st1 = str(domain)+'-dnsmap.png'
        p = 'mv '+st+' '+ st1
        os.system(p)
        mov = 'mv '+ st1 + ' tmp/'
        os.system(mov)
        print(C+' [+] Map saved under "tmp/' + st1 + '"')
        try:
            print(GR+' [!] Trying to open DNS Map...')
            os.system('xdg-open tmp/'+st1)
        except Exception:
            print(R+' [-] Failed to open automatically.')
            print(GR+' [!] Please view the map manually.')
    except TypeError:
        print(R+' [-] No standard publicly recorded DNS records found.\n')

def attack(web):
    web = web.fullurl
    dnschk(web)
