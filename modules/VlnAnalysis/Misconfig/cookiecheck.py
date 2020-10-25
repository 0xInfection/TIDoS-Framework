#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import urllib.request as urllib
import time
import ssl
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module analyzes the security of cookies (HTTPOnly/Secure Flags)"
searchinfo = "Cookie Analysis"
properties = {}

def cookiecheck0x00(searchheaders):

    c = 0
    for header in searchheaders:
        if (("Set-Cookie:".lower() in str(header.lower())) or ('Cookie:'.lower() in str(header.lower()))):
            c = c + 1
    print(G+' [+] %s cookie(s) obtained!' % c)

    for header in searchheaders:
        if (("Set-Cookie:".lower() in str(header.lower())) or ('Cookie:'.lower() in str(header.lower()))):
            try:
                print(G+' [+] Cookie obtained!')
                time.sleep(0.5)
                print(O+' [*] Examining cookie...')
                time.sleep(0.4)
                CookieSplit = header.split(';')
                del CookieSplit[0]
                CookieSplit[-1] = CookieSplit[-1].rstrip()
                CookieString = ''.join(CookieSplit)
                if "HttpOnly".lower() not in CookieString.lower():
                    save_data(database, module, lvl1, lvl2, lvl3, name, "Cookie not marked HttpOnly - "+header.rstrip())
                    print(R+" [-] Cookie not marked HttpOnly - "+C+"'" + header.rstrip() + "' ")
                else:
                    save_data(database, module, lvl1, lvl2, lvl3, name, "Cookie marked HttpOnly - "+header.rstrip())
                    print(G+' [+] Cookie marked HTTPOnly - '+C+'"'+header.rstrip()+'"')
                if "Secure".lower() not in CookieString.lower():
                    save_data(database, module, lvl1, lvl2, lvl3, name, "Cookie not marked Secure - "+header.rstrip())
                    print(R+" [-] Cookie not marked Secure - "+C+"'" + header.rstrip() + "' ")
                else:
                    save_data(database, module, lvl1, lvl2, lvl3, name, "Cookie marked Secure - "+header.rstrip())
                    print(G+' [+] Cookie marked Secure - '+C+'"'+header.rstrip()+'"')

            except Exception as e:
                print(R+' [-] Some thing happened!')
                print(R+' [!] Error : '+str(e))


def RetrieveHeader(Target):

    ReplyHeaders = ""
    print(O+' [*] Making request to retrieve HHTP headers...')
    if "https" in Target[:5]:
        sslcontext = ssl.create_default_context()
        n = input(O+' [§] Ignore SSL certificate errors? (Y/n) :> ')
        if n == 'y' or n == 'Y':
            print(GR+" [*] Ignoring certificate errors...")
            sslcontext = ssl._create_unverified_context()
        try:
            ReplyHeaders = urllib.urlopen(Target,context=sslcontext).headers.headers
        except ssl.CertificateError:
            print(R+" [-] SSL Certificate authentication error...")
        return ReplyHeaders
    else:
        ReplyHeaders = urllib.urlopen(Target).headers.headers
        return ReplyHeaders

def cookiecheck(web):
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
    #print(R+'\n    ==================================================')
    #print(R+'\n     C O O K I E   C H E C K  (HTTPOnly/Secure Flags)')
    #print(R+'    ---<>----<>----<>----<>----<>----<>----<>----<>---\n')

    from core.methods.print import pvln
    pvln("Cookie check")            

    print(GR+" [!] Initializing Header Analysis...")
    Headers = RetrieveHeader(web)
    cookiecheck0x00(Headers)

def attack(web):
    web = web.fullurl
    cookiecheck(web)
