#!/usr/bin/env python
import os
import time
import requests
from core.colors import color
from database.database_module import save_data
import inspect
links = []

def revdns(target):
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        site = host.name.replace('http://','').replace('https://','')
        print('[!] Looking Up for Reverse DNS Info...')
        print(' [~] Result: \n')
        text = requests.get('http://api.hackertarget.com/reversedns/?q=' + site).text
        result = str(text)
        res = result.splitlines()
        if 'error' not in res and 'no' != res[0]:
            data = result
            save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
        else:
            print(color.red(' [-] No result found!'))
    return

