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
import time
import requests as wrn
from core.methods.tor import session
from core.Core.colors import *
sys.path.append('files/signaturedb/')
from bs4 import BeautifulSoup
from files.signaturedb.infodisc_signatures import INTERNAL_IP_SIGNATURE as signature
links = []
urls = []
found = 0x00
from requests.packages.urllib3.exceptions import InsecureRequestWarning
wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module tries to find internal IPs disclosed in target's source code."
searchinfo = "Internal IP hunter"
properties = {}

def internalip0x00(url):
    requests = session()
    #print(R+'\n    ========================')
    #print(R+'     INTERNAL IP DISCLOSURE')
    #print(R+'    ========================\n')
    from core.methods.print import pleak
    pleak("internal ip disclosure")
    time.sleep(0.5)
    links = [url]
    po = url.split('//')[1]
    for w in links:
        print(O+' [*] Scraping Page: '+C+color.TR3+C+G+url+C+color.TR2+C)
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
            print("\n"+O+" [+] Scraping Page: "+C+color.TR3+C*G+uurl+C+color.TR2+C)
            req = requests.get(uurl).text
            check0x00(req, name)

    except Exception:
        print(R+' [-] Outbound Query Exception...')

    if found == 0x00:
        print(R+'\n [-] No Internal IPs found disclosed in plaintext in source code!\n')
        save_data(database, module, lvl1, lvl2, lvl3, name, "No Internal IPs found disclosed in plaintext in source code.")

    print(G+' [+] Scraping Done!'+C+color.TR2+C)

def check0x00(req, name):
    comments = re.findall(signature,req)
    print(GR+" [*] Searching for Internal IPs...")
    for comment in comments:
        print(C+'   '+comment)
        time.sleep(0.03)
        found = 0x01
        save_data(database, module, lvl1, lvl2, lvl3, name, comment)

def internalip(web):
    global lvl1, lvl2, lvl3, name, module
    lvl2 = inspect.stack()[0][3]
    module = "ReconANDOSINT"
    lvl1 = "Information Disclosure"
    lvl3 = ""
    name = targetname(web)
    time.sleep(0.6)
    internalip0x00(web)

def attack(web):
    web = web.fullurl
    internalip(web)
