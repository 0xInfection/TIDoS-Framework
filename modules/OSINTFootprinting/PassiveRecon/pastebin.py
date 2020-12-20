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

info = "Find Pastebin posts."
searchinfo = "Find Pastebin posts."
properties = {}

def getposts(web, name, lvl2):
    web0 = web
    if "@" in web0:
        web0 = web0.split("@")[1]
    site = str(web0)
    def clear_cookie():
        fo = open(".google-cookie", "w")
        fo.close()


    def google_it (dork, name, lvl2):
        clear_cookie()
        data = []
        module = "ReconANDOSINT"
        lvl1 = "Passive Reconnaissance & OSINT"
        lvl3=''
        for title in search(dork, stop=30):
            print(B+' [!] Post Found :> '+C+title)
            data.append(title)
            time.sleep(0.5)
        save_data(database, module, lvl1, lvl2, lvl3, name, str(data))

    try:
        print(C+" [*] Finding Pastebin posts ...\n")
        google_it("site:pastebin.com intext:"+site+"", name, lvl2)

    except urllib.error.HTTPError as err:
        if err.code == 503:
            print(R+' [-] Captcha appeared...\n')
            pass

def pastebin(web):
    name = targetname(web)
    lvl2=inspect.stack()[0][3]
    time.sleep(0.6)
    #print(R+'\n    =============================')
    #print(R+'     P A S T E B I N   P O S T S')
    #print(R+'    =============================\n')
    from core.methods.print import posintpas
    posintpas("pastebin posts")
    getposts(web, name, lvl2)

def attack(web):
    web = web.fullurl
    pastebin(web)
