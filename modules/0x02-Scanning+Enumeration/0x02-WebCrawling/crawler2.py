#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import os
import re
import time
import requests
import mechanize
import cookielib
from bs4 import BeautifulSoup
from core.Core.colors import *

br = mechanize.Browser()

cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [
    ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def out(web, totlist):
    web = web.replace('http://','')
    web = web.replace('https://','')
    print(GR+'\n [*] Writing found URLs to a file...')
    fil = open('tmp/logs/'+web+'-logs/'+web+'-spllinks.lst','w+')
    for lists in totlist:
        fil.write("%s\n" % lists)
    print()

def parseurl(address):
    addr = address.replace("http://",'').split("/")
    return addr

def externalcrawl(startpg):
    html = requests.get(startpg).text
    toparse = BeautifulSoup(html,"html.parser")
    extlinks = external(startpg, toparse, parseurl(startpg)[0])
    return extlinks

def internalcrawl(startpg):
    html = requests.get(startpg).text
    toparse = BeautifulSoup(html,"html.parser")
    intlinks = internal(startpg, toparse, parseurl(startpg)[0])
    return intlinks

def external(web, toparse, excurl):
    try:
        extlinks = []
        for link in toparse.findAll("a", href=re.compile("^(http|www)((?!"+excurl+").)*$")):
            if link.attrs['href'] is not None:
                if link.attrs['href'] not in extlinks:
                    lk = link.attrs['href']
                    if lk.startswith('http') == False:
                        lk = str(web) + str(lk)
                        extlinks.append(lk)
                        res = br.open(lk)
                        if str(res.code) == '200':
                            print(B+' [+] Crawling : '+C+str(lk)+G+' (200)')
                        elif str(res.code) == '404':
                            print(B+' [+] Crawling : '+C+str(lk)+R+' (404)')
                        else:
                            print(B+' [+] Crawling : '+C+str(lk)+O+' ('+str(res.code)+')')
    except Exception as e:
        print(R+' [-] Exception : '+str(e))
        pass

    return extlinks

def internal(web, toparse, incurl):
    try:
        intlinks = []
        for link in toparse.findAll("a", href=re.compile("^(/|.*"+incurl+")")):
            if link.attrs['href'] is not None:
                if link.attrs['href'] not in intlinks:
                    lk = link.attrs['href']
                    if lk.startswith('http') == False:
                        lk = str(web) + str(lk)
                        intlinks.append(lk)
                        res = br.open(lk)
                        if str(res.code) == '200':
                            print(B+' [+] Crawling : '+C+str(lk)+G+' (200)')
                        elif str(res.code) == '404':
                            print(B+' [+] Crawling : '+C+str(lk)+R+' (404)')
                        else:
                            print(B+' [+] Crawling : '+C+str(lk)+O+' ('+str(res.code)+')')

    except Exception as e:
        print(R+' [-] Exception : '+str(e))
        pass

    return intlinks

def crawler2(web):

    print(GR+' [*] Loading Level 2 Crawler...')
    time.sleep(0.6)
    totlinks = []
    print(R+'\n    =========================')
    print(R+'     C R A W L E R (Depth 2)')
    print(R+'    =========================')
    time.sleep(0.7)
    print(O+' [This module will fetch both ext. ')
    print(O+' and internal links from a website]\n')
    print(GR+' [*] Initiating the crawling...')
    time.sleep(0.7)
    try:
        print(O+' [*] Starting internal links gathering...')
        intlinks = internalcrawl(web)
        print(G+' [+] Finished internal links crawling...')
        print(O+'\n [*] Starting external links gathering...')
        extlinks = externalcrawl(web)
        print(G+' [+] Finished external links crawling...')

    except Exception as e:
        print(R+' [-] Exception : '+str(e))
        pass

    print(R+'   EXTERNAL LINKS')
    print(R+'  ================')
    print(O+'   |')

    for lenk in extlinks:
        print(GR+'   + '+lenk)

    print(R+'\n   INTERNAL LINKS')
    print(R+'  ================')
    print(O+'   |')

    for lenk in intlinks:
        print(GR+'   + '+O+lenk)
    totlinks = list(set(intlinks + extlinks))
    out(web, totlinks)
