#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


#import requests
import time
import re
import socket
import core.lib.mechanize as mechanize
import http.cookiejar
from urllib.parse import urlencode
from re import search
from core.Core.colors import *
from core.variables import tor
from core.methods.tor import session
from modules.OSINTFootprinting.ActiveRecon.serverdetect import serverdetect
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

info = "This module searches for Cloudflare misconfigurations and tries to bypass protections."
searchinfo = "Cloudflare Misconfig & Bypass"
properties = {"BYPASS":["Bypass Cloudflare if present [1/0]", " "]}

def cloud0x00(web):
    requests = session()
    web = web.replace('https://','')
    web = web.replace('http://','')
    #print(R+'\n   =========================================')
    #print(R+'\n    C L O U D F L A R E   M I S C O N F I G.')
    #print(R+'   ---<>----<>----<>----<>----<>----<>----<>\n')

    from core.methods.print import pvln
    pvln("cloudflare misconfig.") 
                
    time.sleep(0.4)
    print(GR+' [*] Checking server status...')
    try:
        ip_addr = socket.gethostbyname(web)
        print(G+' [+] Server detected online...')
        time.sleep(0.5)
        print(G+' [+] Server IP :> '+O+ip_addr)
    except Exception:
        print(R+' [-] Server seems down...')

    print(GR+' [*] Trying to identify backend...')
    time.sleep(0.4)
    web = 'http://' + web
    try:
        print(GR+' [*] Making the no-verify request...')
        time.sleep(0.6)
        r = requests.get(web, verify=False)
        header = r.headers['Server']
        if 'cloudflare' in header:
            print(O+' [+] The website is behind '+R+'Cloudflare.')
            print(G+' [+] Server : Cloudflare')
            time.sleep(0.4)
            if properties["BYPASS"][1] == " ":
                m = input(O+' [+] Do you want TIDoS to try and bypass Cloudflare? (enter if not) :> ')
                byp = m != ""
            else:
                byp = properties["BYPASS"][1] == "1"
            if byp:
                bypass(web)
            else:
                print(R+' [-] Invalid choice...')
                serverdetect(web)
            try:
                ip_addr = bypass.ip_addr
            except Exception:
                pass
        else:
            print(R+' [-] Website does not seem to be a part of Cloudflare Network...')
    except Exception:
        print(R+' [-] Failed to identify server.\n [-] Some error occured!')
        pass

def bypass(domain):

    print(GR+' [*] Trying to get real IP...')
    post = urlencode({'cfS': domain})
    result = br.open(
        'http://www.crimeflare.info/cgi-bin/cfsearch.cgi ', post).read()

    match = search(r' \b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', result)
    if match:
        bypass.ip_addr = match.group().split(' ')[1][:-1]
        print(G+' [+] Cloudflare found misconfigured!')
        time.sleep(0.4)
        print(GR+' [*] Identifying IP...')
        time.sleep(0.5)
        print(G+' [+] Real IP Address : ' + bypass.ip_addr + '\n')
        save_data(database, module, lvl1, lvl2, lvl3, name, "Cloudflare misconfigured! IP address: {}".format(bypass.ip_addr))
    else:
        print(R+' [-] Cloudflare properly configured...')
        print(R+' [-] Unable to find remote IP!\n')
        save_data(database, module, lvl1, lvl2, lvl3, name, "Cloudflare properly configured.")
        pass

def cloudflaremisc(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = inspect.stack()[0][3]
    global module
    module = "VulnAnalysis"
    global lvl1
    lvl1 = "Basic Bugs & Misconfigurations"
    global lvl3
    lvl3 = ""
    time.sleep(0.5)
    cloud0x00(web)

def attack(web):
    web = web.fullurl
    cloudflaremisc(web)
