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
from core.methods.tor import session
import sys
sys.path.append('lib/fileutils_mod/')
from core.lib.FileUtils import FileUtils
from core.Core.colors import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)
file_paths = []
dir_path = []

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module determines the path to index files using a dictionary."
searchinfo = "Index Path Bruteforce"
properties = {}

def check0x00(web, dirpath, headers):
    requests = session()
    try:
        for dirs in dirpath:
            web0x00 = web + dirs
            req = requests.get(web0x00, headers=headers, allow_redirects=False, timeout=7, verify=False)
            try:
                if (req.headers['content-length'] is not None):
                    size = int(req.headers['content-length'])
                else:
                    size = 0

            except (KeyError, ValueError, TypeError):
                size = len(req.content)
            finally:
                size = FileUtils.sizeHuman(size)

            resp = str(req.status_code)
            if (resp == '200' or resp == '302' or resp == '304'):
                print(C+' [*] Found : ' + C + web0x00 +GR+' - '+ size + C + ' ('+resp+')')
                file_paths.append(web0x00)

            else:
                print(C+' [*] Checking : ' + B + web0x00 + R + ' ('+resp+')')
        return file_paths

    except Exception as e:
        print(R+' [-] Unknown Exception Encountered!')
        print(R+' [-] Exception : '+str(e))
        return file_paths

def getFile0x00(filepath):

    if os.path.exists(filepath) == True:
        time.sleep(0.5)
        print(GR+' [*] Importing wordlist...')
        with open(filepath, 'r') as f0:
            for f in f0:
                f = f.replace('\n','')
                if f.startswith('/'):
                    dir_path.append(f)
                else:
                    f = '/' + f
                    dir_path.append(f)

    else:
        print(R+' [-] No file path found under ' +filepath+'!')
    return dir_path

def indexmulbrute(web):
    name = targetname(web)
    lvl2 = "filebrute"
    module = "ReconANDOSINT"
    lvl1 = "Active Reconnaissance"
    lvl3 = "indexmulbrute"
    time.sleep(0.5)
    #print(R+'\n    =================================')
    print(R+'\n     M U L T I P L E   I N D I C E S')
    print(R+'    ---<>----<>----<>----<>----<>----\n')
                 
    print(C+' [*] Path to file to be used '+O+'(Default: files/fuzz-db/multipleindex_paths.lst)...'+C)
    fil = input(C+' [§] Your input (Press Enter if default) :> ')
    if fil == '':
        fil = 'files/fuzz-db/multipleindex_paths.lst'
    else:
        print(GR+' [*] Checking filepath...')
        if os.path.exists(fil) == True:
            print(C+' [+] File found!')
        else:
            print(R+' [-] File not found!')

    mo = getFile0x00(fil)
    gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                      'Accept-Language':'en-US;',
                      'Accept-Encoding': 'gzip, deflate',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;',
                      'Connection':'close'}

    try:
        ul = check0x00(web, mo, gen_headers)

    except Exception as e:
        print(R+' [-] Unexpected Exception Encountered!')
        print(R+' [-] Exception : '+str(e))

    if ul:
        print(G+' [+] The following possible index paths were found!'+C+color.TR2+C)
        for u in ul:
            print(O+' [+] Index file :'+C+color.TR3+C+G+u+C+color.TR2+C)
            save_data(database, module, lvl1, lvl2, lvl3, name, u)
    else:
        print(R+' [-] No multiple index locations were found!')
        save_data(database, module, lvl1, lvl2, lvl3, name, "No multiple index locations found.")
    print(C+' [+] Done!')

def attack(web):
    web = web.fullurl
    indexmulbrute(web)
