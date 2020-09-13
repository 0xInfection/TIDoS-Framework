#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import sys
import time
sys.path.append('files/')
import requests as wrn
from core.methods.tor import session
from lxml import etree
from collections import OrderedDict
from urllib.parse import urljoin
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

global actual_uri
actual_uri = []

info = "Depth 3 Crawler."
searchinfo = "Depth 3 Crawler"
properties = {"LIMIT":["Max. number of URLs to be crawled", " "]}

def crawler20x00(url, count):
    requests = session()
    visited_urls = set()
    queued_urls = OrderedDict({ url: '' })

    while len(queued_urls) > 0:
        (u, i) = queued_urls.popitem(last=False)
        try:
            req = requests.get(u, timeout=5)
            res = req.status_code
            root = etree.HTML(req.content, base_url=u)
        except wrn.ConnectionError as e:
            res = e
            continue
        except wrn.Timeout as e:
            res = e
            continue
        except wrn.TooManyRedirects as e:
            res = e
            continue
        except ValueError as e:
            res = e
            continue
        finally:
            visited_urls.add(u)
            pfx = "{}[{}]".format(i, len(visited_urls))
            if res == 200:
                print(B+' [+] Crawling : '+GR+pfx+'  '+C+u+G+'  ('+str(res)+')'+C+color.TR2+C)
                actual_uri.append(u)
            elif res == 404:
                print(B+' [+] Crawling : '+GR+pfx+'  '+C+u+R+'  ('+str(res)+')')
            else:
                print(B+' [+] Crawling : '+GR+pfx+'  '+C+u+O+'  ('+str(res)+')'+C)

        if root is None: continue

        for a in root.xpath('//a'):
            if (len(visited_urls) + len(queued_urls) >= count):
                break
            href = a.get('href')
            if href is None: continue
            (uj, sep, ui) = urljoin(a.base, href).partition('#')
            if uj not in visited_urls and uj not in queued_urls:
                if uj.startswith('http'):
                    queued_urls[uj] = pfx
            if (len(visited_urls) >= count):
                break

def out(web, list0):

    web = web.replace('http://','')
    web = web.replace('https://','')
    print(GR+' [*] Writing found URLs to DB...')
    print(C+' [!] Sorting only scope urls...')
    time.sleep(1)
    for lists in list0:
        if str(web) in lists:
            save_data(database, module, lvl1, lvl2, lvl3, name, str(lists))


def crawler3(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = "crawler3"
    global module
    module = "ScanANDEnum"
    global lvl1
    lvl1 = "Crawling"
    global lvl3
    lvl3 = ""
    try:
        time.sleep(0.5)

        #print(R+'\n    ==========================')
        #print(R+'     C R A W L E R  (Depth 3)')
        #print(R+'    ==========================')
        from core.methods.print import pscan
        pscan("crawler (depth 3)")
        time.sleep(0.7)
        print(C+' [This crawler will recursively crawl')
        print(C+' all the links of the website as well as all')
        print(C+'   links within each of the pages]\n')
        time.sleep(0.7)
        print(R+'  WARNING : Use this with CAUTION!\n')
        if properties["LIMIT"][1] == " ":
            m = input(GR+' [§] No. of links to be crawled (eg 100) :> ')
        else:
            m = properties["LIMIT"][1]
        print(O+' [!] Crawling limit set to :'+C+color.TR3+C+G+str(m)+C+color.TR2+C)
        w = int(m)
        crawler20x00(web, w)
        out(web, actual_uri)

    except Exception as e:
        print(R+' [-] Further crawl aborted due to Exception!')
        print(R+' [-] Exception : '+str(e))
        time.sleep(0.7)
        print(GR+' [*] Saving the links obtained...')
        out(web, actual_uri)
        print(G+' [+] Saved!'+C+color.TR2+C)

def attack(web):
    web = web.fullurl
    crawler3(web)