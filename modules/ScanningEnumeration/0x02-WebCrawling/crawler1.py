#!/usr/bin/env python3
# -*- coding : utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
#import requests
from core.methods.tor import session
import core.lib.mechanize as mechanize
import http.cookiejar
from urllib.request import urlparse
import time
from time import sleep
from core.Core.colors import *
from core.variables import tor

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

br = mechanize.Browser()

cj = http.cookiejar.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

torproxies = {'http':'socks5h://localhost:9050', 'https':'socks5h://localhost:9050'}
if tor:
    br.set_proxies(torproxies)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [
    ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

linksall = []
cis = []
crawled = []

info = "Depth 1 Crawler."
searchinfo = "Depth 1 Crawler"
properties = {}

def crawler10x00(web):
    requests = session()
    time.sleep(0.5)
    #print(R+'\n    ===========================')
    #print(R+'     C R A W L E R  (Depth 1)')
    #print(R+'    ==========================\n')
    from core.methods.print import pscan
    pscan("crawler (depth 1)")
    print(C+' [This module will fetch all links')
    print(C+' from an online API and then crawl ')
    print(C+'         them one by one]      ')
    time.sleep(0.4)
    print(''+GR+' [*] Parsing the web URL... ')
    time.sleep(0.3)
    print('' +B+ ' [!] URL successfully parsed...')
    print('' + GR+ ' [*] Getting links...')
    time.sleep(0.4)
    text = requests.get('http://api.hackertarget.com/pagelinks/?q=' + web).text
    lol = str(text)
    linksall = lol.splitlines()
    for m in linksall:
        if 'http' in m and 'https' not in m:
            cis.append(m)

    flag = 0x00
    for x in cis:
        try:
            print(O+' [+] Crawling link :>'+ C+color.TR3+C+G + str(x)+C+color.TR2+C)
            br.open(x)
            flag = 0x01
            crawled.append(x)

        except Exception as e:
            print(R+' [-] Exception : '+str(e)+'\n')

    if flag == 0x00:
        print(R+' [-] Unable to find any links...')
        print(C+' [+] Please use the second crawler... :)')

    return crawled

def out(web, list0):

    web = web.split('//')[1]
    print(GR+' [*] Writing found URLs to DB...')
    #if os.path.exists('tmp/logs/'+web+'-logs/'+web+'-links.lst'):
    #    fil = open('tmp/logs/'+web+'-logs/'+web+'-links.lst','w+')
    print(P+' [!] Sorting only scope urls...'+C)
    time.sleep(1)
    for lists in list0:
        if str(web) in lists:
            save_data(database, module, lvl1, lvl2, lvl3, name, str(lists))


def crawler1(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = "crawler1"
    global module
    module = "ScanANDEnum"
    global lvl1
    lvl1 = "Crawling"
    global lvl3
    lvl3 = ""
    time.sleep(0.5)
    q = crawler10x00(web)
    out(web, q)
    print(G+' [+] Done!'+C+color.TR2+C)

def attack(web):
    web = web.fullurl
    crawler1(web)