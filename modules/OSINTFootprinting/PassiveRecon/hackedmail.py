#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import sys
import requests as wrn
from core.methods.tor import session
import re
import time
import json
from colorama import Style
from core.Core.colors import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)

info = "This module looks up if an email address was found in a data breach."
searchinfo = "Data Breach Checker"
properties = {}

def getRes0x00():
    requests = session()
    email = input(C+' [§] Enter the email :> '+R)
    if '@' in email and '.' in email:
        pass
    else:
        email = input(C+' [§] Enter a valid email :> '+R)

    print(GR+' [*] Setting headers... (behaving as a browser)...')
    time.sleep(0.7)
    headers =   {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                 'Accept-Language':'en-US;',
                 'Accept-Encoding': 'gzip, deflate',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;',
                 'Connection':'close'}
    print(P+' [!] Making the no-verify request...'+C)
    time.sleep(0.5)
    url = 'https://hacked-emails.com/api?q='+str(email)

    try:
        req = requests.get(url, headers=headers, timeout=10, verify=False)
        content = req.text
        if content != "":
            content = json.loads(content)
            if content['status'] == "found":
                print("Result found ("+G+str(content['results']) + " results" + C+ Style.RESET_ALL + ")")
                for line in content['data']:
                    try:
                        print(O+" [+] "+email+" found in :" +C+color.TR3+C+G+ str(line['title']) +" (" + str(line['date_leaked'])+')'+C+color.TR2+C)
                        data = email+" found in :" + str(line['title']) +" (" + str(line['date_leaked'])+')'
                        save_data(database, module, lvl1, lvl2, lvl3, "", data)
                    except Exception:
                        print(R+" [-] Can't parse the leak titles via APi...")
            else:
                print(R+' [-] Email '+O+email+R+' not found in any breaches!')
                data = 'Email '+email+' not found in any breaches!'
                save_data(database, module, lvl1, lvl2, lvl3, "", data)
        else:
            print(R+' [-] Error found in Json Request...')

    except Exception:
        print(R+" [-] Can't reach url...")
        print(R+' [-] Request timed out!')

def hackedmail():
    global lvl2
    lvl2 = inspect.stack()[0][3]
    global module
    module = "ReconANDOSINT"
    global lvl1
    lvl1 = "Passive Reconnaissance & OSINT"
    global lvl3
    lvl3 = ""
    time.sleep(0.6)
    #print(R+'\n    =========================')
    #print(R+'     H A C K E D   E M A I L ')
    #print(R+'    =========================\n')
    from core.methods.print import posintpas
    posintpas("hacked email")
    time.sleep(0.7)
    getRes0x00()

def attack(web):
    hackedmail()
