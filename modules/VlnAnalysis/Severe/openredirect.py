#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import time
import requests as wrn
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect
from core.methods.tor import session
from multiprocessing import Pool, TimeoutError
from core.methods.multiproc import listsplit
from core.variables import processes
from core.Core.colors import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)
payloads = []

info = "Open Redirect Checker"
searchinfo = "Open Redirect Checker"
properties = {"PARAM":["Directory and Parameter to attack (eg /vuln/page.php?q=lmao)", " "], "PARALLEL":["Parallelise Attack? [1/0]", " "], "COOKIE":["Sets cookie if needed", " "], "DICT":["Path to dictionary to be used in normal attacks (default: files/fuzz-db/openredirect_payloads.lst)", " "]}

def check0x00(web, headers, pays):
    success = []
    requests = session()
    web000 = web.split('=')[0] + '='
    for pay in pays:
        web0x0 = web000 + pay
        print(B+'\n [!] Using payload : '+C+pay+' ...')
        print(GR+' [+] Url : '+C+web0x0+' ...')
        print(O+' [*] Making the no-verify request...')
        time.sleep(0.1)
        req = requests.get(web0x0, headers=headers, allow_redirects=True, timeout=7, verify=False)
        stat = str(req.status_code)
        if stat == '302':
            print(O+' [+] HTTP 302 Response '+GR+'(Found)!\n '+G+' [+] Confirm open-redirection vulnerability at : '+C+web0x0)
            success.append(pay+" : "+stat)
        elif stat == '301':
            print(O+' [+] HTTP 301 Response! '+GR+'(Moved Permanently)!\n '+G+' [+] Potential open-redirection vulnerability at : '+C+web0x0)
            success.append(pay+" : "+stat)
        elif stat == '307':
            print(O+' [+] HTTP 307 Response! '+GR+'(Temporary Redirect)!\n '+G+' [+] Potential open-redirection vulnerability at : '+C+web0x0)
            success.append(pay+" : "+stat)
        elif stat == '400':
            print(R+' [-] HTTP 400 Response '+GR+'(Bad Request)!')
        elif stat == '403':
            print(R+' [-] HTTP 403 Response '+GR+'(Forbidden)!')
        elif stat == '404':
            print(R+' [-] HTTP 404 Response '+GR+'(Not Found)!')
        elif stat == '405':
            print(R+' [-] HTTP 405 Response '+GR+'(Method Not Allowed)!')
        elif stat == '406':
            print(R+' [-] HTTP 406 Response '+GR+'(Not Acceptable)!')
        elif stat == '408':
            print(R+' [-] HTTP 408 Response '+GR+'(Timeout)!')
        elif stat == '500':
            print(O+' [-] HTTP 500 Response '+GR+'(Internal Error)! Server could not handle request!')
            print(G+' [+] Potential Vulnerability at : '+C+web0x0)
            success.append(pay+" : "+stat)
        elif stat == '502':
            print(O+' [-] HTTP 502 Response '+GR+'(Internal Error)! Server could not handle request!')
            print(G+' [+] Potential Vulnerability at : '+C+web0x0)
            success.append(pay+" : "+stat)
        elif stat == '503':
            print(O+' [-] HTTP 503 Response '+GR+'(Internal Error)! Server could not handle request!')
            print(G+' [+] Potential Vulnerability at : '+C+web0x0)
            success.append(pay+" : "+stat)
        elif stat == '200':
            print(R+' [-] HTTP 200 Response '+GR+'(OK)!')
            print(G+' [+] Redirection confirmation page at : '+O+web0x0)
        elif stat == '202':
            print(R+' [-] HTTP 202 Response '+GR+'(Accepted)!')
            print(G+' [+] Redirection confirmation page at : '+O+web0x0)
        elif stat == '204':
            print(R+' [-] HTTP 204 Response '+GR+'(No Content)!')
            print(G+' [+] Redirection confirmation page at : '+O+web0x0)
        elif stat == '203':
            print(R+' [-] HTTP 203 Response '+GR+'(Non-Authoritative Content)!')
            print(G+' [+] Redirection confirmation page at : '+O+web0x0)
        elif stat == '429':
            print(R+' [-] The site has an active rate limiting enabled!')
            time.sleep(0.7)
            print(R+' [-] Server blocking requests... Exiting module...')
            break
        else:
            print(R+' [-] Interesting HTTP Response : '+O+stat)
    return success

