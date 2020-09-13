#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
from core.methods.tor import session
import os
from os import system
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Discovers hosts on the same DNS server."
searchinfo = "DNS Shared Hostnames"
properties = {}

def sharedns(web):
    name = targetname(web)
    lvl2 = "sharedns"
    module = "ReconANDOSINT"
    lvl1 = "Active Reconnaissance"
    lvl3 = ""
    requests = session()
    web = web.split('//')[1]
    #print(R+'\n    =========================================')
    #print(R+'     S H A R E D   D N S   H O S T N A M E S ')
    #print(R+'    =========================================\n')
    from core.methods.print import posintact
    posintact("shared dns hostnames") 
    print(C+' [!] Looking up for name servers on which website is hosted...\n'+G)
    time.sleep(0.7)
    system('dig +nocmd '+web+' ns +noall +answer')
    h = input(C+'\n [*] Enter any DNS Server from above :> ')
    time.sleep(0.4)
    print(GR + ' [!] Discovering hosts on same DNS Server...')
    time.sleep(0.4)
    print(GR +" [~] Result: \n"+ color.END)
    domains = [h]
    for dom in domains:
        text = requests.get('http://api.hackertarget.com/findshareddns/?q=' + dom).text
        dns = str(text)
        if 'error' in dns:
            print(R+' [-] Outbound Query Exception!\n')
            time.sleep(0.8)
        elif 'No results found' in dns:
            print(R+' [-] No shared DNS nameserver hosts...')
            save_data(database, module, lvl1, lvl2, lvl3, name, "No shared DNS nameserver hosts.")
        else:
            p = dns.splitlines()
            for i in p:
                print(O+' [+] Site found :>'+C+color.TR3+C+G+i+C+color.TR2+C)
                time.sleep(0.02)
            save_data(database, module, lvl1, lvl2, lvl3, name, dns)

def attack(web):
    web = web.fullurl
    sharedns(web)