#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import re
import sys
sys.path.append('files/signaturedb/')
import time
from core.methods.tor import session
from core.Core.colors import *
from re import search
from bs4 import BeautifulSoup
from files.signaturedb.commonerror_signatures import patterns
urls = []
links = []
found = 0x00

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module tries to find errors in target's source code."
searchinfo = "Error hunter"
properties = {}

def check0x00(content,url, lvl2, name):
    for pattern in patterns:
        print(C+' [!] Finding '+B+pattern+C+' ...')
        time.sleep(0.005)
        if search(pattern, content):
            print(O+' [!] Possible error at '+C+color.TR3+C+G+url+C+color.TR2+C)
            print(G+" [+] Found : \"%s\" at %s" % (pattern,url)+C+color.TR2+C)
            data = str(pattern) + " @ " + str(url)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            found = 0x01

def request(url, lvl2):
    name = targetname(url)
    requests = session()
    time.sleep(0.5)
    links = [url]
    po = url.split('//')[1]
    for w in links:
        print(GR+' [*] Scraping Page: '+O+url+C)
        req = requests.get(w).text
        check0x00(req, url, lvl2, name)

    soup = BeautifulSoup(req,'lxml')
    for line in soup.find_all('a', href=True):
        newline = line['href']
        try:
            if newline[:4] == "http":
                if po in newline:
                    urls.append(str(newline))
            elif newline[:1] == "/":
                combline = url+newline
                urls.append(str(combline))
        except Exception:
            print(R+' [-] Unhandled Exception Occured!')

    try:
        for uurl in urls:
            print("\n"+O+" [+] Scraping Page: "+C+color.TR3+C+G+uurl+C+color.TR2+C)
            req = requests.get(uurl).text
            check0x00(req, url, lvl2, name)

    except Exception:
        print(R+' [-] Outbound Query Exception...')

    if found == 0x00:
        print(R+'\n [-] No Errors found in Source Code!\n')
        save_data(database, module, lvl1, lvl2, lvl3, name, "No Errors found in Source Code.")

    print(G+' [+] Scraping Done!'+C+color.TR2+C)

def errors(web):
    global module, lvl1, lvl3
    module = "ReconANDOSINT"
    lvl1 = "Information Disclosure"
    lvl3 = ""
    lvl2 = inspect.stack()[0][3]
    from core.methods.print import pleak
    pleak("error hunter")
    print(C+'  [This module covers up Full Path Disclosures]\n')
    print(GR+' [*] Making the request...')
    time.sleep(0.5)
    request(web, lvl2)

def attack(web):
    web = web.fullurl
    errors(web)
