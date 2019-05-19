#!/usr/bin/env python
import requests
import socket
from core.colors import color
from database.database_module import save_data
import inspect

def getgeoip(target):
     for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        site = host.name.replace('http://','').replace('https://','')
        domains = socket.gethostbyname(host.name)
        text = requests.get('http://api.hackertarget.com/geoip/?q=' + domains).text
        result = str(text)
        if 'error' not in result and 'invalid' not in result:
            data = result
            save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
            # res = result.splitlines()
            # for r in res:
            #     print(color.white(' [+] ' + r.split(':')[0].strip() + ' : ' +color.yellow(r.split(':')[1].strip())))
        else:
            print(color.red(' [-] Outbound Query Exception!'))