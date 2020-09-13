#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import socket
import sys
import json
#import requests
from core.methods.tor import session
import re
import time
from core.Core.colors import *
from time import sleep
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module scans the CENSYS database for IP addresses belonging to the target."
searchinfo = "Webserver enumeration"
properties = {}

def webscan(web):
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
    requests = session()
    try:
        #print(R+'\n    ===========================================')
        #print(R+'     W E B S E R V E R   E N U M E R A T I O N')
        #print(R+'    ===========================================')
        from core.methods.print import pscan
        pscan("webserver enumeration")
        print(C+' [This module will scan the whole CENSYS database for')
        print(C+'      collecting domain based IP Addresses and ')
        print(C+'           fingerprint them accordingly]\n')
        time.sleep(0.6)
        print(R+' [-] WARNING: Use this module with caution!')
        print(GR+' [*] Importing API Key...')
        try:
            from files.API_KEYS import CENSYS_UID, CENSYS_SECRET
        except (IOError, ImportError):
            print(R+' [-] Error while importing key...')

        web = web.split('//')[1]
        print(C+' [!] Obtaining reverse DNS lookup...')
        time.sleep(0.7)
        ip = web
        print(O+' [+] Identified IP :'+C+color.TR3+C+G+str(ip)+C+color.TR2+C)
        print(GR+' [*] Starting internet wide server scan...')
        if CENSYS_SECRET != '' and CENSYS_UID != '':

            print(O+' [+] Found Censys UID Key :'+C+color.TR3+C+G+CENSYS_UID+C+color.TR2+C)
            print(O+' [+] Found Censys Secret Token :'+C+color.TR3+C+G+CENSYS_SECRET+C+color.TR2+C)

            pages = float('inf')
            page = 1

            print(GR+' [*] Setting scan parameters...')
            while page <= pages:

                base_url = 'https://www.censys.io/api/v1'
                params = {'query' : ip, 'page' : page}
                res = requests.post(base_url + "/search/ipv4", json = params, auth = (CENSYS_UID, CENSYS_SECRET))
                payload = res.json()

                for r in payload['results']:

                    ip = r["ip"]
                    proto = r["protocols"]
                    proto = [p.split("/")[0] for p in proto]
                    proto.sort(key=float)
                    protoList = ','.join(map(str, proto))

                    print(B+' [+] IP : '+C+str(ip)+C+' - Protocols : '+str(protoList))

                    if '80' in protoList:
                        view(ip, base_url, CENSYS_UID, CENSYS_SECRET, requests)

                pages = payload['metadata']['pages']
                page += 1

        else:
            print(R+' [-] CENSYS API TOKENs not set!')
            print(R+' [-] This module cannot be used!')

    except Exception as e:
        print(R+' [-] Unhandled Exception Encountered!')
        print(R+' [-] Error : '+str(e))

def view(server, ur, uid, sec, requests):

    res = requests.get(ur + ("/view/ipv4/%s" % server), auth = (uid, sec))
    payload = res.json()

    try:
        if 'title' in payload['80']['http']['get'].keys():
            print(C+" [+] Title : "+GR+"%s" % payload['80']['http']['get']['title'])
            data = "Title :> " + payload['80']['http']['get']['title']
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
        if 'server' in payload['80']['http']['get']['headers'].keys():
            print(C+" [+] Server : "+GR+"%s" % payload['80']['http']['get']['headers']['server'])
            data = "Server :> " + payload['80']['http']['get']['headers']['server']
            save_data(database, module, lvl1, lvl2, lvl3, name, data)

    except Exception as error:
        print(R+' [-] Exception : '+str(error))

def attack(web):
    web = web.fullurl
    webscan(web)