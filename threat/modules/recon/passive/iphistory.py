#!/usr/bin/env python
import requests
from bs4 import *
import time
import lxml
import urllib3
import json
from core.colors import color

def iphistory(target):
    for t in target:
        site = t.name.replace('http://','').replace('https://','')
        try:
            web0 = site.split('/')[-1]
            print(' [!] Making the request...')
            html = requests.get('https://viewdns.info/iphistory/?domain=' + web0).text
            print(' [*] Parsing raw-data...')
            soup = BeautifulSoup(html,'lxml')
            print(soup)
            print(' [!] Setting parameters...')
            table = soup.findAll('table', attrs={'border':'1'})[0]
            print(' [!] Finding IP history instances...')
            trs = table.findAll('tr')
            trs.pop(0)

            print('\n [+] Following instances were found...')

            for tr in trs:
                td = tr.findAll('td')
                info = {'ip' : td[0].text, 'owner' : td[2].text.rstrip(), 'last' : td[3].text}
                print(color.green(' [+] Instance : ') + color.blue(info['ip']) + color.white(' => ' + info['owner']) + color.blue(' - (' + info['last'] + ')'))
        except:
            print(color.red(' [-] No instances of IP History found...'))
            pass