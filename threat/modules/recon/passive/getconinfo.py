#!/usr/bin/env python
from core.colors import color
from database.database_module import save_data
import requests
import time
import inspect

def getconinfo(target):
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        print(color.white(' [*] Importing API Key...'))
        try:
            from files.API_KEYS import FULLCONTACT_API_KEY
        except (IOError, ImportError):
            print(color.red(' [-] Error while importing key...'))
        pass
        try:

            if FULLCONTACT_API_KEY != '':
                print(color.green(' [+] Found API Key : ')+color.yellow(FULLCONTACT_API_KEY))
                base_url = 'https://api.fullcontact.com/v2/company/lookup.json'
                print(color.white(' [*] Looking up info...'))
                time.sleep(0.7)
                payload = {'domain':host.name, 'apiKey':FULLCONTACT_API_KEY}
                resp = requests.get(base_url, params=payload)
                #print(resp)
                if resp.status_code == 200:
                    data = resp.text
                    save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
                else:
                    print(color.red(' [-] Did not find any info about domain ')+color.yellow(host.name))
                    print(color.red(' [+] Try with another one...'))
            else:
                print(color.red(' [-] FULL CONTACT API TOKEN not set!'))
                print(color.red(' [-] This module cannot be used!'))
        except Exception as e:
            pass
            print(color.red(' [-] Encountered Exception : '+str(e)))