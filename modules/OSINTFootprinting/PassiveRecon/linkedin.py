#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


try:
    from google import search
except Exception:
    from googlesearch import search
import time
import urllib.request
from random import randint
from time import sleep
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Use LinkedIn as information gathering resource."
searchinfo = "LinkedIn Gathering"
properties = {}

def getposts(web, lvl2, name):
    web0 = web
    if "@" in web0:
        web0 = web0.split("@")[1]
    site = str(web0)
    def clear_cookie():
        fo = open(".google-cookie", "w")
        fo.close()


    def google_it (dork, lvl2, name):
        clear_cookie()
        data = []
        module = "ReconANDOSINT"
        lvl1 = "Passive Reconnaissance & OSINT"
        lvl3=''
        for title in search(dork, stop=30):
            print(B+' [!] Profile Found :> '+C+title)
            data.append(title)
            time.sleep(0.5)
        save_data(database, module, lvl1, lvl2, lvl3, name, str(data))

    try:
        print(GR+" [*] Finding LinkedIn Employees ...\n")
        google_it("site:linkedin.com employees "+site+"", lvl2, name)
        print(O+' [!] Pausing to avoid captcha...'+C)
        time.sleep(10)

        print(GR+' [*] Finding Linkedin company profiles...\n')
        google_it("site:linkedin.com comapany "+site+"", lvl2, name)

    except urllib.error.HTTPError as err:
        if err.code == 503:
            print(R+' [-] Captcha appeared...\n')
            pass

def linkedin(web):
    name = targetname(web)
    lvl2=inspect.stack()[0][3]
    time.sleep(0.6)
    #print(R+'\n    =====================================')
    #print(R+'     L I N K E D I N   G A T H E R I N G')
    #print(R+'    =====================================\n')
    from core.methods.print import posintpas
    posintpas("linkedin gathering")
    getposts(web, lvl2, name)

def attack(web):
    web = web.fullurl
    linkedin(web)
