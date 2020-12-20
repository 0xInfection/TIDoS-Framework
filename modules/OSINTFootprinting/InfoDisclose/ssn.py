#!/usr/bin/env python3
# coding: utf-8
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
from bs4 import BeautifulSoup
from files.signaturedb.infodisc_signatures import SOCIAL_SECURITY_SIGNATURE as signature
found = 0x00
urls = []
links = []
from requests.packages.urllib3.exceptions import InsecureRequestWarning
wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module tries to find social security numbers disclosed in target's source code."
searchinfo = "SSN Hunter"
properties = {}

def ssn0x00(url):
    requests = session()
    #print(R+'\n    =================================')
    #print(R+'     SOCIAL SECURITY INFO DISCLOSURE')
    #print(R+'    =================================\n')
    from core.methods.print import pleak
    pleak("social security info disclosure")
    time.sleep(0.5)
    links = [url]
    po = url.split('//')[1]
    for w in links:
        print(O+' [*] Scraping Page: '+C+color.TR3+C*G+url+C+color.TR2+C)
        req = requests.get(w).text
        check0x00(req, name)

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
            check0x00(req, name)

    except Exception:
        print(R+' [-] Outbound Query Exception...')

    if found == 0x00:
        print(R+'\n [-] No Social Security Numbers found disclosed in plaintext in source code!\n')
        save_data(database, module, lvl1, lvl2, lvl3, name, "No Social Security Numbers found disclosed in plaintext in source code.")

    print(G+' [+] Scraping Done!'+C+color.TR2+C)

def check0x00(req, name):
    comments = re.findall(signature,req)
    print(GR+" [*] Searching for Social Security Numbers...")
    for comment in comments:
        print(C+'   '+comment)
        time.sleep(0.03)
        found = 0x01
        save_data(database, module, lvl1, lvl2, lvl3, name, comment)

def ssn(web):
    global name, lvl1, lvl2, lvl3, module
    name = targetname(web)
    lvl2 = inspect.stack()[0][3]
    module = "ReconANDOSINT"
    lvl1 = "Information Disclosure"
    lvl3 = ""
    time.sleep(0.6)
    ssn0x00(web)

def attack(web):
    web = web.fullurl
    ssn(web)
