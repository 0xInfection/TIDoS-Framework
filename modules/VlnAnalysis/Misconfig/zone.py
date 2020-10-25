#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
import requests
import subprocess
import os
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Zone Transfer module."
searchinfo = "Zone Transfer module"
properties = {"DNSV":["DNS server to test for", " "]}

def zone(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = inspect.stack()[0][3]
    global module
    module = "VulnAnalysis"
    global lvl1
    lvl1 = "Basic Bugs & Misconfigurations"
    global lvl3
    lvl3 = ""
    web = web.replace('http://','')
    web = web.replace('https://','')
    try:
        #print(R+'\n   ===========================')
        #print(R+'\n    Z O N E   T R A N S F E R')
        #print(R+'   ---<>----<>----<>----<>----\n')
        from core.methods.print import pvln
        pvln("zone transfer") 
                    
        time.sleep(0.4)
        print(O+' [!] Looking up for name servers on which website is hosted...\n'+G)
        time.sleep(0.7)
        os.system('dig +nocmd '+web+' ns +noall +answer')
        if properties["DNSV"][1] == " ":
            h = input(O+'\n [*] Enter the DNS Server you want to test for :> ')
        else:
            h = properties["DNSV"][1]
        time.sleep(0.4)
        print(GR+' [*] Attempting zone transfer...')
        time.sleep(0.9)
        cm = subprocess.Popen(['host','-t','axfr',web,h,'+answer','+noall','+nocmd'], stdout = subprocess.PIPE).communicate()[0]
        if 'failed' in str(cm):
            print(R+'\n [-] Zone transfer for '+O+h+R+' failed!')
            print(R+' [-] This website is immune to zone transfers!')
            data = 'Zone transfer for '+h+' failed!\nThis website is immune to zone transfers.'
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
        else:
            print('\n'+G+cm)
            save_data(database, module, lvl1, lvl2, lvl3, name, cm)

    except Exception as e:
        print(R+' [-] Error encountered!')
        print(R+' [-] Error : '+str(e))

def attack(web):
    web = web.fullurl
    zone(web)
