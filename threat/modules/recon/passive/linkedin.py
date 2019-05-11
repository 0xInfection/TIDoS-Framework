#!/usr/bin/env python
from modules.recon.passive.gsearch import gsearch
import time
import requests
from random import randint
from time import sleep
from core.colors import color

def linkedin(target):
    for t in target:
        site = t.name.replace('http://','').replace('https://','')
    def clear_cookie():
        fo = open(".google-cookie", "w")
        fo.close()


    def google_it (dork):
        clear_cookie()
        try:
            for title in gsearch(dork):
                print(color.blue(' [!] Profile Found :> '+color.white(title)))
        except Exception as e:
            pass

    try:
        print(" [*] Finding LinkedIn Employees ...\n")
        google_it("site:linkedin.com employees "+site+"")
        print(color.yellow(' [!] Pausing to avoid captcha...'))
        time.sleep(10)

        print(' [*] Finding Linkedin company profiles...\n')
        google_it("site:linkedin.com comapany "+site+"")

    except requests.HTTPError as err:
        if err.code == 503:
            print(color.red(' [-] Captcha appeared...\n'))
            pass
