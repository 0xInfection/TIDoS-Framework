#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import sys
import requests as wrn
from core.methods.tor import session
import re
import time
import json
from core.Core.colors import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)

info = "Find past versions of a website using the Wayback Machine."
searchinfo = "Wayback Machine Lookup"
properties = {"START":["Year from when results to be fetched", " "], "END":["Year till when results to be fetched", " "], "LIMIT":["No. of results", " "]}

def getRes0x00(web, lvl2):
    #name = targetname(web)
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl3=''
    requests = session()
    error = 0
    if properties["START"][1] == " ":
        fdate = input(C+' [§] Year from when results to be fetched (eg. 2010) :> '+C)
    else:
        fdate = properties["START"][1]
    if properties["END"][1] == " ":
        tdate = input(GR+' [§] Year till when results to be fetched (eg. 2017) :> '+C)
    else:
        tdate = properties["END"][1]
    if properties["LIMIT"][1] == " ":
        limit = input(C+' [§] No. of results (eg. 50) :> '+C)
    else:
        limit = properties["LIMIT"][1]

    if "://" in web:
        web = web.split('://')[1]

    if "@" in web:
        web = web.split("@")[1]

    print(GR+' [*] Setting headers... (behaving as a browser)...')
    time.sleep(0.7)
    headers =   {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                 'Accept-Language':'en-US;',
                 'Accept-Encoding': 'gzip, deflate',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;',
                 'Connection':'close'}
    print(GR+' [*] Setting parameters...')
    url = "https://web.archive.org/cdx/search/cdx?url="+web+"&matchType=domain&limit="+limit+"&output=json&from="+fdate+"&to="+tdate
    time.sleep(0.5)
    try:
        print(P+' [!] Making the no-verify request...'+C)
        req = requests.get(url, headers=headers, timeout=10, verify=False)
        json_data = json.loads(req.text)
        if len(json_data) == 0:
            print(R+' [-] No results found!')
            error = 1
    except Exception as e:
        print(R+' [-] Error loading Url...')
        print(R+' [-] Request got timed out!')
        error = 1

    if error == 0:
        try:
            print(O+' [*] Found the following backups at'+C+color.TR3+C+G+'web.archive.org...'+C+color.TR2+C+'\n')
            result = [ x for x in json_data if x[2] != 'original']
            result.sort(key=lambda x: x[1])
            for line in result:
                timestamp = line[1]
                website   = line[2]
                tlinks  = "https://web.archive.org/web/" + str(timestamp) + "/" + str(website)
                sdates = str(timestamp[:4]) + "/" + str(timestamp[4:6]) + "/" + str(timestamp[6:8])
                print(" {}{}   {}{}  {}({})".format(C, sdates, B, website, C, tlinks))
                time.sleep(0.04)
            save_data(database, module, lvl1, lvl2, lvl3, name, str(result))

        except Exception as e:
            print(R+' [-] Unhandled Exception Encountered!')
            print(R+' [-] Exception : '+str(e))

def webarchive(web):
    global name
    name = targetname(web)
    time.sleep(0.6)
    #print(R+'\n    =============================================')
    #print(R+'     W A Y B A C K   M A C H I N E   L O O K U P')
    #print(R+'    =============================================\n')
    from core.methods.print import posintpas
    posintpas("wayback machine lookup")
    time.sleep(0.7)
    lvl2=inspect.stack()[0][3]
    getRes0x00(web, lvl2)

def attack(web):
    web = web.fullurl
    webarchive(web)