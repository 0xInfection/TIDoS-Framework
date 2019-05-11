#!/usr/bin/env python
import requests
from core.colors import color

def subnet(target):
    for t in target:
        site = t.name.replace('http://','').replace('https://','')
        print(color.green(' [!] Enumerating subnets in network...'))
        print('[*] Getting subnet class infos...\n')
        text = requests.get('http://api.hackertarget.com/subnetcalc/?q=' + site).text
        http = str(text)
        if 'error' not in http:
            result = http.splitlines()
            for r in result:
                print(color.green(' '+r.split('=')[0]+'='+color.yellow(r.split('=')[1])))
        elif 'No results found' in http:
            print(color.red(' [-] No results found!'))
        else:
            print(color.red(' [-] Outbound Query Exception!'))
