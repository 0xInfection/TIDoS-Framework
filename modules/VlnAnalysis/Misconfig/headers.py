#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import http.client
import urllib
import sys
import datetime
import ssl
import time
import os
import requests
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module analyzes the target's HTTP Headers (HSTS etc.)"
searchinfo = "HTTP Header Analysis"
properties = {}

def referrerpol0x00(headx):
    for header in headx:
        if "Referrer-Policy:".lower() in header.lower():
            print("\033[1;32m [+]\033[0m Detected Referrer-Policy - '" + header.rstrip() + "' \033[1;32m(OK)\033[0m")
            save_data(database, module, lvl1, lvl2, lvl3, name, "Detected Referrer-Policy - " + header.rstrip())
            return
    save_data(database, module, lvl1, lvl2, lvl3, name, "Referrer-Policy not present.")
    print("\033[1;31m [-]\033[0m Referrer-Policy not present \033[1;31m(Not OK)\033[0m")

def xframe0x00(headx):
    for header in headx:
        if "X-Frame-Options:".lower() in header.lower():
            save_data(database, module, lvl1, lvl2, lvl3, name, "Detected X-Frame-Options - " + header.rstrip())
            print("\033[1;32m [+]\033[0m Detected X-Frame-Options - '" + header.rstrip() + "' \033[1;32m(OK)\033[0m")
            return
    save_data(database, module, lvl1, lvl2, lvl3, name, "X-Frame-Options not present.")
    print("\033[1;31m [-]\033[0m X-Frame-Options not present \033[1;31m(Not OK)\033[0m")

def contentsec0x00(headx):
    detected = False
    for header in headx:
        if "Content-Security-Policy:".lower() in header.lower():
            save_data(database, module, lvl1, lvl2, lvl3, name, "Detected Content-Security-Policy - " + header.rstrip())
            print("\033[1;32m [+]\033[0m Detected Content-Security-Policy - '" + header.rstrip() + "' \033[1;32m(OK)\033[0m")
            detected = True
        if "X-Webkit-CSP:".lower() in header.lower():
            save_data(database, module, lvl1, lvl2, lvl3, name, "Detected X-Webkit-CSP - " + header.rstrip())
            print("\033[1;32m [+]\033[0m Detected X-Webkit-CSP - '" + header.rstrip() + "' \033[1;32m(OK)\033[0m")
            detected = True
        if "X-Content-Security-Policy:".lower() in header.lower():
            save_data(database, module, lvl1, lvl2, lvl3, name, "Detected X-Content-Security-Policy - " + header.rstrip())
            print("\033[1;32m [+]\033[0m Detected X-Content-Security-Policy - '" + header.rstrip() + "' \033[1;32m(OK)\033[0m")
            detected = True

        if "Content-Security-Policy-Report-Only:".lower() in header.lower():
            save_data(database, module, lvl1, lvl2, lvl3, name, "Detected Content-Security-Policy in report only - " + header.rstrip())
            print("\033[1;33m [I]\033[0m Detected Content-Security-Policy in report only - '" + header.rstrip() + "' \033[1;33m(Informational)\033[0m")
            detected = True
        if "X-Webkit-CSP-Report-Only:".lower() in header.lower():
            save_data(database, module, lvl1, lvl2, lvl3, name, "Detected X-Webkit-CSP in report only - " + header.rstrip())
            print("\033[1;33m [I]\033[0m Detected X-Webkit-CSP in report only - '" + header.rstrip() + "' \033[1;33m(Informational)\033[0m")
            detected = True
        if "X-Content-Security-Policy-Report-Only:".lower() in header.lower():
            save_data(database, module, lvl1, lvl2, lvl3, name, "Detected X-Content-Security-Policy in report only - " + header.rstrip())
            print("\033[1;33m [I]\033[0m Detected X-Content-Security-Policy in report only  - '" + header.rstrip() + "' \033[1;33m(Informational)\033[0m")
            detected = True

    if detected is True:
        return
    else:
        save_data(database, module, lvl1, lvl2, lvl3, name, "Content-Security-Policy not present.")
        print("\033[1;31m [-]\033[0m Content-Security-Policy not present \033[1;31m(Not OK)\033[0m")

def xssprotect0x00(headx):
    for header in headx:
        if "X-XSS-Protection:".lower() in header.lower():
            save_data(database, module, lvl1, lvl2, lvl3, name, "Detected X-XSS-Protection - " + header.rstrip())
            print("\033[1;32m [+]\033[0m Detected X-XSS-Protection - '" + header.rstrip() + "' \033[1;32m(OK)\033[0m")
            return
    save_data(database, module, lvl1, lvl2, lvl3, name, "X-XSS-Protection not present.")
    print("\033[1;31m [-]\033[0m X-XSS-Protection not present \033[1;31m(Not OK)\033[0m")

def xcontenttype0x00(headx):
    for header in headx:
        if "X-Content-Type-Options:".lower() in header.lower():
            save_data(database, module, lvl1, lvl2, lvl3, name, "Detected X-Content-Type-Options - " + header.rstrip())
            print("\033[1;32m [+]\033[0m Detected X-Content-Type-Options - '" + header.rstrip() + "' \033[1;32m(OK)\033[0m")
            return
    save_data(database, module, lvl1, lvl2, lvl3, name, "X-Content-Type-Options not present.")
    print("\033[1;31m [-]\033[0m X-Content-Type-Options not present \033[1;31m(Not OK)\033[0m")

