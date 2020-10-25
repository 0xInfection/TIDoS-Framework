#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import re
import sys
import time
#import requests
from core.Core.colors import *
import sre_constants
from time import sleep
from multiprocessing import Pool, TimeoutError
from core.methods.multiproc import listsplit
from core.variables import processes
from core.methods.tor import session

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

global pay, poly
poly = []
pay = []

info = "This module looks for Cross Site Scripting (XSS) vulnerabilites, either manually or automatically."
searchinfo = "Cross Site Sripting"
properties = {"PARAM":["Directory and Parameter to attack (eg /vuln/page.php?q=lmao)", " "], "PARALLEL":["Parallelise Attack? [1/0]", " "]}

def cookieatck(pays, session, web):
    success = []
    for j in pays:
        i = '%s' % j
        print(B+" [*] Trying Payload : "+C+ i)
        time.sleep(0.7)
        for cookie in session.cookies:
            cookie.value += i
            print(O+' [+] Using '+R+'!nfected'+O+' cookie : '+GR+cookie.value)
            r = session.get(web)
            if str(i) in str(r.text):
                poc = C+" [+] PoC : " +O+ cookie.name + " : " +GR+ cookie.value
                print(G+" [+] Cookie Based XSS Detected! ")
                print(poc)
                print(P+' [+] Code : '+W+str(r.text)+'\n')
                success.append(i)
    return success

def useratck(pays, web):
    success = []
    requests = session()
    for j in pays:
        i = '%s' % j
        print(B+' [*] Using payload : '+C+i)
        time.sleep(0.7)
        user_agent = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux ' +
                        'x86_64; rv:39.0)'}
        user_agent['User-agent'] += i
        req = requests.get(web, headers=user_agent)
        print(O+' [*] Using '+R+'!nfected'+O+' UA : '+GR+user_agent['User-agent'])
        #flag = ' '.join(req.text).encode('utf-8').strip()
        flag = req.text.encode('utf-8').strip()
        if str(i) in str(flag):
            print(G+'\n [!] Cross Site Scripting (User-Agent Based) Detected!')
            print(R+' [!] User-Agent : '+O+user_agent['User-agent'])
            print(W+color.BOLD+' [+] Code: '+W)
            print(str(req.content)+'\n')
            success.append(i)
    return success

def refatck(pays, web):
    success = []
    requests = session()
    for j in pays:
        i = '%s' % j
        print(B+' [*] Using payload : '+C+i)
        time.sleep(0.7)
        user_agent = {'Referer': 'http://' + 'xssing.pwn'}
        user_agent['Referer'] += i
        req = requests.get(web, headers=user_agent)
        print(O+' [*] Using '+R+'!nfected'+O+' UA : '+GR+user_agent['Referer'])
        #flag = ' '.join(k for k in req.text).encode('utf-8').strip()
        flag = req.text.encode("utf-8").strip()     
        if str(i) in str(flag):
            #print("1")
            print(G+'\n [!] Cross Site Scripting (Referrer Based) Detected!')
            #print("2")
            print(R+' [!] User-Agent : '+O+user_agent['Referer'])
            print(W+color.BOLD+' [+] Code: '+W)
            #print("3")
            print(str(req.content)+'\n')
            success.append(i)
    return success

