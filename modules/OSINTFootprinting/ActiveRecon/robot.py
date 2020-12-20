#!/usr/bin/env python3
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
from core.methods.tor import session
from time import sleep
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect


info = "Displays the robots.txt/sitemap.xml file of the target."
searchinfo = "Robot/Sitemap Printer"
properties = {}

def robot(web):
    name = targetname(web)
    lvl2 = "robot"
    module = "ReconANDOSINT"
    lvl1 = "Active Reconnaissance"
    lvl3 = ""
    requests = session()
    #print(R+'\n   =============================')
    #print(R+'    R O B O T S   C H E C K E R')
    #print(R+'   =============================\n')

    from core.methods.print import posintact
    posintact("robots checker") 

    url = web + '/robots.txt'
    print(' [!] Testing for robots.txt...\n')
    try:
        resp = requests.get(url).text
        m = str(resp)
        print(G+' [+] Robots.txt found!'+C+color.TR2+C)
        print(GR+' [*] Displaying contents of robots.txt...')
        print(color.END+m+C)
        data = ">> robots.txt:\n" + m
        save_data(database, module, lvl1, lvl2, lvl3, name, data)
    except Exception:
        print(R+' [-] Robots.txt not found')
        save_data(database, module, lvl1, lvl2, lvl3, name, "robots.txt not found.")

    print(' [!] Testing for sitemap.xml...\n')
    url0 = web + '/sitemap.xml'
    try:
        resp = requests.get(url0).text
        m = str(resp)
        print(G+' [+] Sitemap.xml found!'+C+color.TR2+C)
        print(GR+' [*] Displaying contents of sitemap.xml')
        print(color.END+m+C)
        data = ">> sitemap.xml:\n" + m
        save_data(database, module, lvl1, lvl2, lvl3, name, data)
    except Exception:
        print(R+' [-] Sitemap.xml not found')
        save_data(database, module, lvl1, lvl2, lvl3, name, "sitemap.xml not found.")

def attack(web):
    web = web.fullurl
    robot(web)
