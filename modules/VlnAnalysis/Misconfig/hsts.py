#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import time
import requests
import sys
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module checks if target uses HSTS."
searchinfo = "HSTS Check"
properties = {}

def check0x00(headers):
    flag = False
    for head in headers:
        if 'Strict-Transport-Security'.lower() in head.lower():
            print(O+' [!] Reflection in response headers found...')
            flag = True
    if flag:
        print(G+' [+] Seems like the website uses strong HSTS...')
        time.sleep(0.6)
        print(G+' [+] HSTS Presence Confirmed!')
        save_data(database, module, lvl1, lvl2, lvl3, name, "HSTS Presence Confirmed.")
    else:
        print(GR+' [!] HTTP Strict Transport Security Header not found in response headers!')
        print(O+' [-] Website uses complete SSL throughout website.')
        print(R+' [-] However, it does not seem to use HSTS.\n')
        save_data(database, module, lvl1, lvl2, lvl3, name, "Website uses SSL, however, it does not seem to use HSTS.")

def getHeaders0x00(web):
    print(O+' [*] Configuring headers...')
    time.sleep(0.5)
    gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                      'Accept-Language':'en-US;',
                      'Accept-Encoding': 'gzip, deflate',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;',
                      'Connection':'close'}
    cook = input(C+" [*] Got any cookies? [just Enter if none] :> ")
    if cook:
        gen_headers['Cookie'] = cook
    print(GR+' [*] Making the request...')
    time.sleep(0.6)
    req = requests.get(web, headers=gen_headers, timeout=5, verify=True)
    h = req.headers
    return h

def hsts(web):
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
    time.sleep(0.5)
    #print(R+'\n    ================================')
    #print(R+'\n     HTTP STRICT TRANSPORT SECURITY')
    #print(R+'    ---<>----<>----<>----<>----<>---\n')
    from core.methods.print import pvln
    pvln("hsts") 
                 
    if 'https' in web:
        check0x00(getHeaders0x00(web))
    else:
        print(R+' [-] No SSL/TLS detected...')
        m = input(O+' [§] Force SSL/TLS (y/N) :> ')
        if m == 'y' or m == 'Y':
            print(GR+' [*] Using revamped SSL...')
            o = 'https://' + web.replace('http://','')
            check0x00(getHeaders0x00(web))
        elif m == 'n' or m == 'N':
            print(GR+' [-] Skipping module...')

def attack(web):
    web = web.fullurl
    hsts(web)
