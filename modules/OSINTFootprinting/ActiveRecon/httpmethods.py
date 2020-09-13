#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import http.client
import time
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Lists allowed HTTP methods."
searchinfo = "HTTP Methods Lister"
properties = {}

def httpmethods(web):
    name = targetname(web)
    lvl2 = "httpmethods"
    module = "ReconANDOSINT"
    lvl1 = "Active Reconnaissance"
    lvl3 = ""
    try:
        #print(R+'\n    =========================')
        #print(R+'     H T T P   M E T H O D S ')
        #print(R+'    =========================\n')

        from core.methods.print import posintact
        posintact("http methods") 

        print(GR+' [*] Parsing Url...')
        time.sleep(0.7)
        web = web.replace('https://','')
        web = web.replace('http://','')
        print(C+' [!] Making the connection...')
        conn = http.client.HTTPConnection(web)
        conn.request('OPTIONS','/')
        response = conn.getresponse()
        q = str(response.getheader('allow'))
        if 'None' not in q:
            print(G+' [+] The following HTTP methods are allowed...'+C+color.TR2+C)
            methods = q.split(',')
            for method in methods:
                print(O+'     '+method+C)
            save_data(database, module, lvl1, lvl2, lvl3, name, q)
        else:
            print(R+' [-] HTTP Method Options Request Unsuccessful...')
            save_data(database, module, lvl1, lvl2, lvl3, name, "HTTP Method Options Request Unsuccessful.")

    except Exception as e:
        print(R+' [-] Exception Encountered!')
        print(R+' [-] Error : '+str(e))

def attack(web):
    web = web.fullurl
    httpmethods(web)