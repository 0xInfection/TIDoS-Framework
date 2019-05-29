#!/usr/bin/env python
from modules.recon.passive.gsearch import gsearch
import time
import requests
from random import randint
from time import sleep
from core.colors import color
from database.database_module import save_data
import inspect

def linkedin(target):
    for host in target:
        site = host.name.replace('http://','').replace('https://','').replace('www.','').replace('.com','')
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        def clear_cookie():
            fo = open(".google-cookie", "w")
            fo.close()

        def google_it(host):
            clear_cookie()
            try:
                this = gsearch(host)
                if len(this)>0:
                    data=str(this)
                    #print(data)
                    save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
                    time.sleep(5)
            except Exception as data:
                save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
                pass

        try:
            print(" [*] Finding LinkedIn Employees ...\n")
            host.dork = "site:linkedin.com employees "+site+""

            google_it(host)
            print(color.yellow(' [!] Pausing to avoid captcha...'))
            time.sleep(10)

            print(' [*] Finding Linkedin company profiles...\n')
            host.dork = "site:linkedin.com company "+site+""

            google_it(host)

        except requests.HTTPError as err:
            if err.code == 503:
                print(color.red(' [-] Captcha appeared...\n'))
                pass
    return
