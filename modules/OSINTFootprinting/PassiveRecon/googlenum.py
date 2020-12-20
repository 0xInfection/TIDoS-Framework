#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


from core.methods.tor import session
import time
import json
import urllib.request
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Enumerate profiles using Google."
searchinfo = "Google Gathering"
properties = {}

def googlenum(web):
    requests = session()
    name = targetname(web)
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl3=''
    lvl2=inspect.stack()[0][3]
    kind = []
    etag = []
    obj = []
    ID = []
    disp = []
    url = []
    #print(R+'\n    =================================')
    #print(R+'     G O O G L E   G A T H E R I N G ')
    #print(R+'    =================================\n')
    from core.methods.print import posintpas
    posintpas("google gathering")
    try:
        print(GR+' [*] Importing API Token...')
        time.sleep(0.7)
        from files.API_KEYS import GOOGLE_API_TOKEN
        if GOOGLE_API_TOKEN != '':
            maxr = '50'
            print(GR+' [*] Fetching maximum 50 results...')
            print(O+' [!] Parsing website address...'+C)
            time.sleep(0.6)
            web = web.replace('http://','')
            web = web.replace('https://','')
            if "@" in web:
                web = web.split("@")[1]
            print(GR+' [*] Making the request...')
            try:
                resp = requests.get('https://www.googleapis.com/plus/v1/people?query='+web+'&key='
                        +GOOGLE_API_TOKEN+'&maxResults='+maxr).text
            except Exception:
                print(R+' [-] Access Forbidden (403)...')
            print(O+' [!] Parsing raw-data...'+C)
            time.sleep(1)
            r = json.loads(resp)
            ctr = 1
            print(GR+' [*] Fetching data...')
            if "items" in r:
                for p in r["items"]:
                    ctr+=1
                    time.sleep(0.8)
                    print(C+'\n [+] Info about Profile '+P+str(ctr)+C+' ...')
                    if 'kind' in p:
                        print(O+' [+] Kind :'+C+color.TR3+C+G+p['kind']+C+color.TR2+C)
                        kind.append(p['kind'])
                    time.sleep(0.05)
                    if 'etag' in p:
                        print(O+' [+] E-Tag :'+C+color.TR3+C+G+p['etag']+C+color.TR2+C)
                        etag.append(p['etag'])
                    time.sleep(0.05)
                    if 'objectType' in p:
                        print(O+' [+] Object Type :'+C+color.TR3+C+G+p['objectType']+C+color.TR2+C)
                        obj.append(p['objectType'])
                    time.sleep(0.05)
                    if 'id' in p:
                        print(O+' [+] ID :'+C+color.TR3+C+G+p['id']+C+color.TR2+C)
                        ID.append(p['id'])
                    time.sleep(0.05)
                    if 'displayName' in p:
                        print(O+' [+] Display Name :'+C+color.TR3+C+G+p['displayName']+C+color.TR2+C)
                        disp.append(p['displayName'])
                    time.sleep(0.05)
                    if 'url' in p:
                        print(O+' [+] Link :'+C+color.TR3+C+G+p['url']+C+color.TR2+C)
                        url.append(p['url'])
                    time.sleep(0.05)
                    
            data = {"Kind":kind, "E-Tag":etag, "ObjectType":obj, "ID":ID, "DisplayName":disp, "Link":url}
            save_data(database, module, lvl1, lvl2, lvl3, name, str(data))
            print(G+' [+] Google Enumeration Completed!'+C+color.TR2+C)

        else:
            print(R+' [-] Google API Token Key not set... This modules cannot be used!')

    except IOError:
        print(R+' [-] Google API Token Key not set... This modules cannot be used!')

def attack(web):
    web = web.fullurl
    googlenum(web)