def auto0x00(web, parallel):

    def xsscookie0x00(web, parallel):

        #print(R+'\n    =======================')
        print(R+'\n     X S S  (Cookie Based)')
        print(R+'    ---<>----<>----<>----<>\n')
                     

        sleep(0.5)
        vsession = session()
        vsession.get(web)
        if vsession.cookies:
            print(G+' [+] This website supports session cookies...')
            success = []
            if not parallel:
                success += cookieatck(pay, vsession, web)
            else:
                paylists = listsplit(pay, round(len(pay)/processes))
                with Pool(processes=processes) as pool:
                    res = [pool.apply_async(cookieatck, args=(l,vsession,web,)) for l in paylists]
                    for y in res:
                        i = y.get()
                        success += i
            if success:
                data = "XSS Vulnerability (Cookie) found! Payloads :> " + str(success)
                save_data(database, module, lvl1, lvl2, lvl3, name, data)
                print(" [+] XSS (Cookie) Vulnerability found! Successful payloads:")
                for i in success:
                    print(i)
            else:
                data = "(cookie) no payload succeeded."
                save_data(database, module, lvl1, lvl2, lvl3, name, data)
                print(R + "\n [-] No payload succeeded."+C)
        else:
            print(R+' [-] No support for cookies...')
            time.sleep(0.5)
            print(R+' [-] Cookie based injection not possible...')
            data = "No support for cookies. Cookie based injection not possible."
            save_data(database, module, lvl1, lvl2, lvl3, name, data)

    def xssuser0x00(web, parallel):

        #print(R+'\n    ===========================')
        print(R+'\n     X S S  (User-Agent Based)')
        print(R+'    ---<>----<>----<>----<>----\n')
                     
        success = []
        if not parallel:
            success += useratck(pay, web)
        else:
            paylists = listsplit(pay, round(len(pay)/processes))
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(useratck, args=(l,web,)) for l in paylists]
                for y in res:
                    i = y.get()
                    success += i
        if success:
            data = "XSS Vulnerability (useragent) found! Payloads :> " + str(success)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            print(" [+] XSS Vulnerability (UserAgent) found! Successful payloads:")
            for i in success:
                print(i)
        else:
            data = "(useragent) no payloads succeeded."
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            print(R + "\n [-] No payload succeeded."+C)

    def xssref0x00(web, parallel):

        #print(R+'\n    ===========================')
        print(R+'\n     X S S  (Referrer Based)')
        print(R+'    ---<>----<>----<>----<>----\n')
                     
        success = []
        if not parallel:
            success += refatck(pay, web)
        else:
            paylists = listsplit(pay, round(len(pay)/processes))
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(refatck, args=(l,web,)) for l in paylists]
                for y in res:
                    i = y.get()
                    success += i
        if success:
            data = "XSS Vulnerability (Referrer) found! Payloads :> " + str(success)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            print(" [+] XSS Vulnerability (Referrer) found! Successful payloads:")
            for i in success:
                print(i)
        else:
            data = "(referrer) no payload succeeded."
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            print(R + "\n [-] No payload succeeded."+C)

    print(P+' [!] Enter an option :\n')
    print(B+'   [1] '+C+'Cookie Value Based XSS')
    print(B+'   [2] '+C+'User-Agent Value Based XSS')
    print(B+'   [3] '+C+'Referrer Value Based XSS\n')
    q = input(O+' [§] TID :> ')
    if q == '3':
        print(GR+' [*] Launching Referrer Based Module...')
        xssref0x00(web, parallel)
    elif q == '2':
        print(GR+' [*] Launching User-Agent Based Module...')
        xssuser0x00(web, parallel)
    elif q == '1':
        print(GR+' [*] Launching Cookie-Based Module...')
        xsscookie0x00(web, parallel)

def polyatck(polys, li, bug2):
    success = []
    requests = session()
    for p in polys:
        bugged = li + str(p) + bug2
        print(B+"\n [*] Trying : "+C+bugged)
        time.sleep(0.7)
        print(GR+' [*] Making the request...')
        resp = requests.get(bugged)
        print(O+' [!] Matching payload signatures...')
        try:
            if str(p) in str(resp.text):
                print('\n'+G+' [+] Vulnerable link detected : ' + bugged)
                print(GR+' [*] Injecting payloads...')
                print(B+' [!] PoC : ' + str(bugged))
                print(R+" [!] Payload : " + O + p + '\033[0m')
                print("\033[1m [!] Code Snippet :\n \033[0m" + str(resp) + '\n')
                success.append(str(bugged))
            else:
                print(R+' [-] No successful payload reflection...')
                print(R+' [-] Payload '+O+p+R+' unsuccessful...')
        except sre_constants.error:
            pass
    return success

def xsspoly0x00(li, bug2, parallel):

    success = []
    #print(R+'\n    ==========================')
    print(R+'\n     X S S  (Polyglot Fuzzer)')
    print(R+'    ---<>----<>----<>----<>---\n')
                 
    try:
        if '?' in str(li) and '=' in str(li):
            if not parallel:
                success += polyatck(poly, li, bug2)
            else:
                paylists = listsplit(poly, round(len(poly)/processes))
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(polyatck, args=(l,li,bug2,)) for l in paylists]
                for y in res:
                    i = y.get()
                    success += i
        if success:
            data = "XSS Vulnerability (Polyglot) found! POCs :> " + str(success)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            print(" [+] XSS Vulnerability (Polyglot) found! Successful payloads:")
            for i in success:
                print(i)
        else:
            data = "(polyglot) no payload succeeded."
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            print(R + "\n [-] No payload succeeded."+C)

    except KeyboardInterrupt:
        print(R+' [+] Polyglot Payloads File does not exist!')

def manualatck(pays, bugs, bug2):
    success = []
    requests = session()
    for p in pays:
        bugged = bugs + str(p) + bug2
        print(B+"\n [*] Trying : "+C+bugged)
        time.sleep(0.2)
        print(GR+' [*] Making the request...')
        response = requests.get(bugged)
        print(O+' [!] Matching payload signatures...')
        try:
            if str(p) in str(response.text):
                print(G+' [+] Vulnerable link detected : ' + bugged)
                print(GR+' [*] Injecting payloads...')
                print(B+' [!] PoC : ' + str(bugged))
                print(R+" [!] Payload : " + O + p + '\033[0m')
                print("\033[1m [!] Code Snippet :\n \033[0m" + str(response) + '\n')
                success.append(str(bugged))
            else:
                print(R+' [-] No successful payload reflection...')
                print(R+' [-] Payload '+O+p+R+' unsuccessful...')

        except sre_constants.error:
            pass
    return success

