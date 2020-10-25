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
import requests as wrn
import time
sys.path.append('files/signaturedb/')
from core.variables import processes
from core.methods.multiproc import listsplit
from multiprocessing import Pool, TimeoutError
from core.Core.colors import *
from files.signaturedb.xpatherror_signatures import xpath_errors
from random import choice
from core.methods.tor import session
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)
payloads = []

info = "This module searches for XPATH Injection flaws using the built-in dictionary or an user-provided payload list."
searchinfo = "XPATH Injection Scanner"
properties = {"PARAM":["Directory and Parameter to attack (eg /vuln/page.php?q=lmao)", " "], "PARALLEL":["Parallelise Attack? [1/0]", " "], "DICT":["Path to dictionary to be used in normal attacks (default: files/fuzz-db/xpath_payloads.lst)", " "]}

def check0x00(web0x00, pay, gen_headers):
    success = []
    requests = session()
    try:
        print(GR+' [*] Making the request...')
        rq = requests.get(web0x00, headers=gen_headers, allow_redirects=False, verify=False)
        c = rq.content
        print(O+' [!] Analysing responses...')
        time.sleep(0.7)
        found = False
        for sign in xpath_errors:
            if re.search(sign, str(c), re.I):
                print(G+' [+] Potential XPATH Code Injection Flaw discovered!')
                print(GR+' [*] Injecting payloads...')
                time.sleep(0.4)
                print(B+' [+] Vulnerable Link : '+C+web0x00)
                print(B+' [+] Payload : '+C+pay)
                print(O+' [+] Response : \033[0m\n')
                print(c)
                found = True
                success.append(web0x00)
        if not found:
            print(R+' [-] Payload '+O+pay+R+' unsuccessful...')
            print(R+' [-] No successful code injection at : '+O+web0x00)

    except Exception as e:
        print(R+' [-] Exception encountered!')
        print(R+' [-] Error : '+str(e))
    return success

def getFile0x00():

    try:
        if properties["DICT"][1] == " ":
            print(O+' [§] Enter path to file (default: files/payload-db/xpath_payloads.lst)...')
            w = input(O+' [§] Your input (Press Enter if default) :> '+C)
        elif properties["DICT"][1].lower() == "none":
            w = ""
        else:
            w = properties["DICT"][1]
        if w == '':
            fi = 'files/payload-db/xpath_payloads.lst'
            print(GR+' [*] Importing payloads...')
            with open(fi,'r') as q0:
                for q in q0:
                    q = q.strip('\n')
                    payloads.append(q)
        else:
            fi = w
            if os.path.exists(fi) == True:
                print(G+' [+] File '+fi+' found...')
                print(GR+' [*] Importing payloads...')
                with open(fi,'r') as q0:
                    for q in q0:
                        q = q.strip('\n')
                        payloads.append(q)
    except IOError:
        print(R+' [-] File path '+O+fi+R+' not found!')

def checkpre(payloads, web00, bug2, gen_headers):
    success = []
    for pay in payloads:
        print(GR+'\n [*] Setting parameters...')
        web0x00 = web00 + pay + bug2
        print(C+' [+] Using payload : '+B+str(pay))
        print(B+' [+] Using !nfected Url : '+GR+str(web0x00)) # display whats going on
        success += check0x00(web0x00, pay, gen_headers) # check the outupt of the fuzz
    return success

def xpathi(web):
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
    time.sleep(0.5)
    #print(R+'\n    ===============================')
    #print(R+'\n     X P A T H   I N J E C T I O N')
    #print(R+'    ---<>----<>----<>----<>----<>--\n')

    from core.methods.print import pvln
    pvln("xpath Injection") 
                 

    gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                      'Accept-Language':'en-US;',
                      'Accept-Encoding': 'gzip, deflate',
                      'Accept': 'text/php,application/xhtml+xml,application/xml;',
                      'Connection':'close'}

    print(GR+' [*] Initiating '+R+'Parameter Based Check...')
    if properties["PARAM"][1] == " ":
        param = input(O+' [§] Parameter Path (eg. /vuln/page.php?q=input) :> ')
    else:
        param = properties["PARAM"][1]
    if param.startswith('/') == False:
        param = '/' + param

    choice = ""
    if "&" in param:
        ln = len(param.split("&"))
        choice = input(" [!] Discovered {} parameters. Which one to use? (enter name) :> ".format(ln))
        if not choice in param:
            sys.exit(" [-] Param {} not found.".format(choice))

    bug2 = ""
    if choice != "":
        n = param.split(choice + "=")[1]
        if "&" in n:
            bug2 = param.split(choice)[1]
            tmp = bug2.split("&")[0]
            bug2 = bug2.replace(tmp,"")

    if properties["PARALLEL"][1] == " ":
        pa = input("\n [?] Parallelise Attack? (enter if not) :> ")
        parallel = pa != ""
    else:
        parallel = properties["PARALLEL"][1] == "1"

    print(GR+' [*] Importing filepath...')
    getFile0x00()
    web00 = web + param.split(choice + '=')[0] + choice + '='
    try:
        success = []
        if not parallel:
            for pay in payloads:
                print(GR+'\n [*] Setting parameters...')
                web0x00 = web00 + pay + bug2
                print(C+' [+] Using payload : '+B+str(pay))
                print(B+' [+] Using !nfected Url : '+GR+str(web0x00)) # display whats going on
                success += check0x00(web0x00, pay, gen_headers) # check the outupt of the fuzz
        else:
            paylists = listsplit(payloads, round(len(payloads)/processes))
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(checkpre, args=(l, web00, bug2, gen_headers,)) for l in paylists]
                for y in res:
                    i = y.get()
                    success += i
        if success:
            data = "XPATHi Vulnerability found! POCs :> " + str(success)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            print(" [+] XPATHi Vulnerability found! Successful payloads:")
            for i in success:
                print(i)
        else:
            print(R + "\n [-] No payload succeeded."+C)
            data = "No payload succeeded."
            save_data(database, module, lvl1, lvl2, lvl3, name, data)

    except Exception as e:
        print(R+' [-] Unexpected Exception Encountered!')
        print(R+' [-] Exception : '+str(e))

    print(G+'\n [+] XPATHi Module Completed!\n')

def attack(web):
    web = web.fullurl
    xpathi(web)