def general0x00(headx):
    serverversion = ""
    for header in headx:
        if "Server: ".lower() in header.lower() and header.startswith("Server:"):
            save_data(database, module, lvl1, lvl2, lvl3, name, "(info) Detected Server header - " + header.rstrip())
            print("\033[1;33m [I]\033[0m Detected Server header - '" + header.rstrip() + "' \033[1;33m(Informational)\033[0m")
            serverversion = header
        if "ETag: ".lower() in header.lower():
            if "Apache".lower() in serverversion.lower():
                save_data(database, module, lvl1, lvl2, lvl3, name, "(info) Detected ETag Apache - " + header.rstrip())
                print("\033[1;33m [I]\033[0m Detected ETag Apache - '" + header.rstrip() + "' \033[1;33m(Informational)\033[0m")
            else:
                save_data(database, module, lvl1, lvl2, lvl3, name, "(info) Possible ETag - " + header.rstrip())
                print("\033[1;34m [I]\033[0m Possible ETag - '" + header.rstrip() + "' \033[1;34m(Possible Informational)\033[0m")
        if "X-Powered-By: ".lower() in header.lower():
            save_data(database, module, lvl1, lvl2, lvl3, name, "(info) Detected X-Powered-By - " + header.rstrip())
            print("\033[1;33m [I]\033[0m Detected X-Powered-By - '" + header.rstrip() + "' \033[1;33m(Informational)\033[0m")

def seccheck0x00(headx):
    headerlist = ''.join(headx)
    if "Strict-Transport-Security:".lower() in headerlist.lower():
        #HSTSHeader = filter(lambda y: 'Strict-Transport-Security' in y,headx)
        save_data(database, module, lvl1, lvl2, lvl3, name, "Detected Strict-Transport-Security")
        print("\033[1;32m [+]\033[0m Detected Strict-Transport-Security \033[1;32m(OK)\033[0m")
        #print("\033[1;32m [+]\033[0m Detected Strict-Transport-Security - " + HSTSHeader[0].rstrip() + "' \033[1;32m(OK)\033[0m")
    else:
        save_data(database, module, lvl1, lvl2, lvl3, name, "Strict-Transport-Security not present")
        print("\033[1;31m [-]\033[0m Strict-Transport-Security not present \033[1;31m(Not OK)\033[0m")
    if "Public-Key-Pins:".lower() in headerlist.lower():
        #PKPHeader = filter(lambda y: 'Public-Key-Pins' in y,headx)
        save_data(database, module, lvl1, lvl2, lvl3, name, "Detected Public-Key-Pins")
        print("\033[1;32m [+]\033[0m Detected Public-Key-Pins \033[1;32m(OK)\033[0m")
        #print("\033[1;32m [+]\033[0m Detected Public-Key-Pins - " + PKPHeader[0].rstrip() + "' \033[1;32m(OK)\033[0m")
    else:
        save_data(database, module, lvl1, lvl2, lvl3, name, "Public-Key-Pins not present")
        print("\033[1;31m [-]\033[0m Public-Key-Pins not present \033[1;31m(Not OK)\033[0m")

def anomaly0x00(headx):
    knownhead = ['HTTP/1.1','Date','Server', 'Last-Modified','ETag','Accept-Ranges','Content-Length','Vary','Cache-Control','Content-Type','Pragma','Transfer-Encoding','Connection','Set-Cookie', 'Expires', 'WWW-Authenticate', 'Content-Encoding','Age','Status', 'Content-Range','Content-Language','Public-Key-Pins','Strict-Transport-Security','ETag', 'X-Powered-By', 'X-Content-Type-Options', 'X-XSS-Protection', 'Content-Security-Policy','X-Frame-Options', 'Referrer-Policy' ]
    for header in headx:
        if not any(y.lower() in header.lower() for y in knownhead):
            save_data(database, module, lvl1, lvl2, lvl3, name, "(info) Anomalous Header detected - " + header.rstrip())
            print("\033[1;34m [I]\033[0m Anomalous Header detected '" + header.rstrip() + "' \033[1;34m(Possible Informational)\033[0m")

def RetrieveHeader(Target):
    ReplyHeaders = ""

    if "https" in Target[:5]:
        sslcontext = ssl.create_default_context()
        n = input(O+' [!] Ignore SSL certificate errors? (Y/n) :> ')
        if n == 'y' or n == 'Y':
            print(GR+" [!] Ignoring certificate errors...")
            sslcontext = ssl._create_unverified_context()
        try:
            ReplyHeaders = urllib.request.urlopen(Target,context=sslcontext).headers.headers
        except ssl.CertificateError:
            print(R+" [-] SSL Certificate authentication error...")
        return ReplyHeaders
    else:
        ReplyHeaders = urllib.request.urlopen(Target).headers.headers
        return ReplyHeaders


def headers(web):
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
    try:
        #print(R+'\n    =========================================')
        #print(R+'\n     H T T P   H E A D E R   A N A L Y S I S')
        #print(R+'    ---<>----<>----<>----<>----<>----<>----<>\n')

        from core.methods.print import pvln
        pvln("http header analysis") 
                   
        time.sleep(0.5)
        print(GR+" [!] Initializing Header Analysis...")
        Headers = RetrieveHeader(web)
        xframe0x00(Headers)
        contentsec0x00(Headers)
        xssprotect0x00(Headers)
        xcontenttype0x00(Headers)
        general0x00(Headers)
        referrerpol0x00(Headers)
        anomaly0x00(Headers)
        if "https" in web[:5]:
            seccheck0x00(Headers)
        print(G+' [+] Done!')
    except Exception as e:
        print(R+' [-] Something happened...')
        print(R+' [-] Error : '+str(e))

def attack(web):
    web = web.fullurl
    headers(web)
