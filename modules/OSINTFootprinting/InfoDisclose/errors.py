#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


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

info = "This module tries to find errors in target's source code."
searchinfo = "Error hunter"
properties = {}

def check0x00(content,url):

    for pattern in patterns:
        print(C+' [!] Finding '+B+pattern+C+' ...')
        time.sleep(0.005)
        if search(pattern, content):
            print(O+' [!] Possible error at '+C+color.TR3+C+G+url+C+color.TR2+C)
            print(G+" [+] Found : \"%s\" at %s" % (pattern,url)+C+color.TR2+C)
            found = 0x01

def request(url):
    requests = session()
    time.sleep(0.5)
    links = [url]
    po = url.split('//')[1]
    for w in links:
        print(GR+' [*] Scraping Page: '+O+url+C)
        req = requests.get(w).text
        check0x00(req, url)

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
            print("\n"+O+" [+] Scraping Page: "+C+color.TR3+C+G+uurl+C+color.TR2+C)
            req = requests.get(uurl).text
            check0x00(req, url)

    except:
        print(R+' [-] Outbound Query Exception...')

    if found == 0x00:
        print(R+'\n [-] No Errors found in Source Code!\n')

    print(G+' [+] Scraping Done!'+C+color.TR2+C)

def errors(web):

    #print(R+'\n       =========================')
    #print(R+'        E R R O R   H U N T E R ')
    #print(R+'       =========================')
    from core.methods.print import pleak
    pleak("error hunter")
    print(C+'  [This module covers up Full Path Disclosures]\n')
    print(GR+' [*] Making the request...')
    time.sleep(0.5)
    request(web)

def attack(web):
    web = web.fullurl
    errors(web)