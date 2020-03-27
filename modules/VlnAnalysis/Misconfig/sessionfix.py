#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


import time
from core.methods.tor import session
from core.Core.colors import *

info = "This module hunts for Session Fixation vulnerabilities."
searchinfo = "Session Fixation Check"
properties = {"COOKIE":["Cookie used in the request ['none' if none]", " "]}

def sessionfix(url):
    requests = session()
    #print(R+'\n   =================================')
    #print(R+'\n    S E S S I O N   F I X A T I O N')
    #print(R+'   ——·‹›·––·‹›·——·‹›·——·‹›·––·‹›·——·\n')

    from core.methods.print import pvln
    pvln("session fixation") 
                
    print(GR+' [*] Making the request...')
    if properties["COOKIE"][1] == " ":
        coo = input(O+' [§] Got any cookies? [Just Enter if None] :> ')
    elif properties["COOKIE"][1].lower() == "none":
        coo = ""
    else:
        coo = properties["COOKIE"][1]
    if coo is not "":
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
        else:
            print(O+' [!] Cookie values do not match...')
            print(R+' [-] Target not vulnerable to session fixation!')
    else:
        print(R+' [-] No basic cookie support!')
        print(R+' [-] Target not vulnerable to session fixation!')
    print(G+' [+] Session Fixation Module Completed!\n')

def attack(web):
    sessionfix(web)