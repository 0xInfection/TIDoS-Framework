#!/usr/bin/env python
import requests
from bs4 import *
import time
import lxml
import urllib3
import json
from core.colors import color
from database.database_module import save_data
import inspect

def iphistory(target):
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        site = host.name.replace('http://','').replace('https://','')
        try:
            web0 = site.split('/')[-1]
            print(' [!] Making the request...')
            html = requests.get('https://viewdns.info/iphistory/?domain=' + web0).text
            print(' [*] Parsing raw-data...')
            soup = BeautifulSoup(html,'lxml')
            if 'captcha?' in str(soup).lower():
                print(color.red(' [-] CAPTCHA detected, this method won\'t work...'))
                break
            #print(soup)
            print(' [!] Setting parameters...')
            table = soup.findAll('table', attrs={'border':'1'})[0]
            print(' [!] Finding IP history instances...')
            trs = table.findAll('tr')
            trs.pop(0)
            print('\n [+] Following instances were found...')
            data=[]
            for tr in trs:
                td = tr.findAll('td')
                info = {'ip' : td[0].text, 'owner' : td[2].text.rstrip(), 'last' : td[3].text}
                data.append(info)
                #print(color.green(' [+] Instance : ') + color.blue(info['ip']) + color.white(' => ' + info['owner']) + color.blue(' - (' + info['last'] + ')'))
            save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
        except:
            print(color.red(' [-] No instances of IP History found...'))
            pass