def manual0x00(web, parallel):
    #print(R+'\n    ======================')
    print(R+'\n     X S S  (Manual Mode)')
    print(R+'    ---<>----<>----<>----<\n')
                 
    if properties["PARAM"][1] == " ":
        bug = input(O+' [§] Injectable Endpoint'+R+' (eg. /xss/search.php?q=drake)'+O+' :> ')
    else:
        bug = properties["PARAM"][1]
    choice = ""
    if "&" in bug:
        ln = len(bug.split("&"))
        choice = input(" [!] Discovered {} parameters. Which one to use? (enter name) :> ".format(ln))
        if not choice in bug:
            sys.exit(" [-] Param {} not found.".format(choice))
    bugs = web + bug.split(choice + '=')[0] + choice + '='
    bug2 = ""
    if choice != "":
        n = bug.split(choice + "=")[1]
        if "&" in n:
            bug2 = bug.split(choice)[1]
            tmp = bug2.split("&")[0]
            bug2 = bug2.replace(tmp,"")
    print(O+' [!] Using Url : '+GR+bugs+"INJECT"+bug2)
    if '?' in str(bugs) and '=' in str(bugs):
        success = []
        if not parallel:
            manualatck(pay, bugs, bug2)
        else:
            paylists = listsplit(pay, round(len(pay)/processes))
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(manualatck, args=(l,bugs,bug2,)) for l in paylists]
                for y in res:
                    i = y.get()
                    success += i
        if success:
            data = "XSS Vulnerability (manual) found! POCs :> " + str(success)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            print(" [+] XSS Vulnerability found! Successful payloads:")
            for i in success:
                print(i)
        else:
            data = "(manual) no payload succeeded."
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            print(R + "\n [-] No payload succeeded."+C)
            x = input(O+' [§] Test Polyglots? (Y/n) :> ')
            if x == 'Y' or x == 'y':
                print(GR+' [*] Proceeding fuzzing with polyglots...')
                xsspoly0x00(bugs, bug2, parallel)
            elif x == 'n' or x == 'N':
                print(C+' [+] Okay!')
            else:
                print(GR+' [-] U high dude?')

    else:
        print(R+' [-] Enter an URL with scope parameter...')
        manual0x00(web, parallel)

def xss(web):
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
    first = True
    while True:
        sleep(0.6)
        if web.endswith('/'):
            web = web[:-1]
        #print(R+'\n    =========================================')
        #print(R+'\n     C R O S S   S I T E   S C R I P T I N G')
        #print(R+'    ---<>----<>----<>----<>----<>----<>----<>\n')

        from core.methods.print import pvln
        pvln("Cross site scripting") 
        if first:            
            print(GR+' [*] Importing payloads...')
            sleep(0.8)
            try:
                with open('files/payload-db/xss_payloads.lst','r') as payloads:
                    pay.clear()
                    for payload in payloads:
                        payload = payload.replace('\n','')
                        pi = r'%s' % (payload)
                        #pi = payload.encode("utf-8").decode("utf-8")# % (payload)  # Converting to a raw string
                        #pil = str(pi).split("'")
                        #payl = ""
                        #for i in range(1,len(pil)-1):
                        #    payl += pil[i]
                        pay.append(pi)
                print(G+' [+] '+O+str(len(pay))+G+' payloads loaded!')
                first = False
                sleep(0.2)
                with open('files/payload-db/polyglot_payloads.lst','r') as polyy:
                    poly.clear()
                    for payload in polyy:
                        payload = payload.replace('\n','')
                        poy = r'%s' % (payload)
                        poly.append(poy)
                print(G+' [+] '+O+str(len(poly))+G+' polyglots loaded!')
                sleep(0.7)
            except IOError:
                print(R+' [-] Payloads file does not exist!')

        if properties["PARALLEL"][1] == " ":
            pa = input(" [?] Parallel Attack? (enter if not) :> ")
            parallel = pa != ""
        else:
            parallel = properties["PARALLEL"][1] == "1"
        print(O+'\n [§] Enter the type you want to proceed:\n')
        print(B+'   [1] '+C+'Manual Mode')
        print(B+'   [2] '+C+'Automatic Mode\n')
        p = input(O+' [§] TID :> ')
        if p == '1':
            print(GR+' [*] Initializing manual mode...')
            manual0x00(web, parallel)
        if p == '2':
            print(GR+' [*] Loading automatic mode...')
            auto0x00(web, parallel)

    print(G+' [+] XSS Module Completed!\n')

def attack(web):
    web = web.fullurl
    xss(web)
