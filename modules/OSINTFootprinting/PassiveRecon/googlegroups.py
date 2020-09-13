#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import json
import time
from core.methods.tor import session
import re
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module uses Google Groups to enumerate email addresses."
searchinfo = "Enumeration using Google Groups"
properties = {}

def getemails0x00(domain):
    requests = session()
    global flag
    flag = False
    page_counter = 0
    emails = []
    try:
        while page_counter < 100 :
            print(GR+' [*] Setting parameters...')
            time.sleep(0.6)
            results = 'http://www.google.com/search?q='+str(domain)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter) + '&sa=N'
            print(C+' [!] Making the request...')
            response = requests.get(results)
            print(GR+' [*] Extracting reponse...')
            text = response.text
            emails = re.findall('([\w\.\-]+@'+domain+')',tagparse(text))
            for email in emails:
                print(O+' [+] Received e-mail :'+C+color.TR3+C+G+email+C+color.TR2+C)
                if email not in emails:
                    emails.append(email)
                flag = True
            page_counter = page_counter + 10
    except IOError:
        print(R+" [-] Error connecting to Google Groups...")

    try:
        while page_counter < 100 :
            print(GR+' [*] Setting parameters...')
            time.sleep(0.6)
            results = 'http://groups.google.com/groups?q='+str(domain)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter) + '&sa=N'
            print(C+' [!] Making the request...')
            response = requests.get(results)
            print(GR+' [*] Extracting reponse...')
            text = response.text
            emails = re.findall('([\w\.\-]+@'+domain+')',tagparse(text))
            for email in emails:
                print(O+' [+] Received e-mail :'+C+color.TR3+C+G+email+C+color.TR2+C)
                if email not in emails:
                    emails.append(email)
                flag = True
            page_counter = page_counter + 10
    except IOError:
        print(R+" [-] Error connecting to Google Groups...")
    return emails

def tagparse(text):
    print(GR+' [*] Parsing raw data...')
    time.sleep(0.5)
    finished = 0
    while not finished:
        finished = 1
        start = text.find("<")
        if start >= 0:
            stop = text[start:].find(">")
            if stop >= 0:
                text = text[:start] + text[start+stop+1:]
                finished = 0
    return text

def googlegroups(web):
    name = targetname(web)
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl3=''
    lvl2=inspect.stack()[0][3]
    time.sleep(0.7)
    #print(R+'\n    ===========================')
    #print(R+'     G O O G L E   G R O U P S')
    #print(R+'    ===========================\n')
    from core.methods.print import posintpas
    posintpas("google groups")

    print(C+' [!] Initiating enumeration via Google Web...')
    time.sleep(0.7)
    print(C+' [!] Parsing url...')
    web = web.replace('https://','')
    web = web.replace('http://','')
    if "@" in web:
        web = web.split("@")[1]
    data = getemails0x00(web)
    if flag == False:
        print(R+' [-] No results found via enumeration on Google Groups...')
        save_data(database, module, lvl1, lvl2, lvl3, name, "No results found via enumeration on Google Groups.")
    else:
        save_data(database, module, lvl1, lvl2, lvl3, name, str(data))
    print(C+' [+] Done!')

def attack(web):
    web = web.fullurl
    googlegroups(web)
