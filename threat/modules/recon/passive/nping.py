#!/usr/bin/env python
import requests
from core.colors import color

def nping(target):
     for t in target:
        site = t.name.replace('http://','').replace('https://','')
        text = requests.get('http://api.hackertarget.com/nping/?q=' + site).text
        nping = str(text)
        if 'error' not in nping:
            print(color.white(nping))
        else:
            print(color.red(' [-] Outbound Query Exception!'))