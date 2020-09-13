#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import json
from core.methods.tor import session
import time
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Find information about domains using CENSYS."
searchinfo = "CENSYS Domain Recon"
properties = {}

def censysdom(web):
    name = targetname(web)
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl2 = inspect.stack()[0][3]
    lvl3 = ""
    requests = session()
    #print(R+'\n    =======================================')
    #print(R+'     C E N S Y S   D O M A I N   R E C O N')
    #print(R+'    =======================================\n')
    from core.methods.print import posintpas
    posintpas("censys domain recon") 

    time.sleep(0.6)
    print(GR+' [*] Importing API Key...')
    try:
        from files.API_KEYS import CENSYS_UID, CENSYS_SECRET
    except IOError as ImportError:
        print(R+' [-] Error while importing key...')

    web = web.split('//')[1]
    if "@" in web:
        web = web.split("@")[1]
    if CENSYS_SECRET != '' and CENSYS_UID != '':
        print(O+' [+] Found Censys UID Key : '+C+color.TR3+C+G+CENSYS_UID+C+color.TR2+C)
        print(O+' [+] Found Censys Secret Token : '+C+color.TR3+C+G+CENSYS_SECRET+C+color.TR2+C)
        base_url = 'https://www.censys.io/api/v1'
        print(GR+' [*] Looking up info...')
        time.sleep(0.7)
        resp = requests.get(base_url + "/view/websites/"+web, auth=(CENSYS_UID, CENSYS_SECRET))
        if 'quota_exceeded' in resp.text:
            print(R+' [-] Daily limit reached for this module. Use you own API key for CENSYS.')

        if resp.status_code == 200:

            print(G+' [+] Found domain info!'+C+color.TR2+C)
            w = resp.text.encode('utf-8')
            asio = json.dumps(resp.json(), indent=4)
            data = asio.splitlines()
            save_data(database, module, lvl1, lvl2, lvl3, name, str(data))
            quest = asio.splitlines()
            print(O+' [!] Parsing info...'+C+'\n')
            time.sleep(1)
            for q in quest:
                q = q.replace('"','')
                if ':' in q and '[' not in q and '{' not in q:
                    q1 = q.split(':',1)[0].strip().title()
                    q2 = q.split(':',1)[1].strip().replace(',','')
                    print(C+'   [+] '+q1+' : '+GR+q2)
                    time.sleep(0.01)

                elif ('{' or '[' in q) and (':' in q):
                    w1 = q.split(':',1)[0].strip().upper()
                    w2 = q.split(':',1)[1].strip()
                    print(C+'\n [+] '+w1+' :-'+'\n')

                elif '{' not in q and '[' not in q and ']' not in q and '}' not in q:
                    print(GR+'   [+] '+q.replace(',','').strip())

            print(C+' [!] Saving retrieved CENSYS data...')
            time.sleep(1)
            with open('tmp/logs/'+web+'-logs/'+web+'-censys-data.json', 'w+') as file:
                json.dump(resp.json(), file, ensure_ascii=True,indent=4)
                eq = os.getcwd()
                print(C+' [+] Censys Data stored '+eq+'/tmp/logs/'+web+'-logs/'+web+'-censys-data.json')

        else:
            print(R+' [-] Did not find any info about domain '+O+web+C)
            print(R+' [+] Try with another one...')
            save_data(database, module, lvl1, lvl2, lvl3, name, "Did not find any info about domain "+web)

    else:
        print(R+' [-] CENSYS API TOKENs not set!')
        print(R+' [-] This module cannot be used!')

def attack(web):
    web = web.fullurl
    censysdom(web)
