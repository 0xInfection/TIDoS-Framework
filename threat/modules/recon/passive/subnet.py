#!/usr/bin/env python
import requests
from core.colors import color
from database.database_module import save_data
import inspect

def subnet(target):
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        site = host.name.replace('http://','').replace('https://','')
        print(color.green(' [!] Enumerating subnets in network...'))
        print('[*] Getting subnet class infos...\n')
        text = requests.get('http://api.hackertarget.com/subnetcalc/?q=' + site).text
        http = str(text)
        if 'error' not in http:
            data = http
            # result = http.splitlines()
            # for data in result:
            save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
        elif 'No results found' in http:
            print(color.red(' [-] No results found!'))
        else:
            print(color.red(' [-] Outbound Query Exception!'))
    return