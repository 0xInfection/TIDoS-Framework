#!/usr/bin/env python
import requests
from core.colors import color
from database.database_module import save_data
import inspect

def nping(target):
     for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        site = host.name.replace('http://','').replace('https://','')
        text = requests.get('http://api.hackertarget.com/nping/?q=' + site).text
        data = str(text)
        if 'error' not in data:
            save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
        else:
            print(color.red(' [-] Outbound Query Exception!'))