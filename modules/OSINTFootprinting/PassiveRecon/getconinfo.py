#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


from core.methods.tor import session
import time
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Find domain contact info."
searchinfo = "Domain Contact Info"
properties = {}

def getconinfo(domain):
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl2 = inspect.stack()[0][3]
    lvl3 = ""
    name = targetname(domain)
    requests = session()
    web = domain
    if "@" in web:
        domain = domain.split("@")[1]
        if "https" in web:
            domain = "https://" + domain
        else:
            domain = "http://" + domain
    #print(R+'\n    =======================================')
    #print(R+'     D O M A I N   C O N T A C T   I N F O')
    #print(R+'    =======================================\n')
    from core.methods.print import posintpas
    posintpas("domain contact info")
    time.sleep(0.6)
    print(GR+' [*] Importing API Key...')
    try:
        from files.API_KEYS import FULLCONTACT_API_KEY
    except (IOError, ImportError):
        print(R+' [-] Error while importing key...')

    try:

        if FULLCONTACT_API_KEY != '':
            print(O+' [+] Found API Key :'+C+color.TR3+C+G+FULLCONTACT_API_KEY+C+color.TR2+C)
            base_url = 'https://api.fullcontact.com/v2/company/lookup.json'
            print(GR+' [*] Looking up info...')
            time.sleep(0.7)
            payload = {'domain':domain, 'apiKey':FULLCONTACT_API_KEY}
            resp = requests.get(base_url, params=payload)

            if resp.status_code == 200:

                print(G+' [+] Found domain info!'+C+color.TR2+C)
                w = resp.text.encode('ascii', 'ignore')
                result = resp.text
                quest = w.splitlines()
                print(O+' [!] Parsing info...'+C+'\n')
                print(R+' [+] REPORT :-\n')
                time.sleep(1)
                for q in quest:
                    q = q.replace('"','')
                    if ':' in q and '[' not in q and '{' not in q:
                        q1 = q.split(':',1)[0].strip().title()
                        q2 = q.split(':',1)[1].strip().replace(',','')
                        if q1.lower() == 'typeid' or q1.lower() == 'number' or q1.lower() == 'type':
                            print(C+'\n   [+] '+q1+' : '+GR+q2)
                        else:
                            print(C+'   [+] '+q1+' : '+GR+q2)
                        time.sleep(0.01)

                    elif ('{' or '[' in q) and (':' in q):
                        w1 = q.split(':',1)[0].strip().upper()
                        w2 = q.split(':',1)[1].strip()
                        if w1.lower() == 'keywords':
                            print(C+'\n   [+] '+w1+' : '+GR+w2)
                        else:
                            print(C+'\n [+] '+w1+' :-'+'\n')

                data = result
                save_data(database, module, lvl1, lvl2, lvl3, name, data)

            else:
                print(R+' [-] Did not find any info about domain '+O+domain+C)
                print(R+' [+] Try with another one...')
                save_data(database, module, lvl1, lvl2, lvl3, name, "Did not find any info about domain "+domain)

        else:
            print(R+' [-] FULL CONTACT API TOKEN not set!')
            print(R+' [-] This module cannot be used!')

    except Exception as e:
        print(R+' [-] Encountered Exception : '+str(e))

    print(G+'\n [+] Public Contact Info Module Completed!'+C+color.TR2+C+'\n')


def attack(web):
    web = web.fullurl
    getconinfo(web)
