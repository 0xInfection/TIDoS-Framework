#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import re
import os
import sys
import time
import urllib3
import urllib.parse
import requests as wrn
from core.methods.tor import session
from core.Core.colors import *
from modules.VlnAnalysis.Severe.subdom0x00 import subdom0x00
from modules.VlnAnalysis.Severe.signatures import services
from requests.packages.urllib3.exceptions import InsecureRequestWarning
wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module searches for possibilities of subdomain takeovers, either for a single subdomain, or for all of them."
searchinfo = "Subdomain Takeover Module"
properties = {"SUBDOM":["Subdomain to attack in single mode", " "]}

def getReq0x00(url):
    requests = session()
    print(GR+' [*] Setting headers...')
    headers = {
                    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                    'Accept-Language':'en-US;',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;',
                    'Connection':'close'
            }

    try:
        print(O+' [!] Making the no-verify request...')
        req = requests.get(url=url, headers=headers, timeout=7, allow_redirects=False, verify=False)
        return req.status_code,req.content

    except Exception as e:
        print(R+' [-] Exception : '+str(e))
        pass

    return None, None

def check0x00(status,content):

    code = ""
    error = ""

    print(GR+' [*] Searching through signatures...')
    time.sleep(0.7)
    for service in services:
        values = services[service]

        for value in values:
            stfu = services[service][value]
            if value == 'error':
                error = stfu
            if value == 'code':
                code = stfu

        if re.search(code,str(status),re.I) and re.search(error,str(content),re.I):
            return service,error

    return None, None

def subdomover(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = inspect.stack()[0][3]
    global module
    module = "VulnAnalysis"
    global lvl1
    lvl1 = "Critical Vulnerabilities"
    global lvl3
    lvl3 = ""
    #print(R+'\n    =====================================')
    #print(R+'\n     S U B D O M A I N   T A K E O V E R ')
    #print(R+'    ---<>----<>----<>----<>----<>----<>--\n')

    from core.methods.print import pvln
    pvln("subdomain takeover") 
                 

    time.sleep(0.6)
    print(O+' Choose from the following:\n')
    print(B+'  [1] '+C+'Single Subdomain '+W+'(Manual)')
    print(B+'  [2] '+C+'All Subdomains '+W+'(Automated)')
    v = input(O+'\n [§] Enter type :> '+GR)

    if v.strip() == '1':
        if properties["SUBDOM"][1] == " ":
            su = input(C+' [§] Enter the subdomain :> '+GR)
        else:
            su = properties["SUBDOM"][1]
        if su.startswith('http'):
            pass
        else:
            su = 'http://'+su
        time.sleep(0.7)
        print(O+' [!] Starting enumeration...')
        time.sleep(0.8)
        print(R+' [+] Target Locked : '+O+su)
        status,content = getReq0x00(su)
        service,error = check0x00(status,content)
        print(B+' [!] Error : '+C+str(error))
        print(B+' [!] Service Status : '+C+str(status))
        print(GR+' [*] Analysing vulnerability...')
        if service and error:
            time.sleep(0.5)
            print(G+' [+] Potential subdomain takeover was found!')
            print(G+' [+] Service Identified : '+O+str(service))
            data = "Potential subdomain takeover @ " + su + "\nService: " + str(service)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
        else:
            time.sleep(0.5)
            print(R+' [-] No subdomain takeover possible for '+O+su)
            data = "No takeover possible for " + su
            save_data(database, module, lvl1, lvl2, lvl3, name, data)

    elif v.strip() == '2':

        print(C+' [*] Starting enumeration...')
        time.sleep(0.5)
        web0 = web.replace('http://','')
        web0 = web.replace('https://','')
        if "@" in web0:
            web0 = web0.split("@")[1]
        if not os.path.exists('tmp/logs/'+web0+'-logs/'):
            os.makedirs('tmp/logs/'+web0+'-logs/')

        try:
            print(GR+' [+] Searching for subdomains file...')
            if os.path.exists('tmp/logs/'+web0+'-logs/'+web0+'-subdomains.lst'):
                pass
            else:
                print(R+' [-] Subdomains file not found!')
                print(GR+' [*] Initializing sub-domain gathering...')
                subdom0x00(web)

        except Exception as e:
            print(R+' [-] Exception occured!')
            print(R+' [-] Error : '+str(e))

        with open('tmp/logs/'+web0+'-logs/'+web0+'-subdomains.lst') as sub_domain_list:
            for sub_domain in sub_domain_list:
                print(GR+' [*] Parsing sub-domain...')
                sub_domain = sub_domain.replace('\n','')
                if sub_domain.startswith('http'):
                    pass
                else:
                    if 'http://' in web:
                        sub_domain = 'http://' + sub_domain
                    elif 'https://' in web:
                        sub_domain = 'https://' + sub_domain

                print(O+'\n [+] Target Url :> '+C+sub_domain)
                status,content = getReq0x00(sub_domain)
                service,error = check0x00(status,content)
                print(B+' [!] Error : '+C+str(error))
                print(B+' [!] Service Status : '+C+str(status))
                print(GR+' [*] Analysing vulnerability...')
                if service and error:
                    time.sleep(0.5)
                    print(G+' [+] Potential subdomain takeover was found!')
                    print(G+' [+] Service Identified : '+O+str(service))
                    data = "Potential subdomain takeover @ " + sub_domain + "\nService: " + str(service)
                    save_data(database, module, lvl1, lvl2, lvl3, name, data)
                else:
                    time.sleep(0.5)
                    print(R+' [-] No subdomain takeover possible for '+O+sub_domain)
                    data = "No takeover possible for " + sub_domain
                    save_data(database, module, lvl1, lvl2, lvl3, name, data)

    else:
        print(W+' [-] U high dude?')
        time.sleep(1)

    print(G+' [+] Subdomain takeover module completed!')

def attack(web):
    web = web.fullurl
    subdomover(web)
