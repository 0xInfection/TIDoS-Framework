#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import re
import time
import os
import requests as wrn
from core.methods.tor import session
from core.Core.colors import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
pathsinfo = []
wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)

info = "This module tries to find PHPInfo files on the target's webserver."
searchinfo = "PHPInfo search"
properties = {}

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

def phpinfo(web):
    name = targetname(web)
    lvl2 = "phpinfo"
    module = "ReconANDOSINT"
    lvl1 = "Active Reconnaissance"
    lvl3 = ""
    requests = session()
    found = 0x00
    #print(R+'\n    =============================')
    #print(R+'     P H P I N F O   F I N D E R')
    #print(R+'    =============================\n')
    from core.methods.print import posintact
    posintact("phpinfo finder") 

    print(GR+' [*] Importing file paths...')
    if os.path.exists('files/fuzz-db/phpinfo_paths.lst'):
        with open('files/fuzz-db/phpinfo_paths.lst','r') as paths:
            for path in paths:
                path = '/' + path.replace('\n','')
                pathsinfo.append(path)

        print(C+' [!] Starting bruteforce...')
        for p in pathsinfo:
            web0x00 = web + p
            req = requests.get(web0x00, allow_redirects=False, verify=False)
            if (req.status_code == 200 or req.status_code == 302):
                if re.search(r'\<title\>phpinfo()\<\/title\>|\<h1 class\=\"p\"\>PHP Version',req.content):
                    found = 0x01
                    print(O+' [+] Found PHPInfo File At :'+C+color.TR3+C+G+web0x00+C+color.TR2+C)
                    data = "phpinfo @ " + web0x00
                    save_data(database, module, lvl1, lvl2, lvl3, name, data)
            else:
                print(B+' [*] Checking : '+C+web0x00+R+' ('+str(req.status_code)+')')

        if found == 0x00:
            print(R+'\n [-] Did not find PHPInfo file...\n')
            save_data(database, module, lvl1, lvl2, lvl3, name, "Did not find PHPInfo file.")
    else:
        print(R+' [-] Bruteforce filepath not found!')

def attack(web):
    web = web.fullurl
    phpinfo(web)