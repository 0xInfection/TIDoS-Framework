#!/usr/bin/env python
import requests
#import os
from core.colors import color
from database.database_module import save_data
import inspect

links = []

def revip(target):
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        site = host.name.replace('http://','').replace('https://','')
        print(' [!] Looking Up for Reverse IP Info...')
        print(' [~] Result : \n')
        text = requests.get('http://api.hackertarget.com/reverseiplookup/?q=' + site).text
        result = str(text)
        res = result.splitlines()
        if 'error' not in result:
            data = result
            save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
        elif 'error' in result:
            print(color.red(' [-] Outbound Query Exception!'))
    return

