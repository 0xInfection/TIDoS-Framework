#!/usr/bin/env python3
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


import time
from core.methods.tor import session
from time import sleep
from core.Core.colors import *

info = "Displays the robots.txt/sitemap.xml file of the target."
searchinfo = "Robot/Sitemap Printer"
properties = {}

def robot(web):
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
    except:
        print(R+' [-] Robots.txt not found')

    print(' [!] Testing for sitemap.xml...\n')
    url0 = web + '/sitemap.xml'
    try:
        resp = requests.get(url0).text
        m = str(resp)
        print(G+' [+] Sitemap.xml found!'+C+color.TR2+C)
        print(GR+' [*] Displaying contents of sitemap.xml')
        print(color.END+m+C)
    except:
        print(R+' [-] Sitemap.xml not found')

def attack(web):
    robot(web)