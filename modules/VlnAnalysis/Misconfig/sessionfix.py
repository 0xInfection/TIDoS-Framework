#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
from core.methods.tor import session
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module hunts for Session Fixation vulnerabilities."
searchinfo = "Session Fixation Check"
properties = {"COOKIE":["Cookie used in the request ['none' if none]", " "]}

def sessionfix(url):
    global name
    name = targetname(url)
    global lvl2
    lvl2 = inspect.stack()[0][3]
    global module
    module = "VulnAnalysis"
    global lvl1
    lvl1 = "Basic Bugs & Misconfigurations"
    global lvl3
    lvl3 = ""
    requests = session()
    #print(R+'\n   =================================')
    #print(R+'\n    S E S S I O N   F I X A T I O N')
    #print(R+'   ---<>----<>----<>----<>----<>----\n')

    from core.methods.print import pvln
    pvln("session fixation") 
                
    print(GR+' [*] Making the request...')
    if properties["COOKIE"][1] == " ":
        coo = input(O+' [§] Got any cookies? [Just Enter if None] :> ')
    elif properties["COOKIE"][1].lower() == "none":
        coo = ""
    else:
        coo = properties["COOKIE"][1]
    if coo != "":
        req = requests.get(url, cookies=coo, verify=True, timeout=7)
    else:
        req = requests.get(url, verify=True, timeout=7)
    if req.cookies:
        print(G+' [+] Found cookie reflecting in headers...')
        print(B+' [+] Initial cookie state: '+C, req.cookies, '\n')
        user = input(O+' [§] Enter authentication username :> '+C)
        upass = input(O+' [§] Enter password :> '+C)
        print(GR+' [*] Trying POST request with authentication...')
        cookie_req = requests.post(url, cookies=req.cookies, auth=(user, upass), timeout=7)
        print(B+' [+] Authenticated cookie state:'+C, cookie_req.cookies)
        if req.cookies == cookie_req.cookies:
            print(G+' [+] Site seems to be vulnerable...')
            print(G+' [+] Site is vulnerable to session fixation vulnerability!')
            save_data(database, module, lvl1, lvl2, lvl3, name, "Site is vulnerable to session fixation vulnerability!")
        else:
            print(O+' [!] Cookie values do not match...')
            print(R+' [-] Target not vulnerable to session fixation!')
            save_data(database, module, lvl1, lvl2, lvl3, name, "Target not vulnerable to session fixation (cookie values do not match).")
    else:
        print(R+' [-] No basic cookie support!')
        print(R+' [-] Target not vulnerable to session fixation!')
        save_data(database, module, lvl1, lvl2, lvl3, name, "Target not vulnerable to session fixation (no basic cookie support).")
    print(G+' [+] Session Fixation Module Completed!\n')

def attack(web):
    web = web.fullurl
    sessionfix(web)
