#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import time
from core.methods.tor import session
import hashlib
from core.Core.colors import *

md5s = {}
responses = {}

info = "Alternate Site Discovery using UserAgent spoofing."
searchinfo = "Alternate Site Discovery"
properties = {}

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

def altsites(web):
    requests = session()
    tname = targetname(web)
    lvl2 = "altsites"
    module = "ReconANDOSINT"
    lvl1 = "Active Reconnaissance"
    lvl3 = ""
    #print(R+'\n    ===================================')
    #print(R+'     A L T E R N A T I V E   S I T E S')
    #print(R+'    ===================================\n')

    from core.methods.print import posintact
    posintact("alternative sites") 

    print(GR+' [*] Setting User-Agents...')
    time.sleep(0.7)
    user_agents = {
            'Chrome on Windows 8.1' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
            'Safari on iOS'         : 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4',
            'IE6 on Windows XP'     : 'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
            'Googlebot'             : 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            }

    print(GR+'\n [*] Preparing for series of requests...')
    for name, agent in user_agents.items():
        print(B+' [+] Using User-Agent : '+C+name)
        print(GR+' [+] UA Value : '+O+agent)
        headers = {'User-Agent' : agent}
        print(GR+' [*] Making the request...')
        req = requests.get(web, headers=headers, allow_redirects=True, verify=True)
        responses[name] = req

    print(C+'\n [!] Comparing base value standards...')
    time.sleep(0.5)
    for name, response in responses.items():
        print(O+' [+] User-Agent :'+C+color.TR3+C+G+name+C+color.TR2+C)
        print(O+' [+] Response :'+C+color.TR3+C+G+str(response)+C+color.TR2+C)
        md5s[name] = hashlib.md5(response.text.encode('utf-8')).hexdigest()

    print(C+'\n [!] Matching hexdigest signatures...')
    for name, md5 in md5s.items():
        print(O+' [+] User-Agent :'+C+color.TR3+C+G+name+C+color.TR2+C)
        print(O+' [+] Hex-Digest :'+C+color.TR3+C+G+str(md5)+C+color.TR2+C)
        if name != 'Chrome on Windows 8.1':
            if md5 != md5s['Chrome on Windows 8.1']:
                print(G+' [+] '+str(name)+' differs fromk baseline!'+C+color.TR2+C)
                save_data(database, module, lvl1, lvl2, lvl3, tname, str(name)+" differs fromk baseline")
            else:
                print(R+' [-] No alternative site found via User-Agent spoofing:'+ str(md5))
                save_data(database, module, lvl1, lvl2, lvl3, tname, "No alternative site found via User-Agent spoofing: "+ str(md5))
    print(C+'\n [+] Alternate Site Discovery Completed!\n')

def attack(web):
    web = web.fullurl
    altsites(web)
