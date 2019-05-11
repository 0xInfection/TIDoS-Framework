#!/usr/bin/env python
import requests
import socket
from core.colors import color

def getgeoip(target):
     for t in target:
        site = t.name.replace('http://','').replace('https://','')
        domains = socket.gethostbyname(t.name)
        text = requests.get('http://api.hackertarget.com/geoip/?q=' + domains).text
        result = str(text)
        if 'error' not in result and 'invalid' not in result:
            res = result.splitlines()
            for r in res:
                print(color.white(' [+] ' + r.split(':')[0].strip() + ' : ' +color.yellow(r.split(':')[1].strip())))
        else:
            print(color.red(' [-] Outbound Query Exception!'))