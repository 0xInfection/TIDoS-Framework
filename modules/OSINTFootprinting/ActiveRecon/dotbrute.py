#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


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

info = "This module finds common hidden files on the target's server using a dictionary."
searchinfo = "Hidden File Enumeration"
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
                f = f.strip('\n')
                if f.startswith('/'):
                    dir_path.append(f)
                else:
                    f = '/' + f
                    dir_path.append(f)

    else:
        print(R+' [-] No file path found under ' +filepath+'!')
    return dir_path

def dotbrute(web):

    print(GR+' [*] Loading module...')
    time.sleep(0.5)
    #print(R+'\n    =======================================')
    print(R+'\n     D O T   F I L E   B R U T E F O R C E')
    print(R+'    ––·‹›·––·‹›·––·‹›·––·‹›·––·‹›·––·‹›·––·\n')
                 
    print(C+' [*] Path to file to be used '+O+'(Default: files/fuzz-db/dot_paths.lst)...'+C)
    fil = input(C+' [§] Your input (Press Enter if default) :> ')
    if fil == '':
        fil = 'files/fuzz-db/dot_paths.lst'
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
        print(R+' [-] Exception Encountered!')
        print(R+' [-] Exception : '+str(e))

    if ul:
        print(G+' [+] The following interesting files were found!'+C+color.TR2+C)
        for u in ul:
            print(O+' [+] Path :'+C+color.TR3+C+G+u+C+color.TR2+C)
    else:
        print(R+' [-] No common interesting files were found!')
    print(C+' [+] Done!')

def attack(web):
    web = web.fullurl
    dotbrute(web)