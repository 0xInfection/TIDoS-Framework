#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#
#
#Author : @_tID (0xInfection)
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import re
import sys
sys.path.append('files/signaturedb/')
import time
import requests as wrn
from core.methods.tor import session
from core.Core.colors import *
links = []
urls = []
found = 0x00
from bs4 import BeautifulSoup
from files.signaturedb.infodisc_signatures import EMAIL_HARVESTER_SIGNATURE as signature
from requests.packages.urllib3.exceptions import InsecureRequestWarning
wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module tries to find email addresses disclosed in target's source code."
searchinfo = "Email hunter"
properties = {}

def mail0x00(url, lvl2):
    name = targetname(url)
    requests = session()
    #print(R+'\n    ======================')
    #print(R+'     EMAIl INFO HARVESTER')
    #print(R+'    ======================\n')
    from core.methods.print import pleak
    pleak("email info harvester")
    time.sleep(0.5)
    links = [url]
    po = url.split('//')[1]
    for w in links:
        print(O+' [*] Scraping Page:'+C+color.TR3+C+G+url+C+color.TR2+C)
        req = requests.get(w).text
        check0x00(req, lvl2, name)

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
            print("\n"+O+" [+] Scraping Page:"+C+color.TR3+C+G+uurl+C+color.TR2+C)
            req = requests.get(uurl).text
            check0x00(req, lvl2, name)

    except Exception:
        print(R+' [-] Outbound Query Exception...')

    if found == 0x00:
        print(R+'\n [-] No Emails found disclosed in plaintext in source code!\n')
        save_data(database, module, lvl1, lvl2, lvl3, name, "No emails found disclosed in plaintext in source code")

    print(G+' [+] Scraping Done!'+C+color.TR2+C)

def check0x00(req, lvl2, name):
    comments = re.findall(signature,req)
    print(GR+" [*] Searching for Emails...")
    if comments:
        print('\n'+G+' [+] Found Email(s):'+C+color.TR2+C)
        for comment in comments:
            print(C+'   - '+comment)
            time.sleep(0.03)
            found = 0x01
            save_data(database, module, lvl1, lvl2, lvl3, name, comment)

def emailext(web):
    global module, lvl1, lvl3
    module = "ReconANDOSINT"
    lvl1 = "Information Disclosure"
    lvl3 = ""
    lvl2 = inspect.stack()[0][3]
    time.sleep(0.6)
    mail0x00(web, lvl2)

def attack(web):
    web = web.fullurl
    emailext(web)
