#!/usr/bin/env python
from core.colors import color
from database.database_module import save_data
import inspect
import requests, time
from time import sleep

def robot(target):
    from core.build_menu import buildmenu
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        if '//' in host.name:
            site = host.name
        else:
            site = 'https://'+host.name
        url = site + '/robots.txt'
        print(' [!] Testing for robots.txt...\n')
        try:
            resp = requests.get(url).text
            m = str(resp)
            print(color.yellow(' [+] Robots.txt found!'))
            print(color.green(' [*] Saving contents of robots.txt...'))
            data = m
            save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(data))
            #print(m)
        except:
            print(color.red(' [-] Robots.txt not found'))

        print(' [!] Testing for sitemap.xml...\n')
        url0 = site + '/sitemap.xml'
        try:
            resp = requests.get(url0).text
            m = str(resp)
            print(color.yellow(' [+] Sitemap.xml found!'))
            print(color.green(' [*] Saving contents of sitemap.xml'))
            data=m
            save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(data))
        except:
            print(color.red(' [-] Sitemap.xml not found'))
        time.sleep(2)
        buildmenu(target,target[0].main_menu,'Main Menu','')
