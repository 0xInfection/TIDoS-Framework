#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import sys
import time
import requests as wrn
sys.path.append('files/signaturedb/')
from core.methods.tor import session
from multiprocessing import Pool, TimeoutError
from core.methods.multiproc import listsplit
from core.variables import processes
from core.Core.colors import *
from files.signaturedb.ldaperror_signatures import ldap_errors
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)

info = "This module tests LDAP Injections using either the default payload database, or an user-provided dictionary."
searchinfo = "LDAP Injection Scan"
properties = {"PARAM":["Directory and Parameter to attack (eg /vuln/page.php?q=lmao)", " "], "PARALLEL":["Parallelise Attack? [1/0]", " "], "COOKIE":["Sets cookie if needed", " "], "DICT":["Path to dictionary to be used in normal attacks (default: files/fuzz-db/ldap_payloads.lst)", " "]}

def getFile0x00(fi):

    global payloads
    payloads = []
    print(GR+' [*] Importing payloads...')
    time.sleep(0.7)
    with open(fi,'r') as payl:
        for pay in payl:
            c = pay.replace('\n','')
            payloads.append(c)
    print(G+' [+] Loaded '+O+str(len(payloads))+G+' payloads...')

def check0x00(web000, headers, pays):
    success = []
    requests = session()
    for payload in pays:
        gotcha = False
        print(B+'\n [+] Using Payload : '+C+payload)
        web0x00 = web000 + payload
        print(O+' [+] Url : '+C+web0x00)
        print(GR+' [*] Making the request...')
        try:
            req = requests.get(web0x00, headers=headers, allow_redirects=False, timeout=7, verify=False).text
            print(O+' [!] Searching through error database...')
            for err in ldap_errors:
                if err.lower() in req.lower():
                    print(G+' [+] Possible LDAP Injection Found : '+O+web0x00)
                    gotcha=True
                    print(O+' [+] Response : ')
                    print(P+req)
                    success.append(payload)
                else:
                    pass

            if gotcha == False:
                print(R+' [-] No error reflection found in response!')
                time.sleep(0.4)
                print(R+' [-] Payload '+O+payload+R+' not working!')
                pass

        except Exception as e:
            print(R+' [-] Query Exception : '+str(e))
    return success

def ldap(web):
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
    #print(R+'\n     =============================')
    #print(R+'\n      L D A P   I N J E C T I O N')
    #print(R+'     ---<>----<>----<>----<>----<>\n')

    from core.methods.print import pvln
    pvln("ldap Injection") 
                  
    try:
        if properties["PARAM"][1] == " ":
            web0 = input(O+' [§] Parameter path to test (eg. /lmao.php?foo=bar) :> ')
        else:
            web0 = properties["PARAM"][1]
        if "?" in web0 and '=' in web0:
            if web0.startswith('/'):
                m = input(GR+'\n [!] Your path starts with "/".\n [§] Do you mean root directory? (Y/n) :> ')
                if m.lower() == 'y':
                    web00 = web + web0
                elif m.lower() == 'n':
                    web00 = web + web0
                else:
                    print(R+' [-] U mad?')
            else:
                web00 = web + '/' + web0
        else:
            sys.exit(R+" [-] Invalid parameters."+C)
        print(B+' [+] Parameterised Url : '+C+web00)

        if properties["PARALLEL"][1] == " ":
            pa = input(" [?] Parallel Attack? (enter if not) :> ")
            parallel = pa != ""
        else:
            parallel = properties["PARALLEL"][1] == "1"

        if properties["COOKIE"][1] == " ":
            input_cookie = input("\n [*] Enter cookies if needed (Enter if none) :> ")
        elif properties["COOKIE"][1].lower() == "none":
            input_cookie = ""
        else:
            input_cookie = properties["COOKIE"][1]
        print(GR+' [*] Setting headers...')
        time.sleep(0.6)
        gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                          'Accept-Language':'en-US;',
                          'Accept-Encoding': 'gzip, deflate',
                          'Accept': 'text/html,application/xhtml+xml,application/xml;',
                          'Connection':'close'}

        if(len(input_cookie) > 0):
            gen_headers['Cookie'] = input_cookie
        if properties["DICT"][1] == " ":
            print(O+' [§] Enter the payloads file '+R+'(Default: files/payload-db/ldap_payloads.lst)...')
            fi = input(O+' [§] Your input (Press Enter for default) :> ')
        elif properties["DICT"][1].lower() == "none":
            fi = ""
        else:
            fi = properties["DICT"][1]
        if fi == '':
            fi = 'files/payload-db/ldap_payloads.lst'
            getFile0x00(fi)
        else:
            if os.path.exists(fi) == True:
                print(G+' [+] File under '+fi+' found!')
                getFile0x00(fi)
            else:
                print(R+' [-] Invalid input... Using default...')
                fi = 'files/payload-db/ldap_payloads.lst'
                getFile0x00(fi)
        print(O+' [!] Parsing url...')
        time.sleep(0.7)
        web000 = web00.split('=')[0] + '='
        print(GR+' [*] Starting enumeration...')
        time.sleep(0.7)
        success = []
        if not parallel:
            success += check0x00(web000, gen_headers, payloads)
        else:
            paylists = listsplit(payloads, round(len(payloads)/processes))
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(check0x00, args=(web000,gen_headers,l,)) for l in paylists]
                for y in res:
                    i = y.get()
                    success += i
        if success:
            data = "LDAPi Vulnerability found!\nVulnerable param: " + web00 + "\nPayloads: " + str(success)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            print(" [+] LDAPi Vulnerability found! Successful payloads:")
            for i in success:
                print(i)
        else:
            save_data(database, module, lvl1, lvl2, lvl3, name, "No payload succeeded.")
            print(R + "\n [-] No payload succeeded."+C)

    except KeyboardInterrupt:
        print(R+' [-] Aborting module...')
        pass
    except Exception as e:
        print(R+' [-] Exception : '+str(e))
    print(G+'\n [+] LDAP Injection module completed!\n')

def attack(web):
    web = web.fullurl
    ldap(web)
