#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


import builtwith
import json
from bs4 import BeautifulSoup
import time
#import requests
from core.methods.tor import session
from core.Core.colors import *

info = "This module tries to find out what technologies the target uses."
searchinfo = "Web Technology Fingerprinter"
properties = {}

def check0x00(domain):

    print(C+" [+] Domain : "+GR+domain)
    print(B+' [*] Fingerprinting web technologies...')
    resp = builtwith.parse(domain)
    print(C+' [*] Parsing raw-data...')
    time.sleep(0.7)
    res = json.dumps(resp)
    r = json.loads(res)
    print(G+' [+] Result :'+C+color.TR2+C+' \n')
    try:

        if "cdn" in r:
            print(G+' [+] Content Delivery Network:'+C+color.TR2+C)
            for p in r["cdn"]:
                print(C+'      '+p)
            print('')
            time.sleep(0.7)

        if "font-scripts" in r:
            print(G+' [+] Font-Script Source:'+C+color.TR2+C)
            for p in r["font-scripts"]:
                print(C+'      '+p)
            print('')
            time.sleep(0.7)

        if "widgets" in r:
            print(G+' [+] Widgets:'+C+color.TR2+C)
            for p in r["widgets"]:
                print(C+'      '+p)
            print('')
            time.sleep(0.7)

        if "web-frameworks" in r:
            print(G+' [+] Web Frameworks:'+C+color.TR2+C)
            for p in r["web-frameworks"]:
                print(C+'      '+p)
            print('')
            time.sleep(0.7)

        if "programming-languages" in r:
            print(G+' [+] Front-End Programming Languages:'+C+color.TR2+C)
            for p in r["programming-languages"]:
                print(C+'      '+p)
            print('')
            time.sleep(0.7)

        if "marketing-automation" in r:
            print(G+' [+] Marketing Automation Source:'+C+color.TR2+C)
            for p in r["marketing-automation"]:
                print(C+'      '+p)
            print('')
            time.sleep(0.7)

        if "mobile-frameworks" in r:
            print(G+' [+] Mobile Frameworks:'+C+color.TR2+C)
            for p in r["mobile-frameworks"]:
                print(C+'      '+p)
            print('')
            time.sleep(0.7)

        if "video-players" in r:
            print(G+' [+] In-Built Video Players:'+C+color.TR2+C)
            for p in r["video-players"]:
                print(C+'      '+p)
            print('')
            time.sleep(0.7)

    except Exception as e:
        print(R+' [-] Exception : '+str(e))

def apircv(web):
    requests = session()
    try:
        domain = web.replace('http://','')
        domain = web.replace('https://','')
        html = requests.get('http://w3techs.com/siteinfo.html?fx=y&url=' + domain).text
        soup = BeautifulSoup(html, 'lxml')
        table = soup.findAll('table', attrs={'class':'w3t_t'})[0]
        trs = table.findAll('tr')

        for tr in trs:
            th = tr.find('th')
            td = tr.find('td').text

            if td[-7:] == 'more...':
                td = td[:-9]

            print(G+' [+] '+th.text+':'+C+color.TR2+C)
            print(C+'      '+td+'\n')
            time.sleep(0.7)
    except:
        print(R+' [-] Outbound Query Exception!')

def webtech(web):

    #print(R+'\n    =================================')
    #print(R+'     W E B   T E C H N O L O G I E S')
    #print(R+'    =================================\n')

    from core.methods.print import pscan
    pscan("web technologies")

    check0x00(web)
    apircv(web)
    print(C+' [+] Fingerprinting Done!')

def attack(web):
    web = web.fullurl
    webtech(web)