#!/usr/bin/env python
from core.colors import color
from database.database_module import save_data
import inspect
import requests
# import os
import json
# import time

def censysdom(target):
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''    
        print(' [*] Importing API Key...')
        try:
            from files.API_KEYS import CENSYS_UID, CENSYS_SECRET
        except IOError as ImportError:
            print(color.red(' [-] Error while importing key...'))
        if '//' in host.name:
            web = host.name.split('//')[1]
        else:
            web = host.name
        if CENSYS_SECRET != '' and CENSYS_UID != '':
            print(color.green(' [+] Found Censys UID Key : ')+color.yellow(CENSYS_UID))
            print(color.green(' [+] Found Censys Secret Token : ')+color.yellow(CENSYS_SECRET))
            base_url = 'https://www.censys.io/api/v1'
            print(' [*] Looking up info...')

            resp = requests.get(base_url + "/view/websites/"+web, auth=(CENSYS_UID, CENSYS_SECRET))
            if 'quota_exceeded' in resp.text:
                print(color.red(' [-] Daily limit reached for this module. Use you own API key for CENSYS.'))
            if resp.status_code == 200:
                print(color.green(' [+] Found domain info!'))
                w = resp.text.encode('utf-8')
                asio = json.dumps(resp.json(), indent=4)
                data = asio.splitlines()
                print(color.yellow(' [!] Parsing info...\n'))
                #print(data)
                save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(data))
        #         for q in quest:
        #             q = q.replace('"','')
        #             if ':' in q and '[' not in q and '{' not in q:
        #                 q1 = q.split(':',1)[0].strip().title()
        #                 q2 = q.split(':',1)[1].strip().replace(',','')
        #                 print(C+'   [+] '+q1+' : '+GR+q2)
        #                 time.sleep(0.01)

        #             elif ('{' or '[' in q) and (':' in q):
        #                 w1 = q.split(':',1)[0].strip().upper()
        #                 w2 = q.split(':',1)[1].strip()
        #                 print(O+'\n [+] '+w1+' :-'+'\n')

        #             elif '{' not in q and '[' not in q and ']' not in q and '}' not in q:
        #                 print(GR+'   [+] '+q.replace(',','').strip())

        #         print(O+' [!] Saving retrieved CENSYS data...')
        #         time.sleep(1)
        #         with open('tmp/logs/'+web+'-logs/'+web+'-censys-data.json', 'w+') as file:
        #             json.dump(resp.json(), file, ensure_ascii=True,indent=4)
        #             eq = os.getcwd()
        #             print(G+' [+] Censys Data stored '+eq+'/tmp/logs/'+web+'-logs/'+web+'-censys-data.json')

            else:
                print(color.red(' [-] Did not find any info about domain '))
                print(color.red(' [+] Try with another one...'))

        else:
            print(color.red(' [-] CENSYS API TOKENs not set!'))
            print(color.red(' [-] This module cannot be used!'))
