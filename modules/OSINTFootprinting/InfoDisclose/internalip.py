#!/usr/bin/env python3
# coding: utf-8
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#
#
#Author : @_tID (0xInfection)
#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


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
        check0x00(req)

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
        except:
            print(R+' [-] Unhandled Exception Occured!')

    try:
        for uurl in urls:
            print("\n"+O+" [+] Scraping Page: "+C+color.TR3+C*G+uurl+C+color.TR2+C)
            req = requests.get(uurl).text
            check0x00(req)

    except:
        print(R+' [-] Outbound Query Exception...')

    if found == 0x00:
        print(R+'\n [-] No Internal IPs found disclosed in plaintext in source code!\n')

    print(G+' [+] Scraping Done!'+C+color.TR2+C)

def check0x00(req):
    comments = re.findall(signature,req)
    print(GR+" [*] Searching for Internal IPs...")
    for comment in comments:
        print(C+'   '+comment)
        time.sleep(0.03)
        found = 0x01

def internalip(web):

    print(GR+' [*] Loading module...')
    time.sleep(0.6)
    internalip0x00(web)

def attack(web):
    internalip(web)