def getPayloads0x00(fi):
    try:
        print(GR+' [*] Importing payloads from '+O+fi+'...')
        time.sleep(1)
        with open(fi,'r') as f0:
            for f in f0:
                f = f.strip('\n')
                payloads.append(f)
        print(G+' [+] '+O+str(len(payloads))+G+' Payloads Loaded!')

    except ImportError:
        print(R+' [-] Unable to import payloads!')
        print(R+' [-] File does not exist!')

def openredirect(web):
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
    time.sleep(0.6)
    #print(R+'\n    ===========================================')
    #print(R+'\n     O P E N   R E D I R E C T   C H E C K E R')
    #print(R+'    ---<>----<>----<>----<>----<>----<>----<>--\n')

    from core.methods.print import pvln
    pvln("open redirect checker") 
                 

    try:
        if properties["PARAM"][1] == " ":
            param = input(O+' [§] Scope parameter to test (eg. /redirect.php?site=foo) :> ')
        else:
            param = properties["PARAM"][1]
        if '?' in param and '=' in param:
            if param.startswith('/'):
                m = input(GR+'\n [!] Your path starts with "/".\n [§] Do you mean root directory? (Y/n) :> ')
                if m == 'y':
                    web00 = web + param
                elif m == 'n':
                    web00 = web + param
                else:
                    print(R+' [-] U mad?')
            else:
                web00 = web + '/' + param
        else:
            print(R+' [-] Your input does not match a parameter...')
            param = input(O+' [§] Enter paramter to test :> ')

        if properties["PARALLEL"][1] == " ":
            pa = input(" [?] Parallel Attack? (enter if not) :> ")
            parallel = pa != ""
        else:
            parallel = properties["PARALLEL"][1] == "1"

        print(GR+' [*] Configuring relative headers...')
        time.sleep(0.8)
        gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                          'Accept-Language':'en-US;',
                          'Accept-Encoding': 'gzip, deflate',
                          'Accept': 'text/html,application/xhtml+xml,application/xml;',
                          'Connection':'close'}

        if properties["DICT"][1] == " ":
            print(O+' [!] Enter path to payload file '+R+'(Default: files/payload-db/openredirect_payloads.lst)')
            fi = input(O+' [§] Your input (Press Enter if default) :> ')
        elif properties["DICT"][1].lower() == "none":
            fi = ""
        else:
            fi = properties["DICT"][1]
        if fi == '':
            fi = 'files/payload-db/openredirect_payloads.lst'
            getPayloads0x00(fi)
        else:
            if os.path.exists(fi) == True:
                print(G+' [+] File found under '+fi)
                getPayloads0x00(fi)
            else:
                print(R+' [-] File not found... Using default payload...')
                fi = 'files/payload-db/openredirect_payloads.lst'
                getPayloads0x00(fi)
        if properties["COOKIE"][1] == " ":
            input_cookie = input("\n [§] Got any cookies? [just enter if none] :> ")
        elif properties["COOKIE"][1].lower() == "none":
            input_cookie = ""
        else:
            input_cookie = properties["COOKIE"][1]
        if(len(input_cookie) > 0):
            gen_headers['Cookie'] = input_cookie
        print(GR+' [*] Configuring payloads with Url...')
        success = []
        if not parallel:
            success += check0x00(web00, gen_headers, payloads)
        else:
            paylists = listsplit(payloads, round(len(payloads)/processes))
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(check0x00, args=(web00,gen_headers,l,)) for l in paylists]
                for y in res:
                    i = y.get()
                    success += i
        if success:
            data = "Open Redirect Vulnerability found!\nVulnerable param: " + web00 + "\nPayloads: " + str(success)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            print(" [+] Open Redirect Vulnerability found! Successful payloads:")
            for i in success:
                print(i)
        else:
            print(R + "\n [-] No payload succeeded."+C)
            save_data(database, module, lvl1, lvl2, lvl3, name, "No payload succeeded.")
    except KeyboardInterrupt:
        print(R+' [-] User Interruption Detected!')
        pass

def attack(web):
    web = web.fullurl
    openredirect(web)
