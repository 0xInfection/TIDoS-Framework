#!/usr/bin/env python3
# -*- coding : utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


from core.methods.tor import session 
from core.Core.colors import *
from core.variables import tor
from core.methods.print import pscan

import time, subprocess, re
from core.methods.print import gprint

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Incredibly fast crawler designed for OSINT"
searchinfo = "Incredibly fast crawler designed for OSINT"
properties = {"ROOT":["Root URL the crawling starts with", " "], "ARGS":["The arguments passed to Photon (formatted as after $photon -u ROOT )", " "]}


def photon(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = inspect.stack()[0][3]
    global module
    module = "ScanANDEnum"
    global lvl1
    lvl1 = "Crawling"
    global lvl3
    lvl3 = ""
    time.sleep(0.5)
    pscan("photon")
    if properties["ROOT"][1] == " ":
        root = input(" [§] Enter the root URL :> ")
    else:
        root = properties["ROOT"][1]
        
    if properties["ARGS"][1] == " ":
        try:
            try:
                help_photon = subprocess.call(["photon", "--help"])
            except Exception:
                #in case of buggy photon pip installation
                help_photon = subprocess.call(["python3", "core/lib/Photon/photon.py", "--help"])
            arguments = input(" [§] Enter arguments (as you would after $photon -u ROOT on the commandline) :> ")
            assert "-u" not in arguments and "--url" not in arguments
        except AssertionError:
            arguments = input(" [-] Argument '-u' already present in command string.\n [§] Enter arguments (as you would after $photon -u ROOT on the commandline) :> ")
    else:
        arguments = properties["ARGS"][1]
        
    arglist = re.split("\s+", arguments)
    print(" [+] Starting Photon Scan (this will take a while, output piped into variable)")
    try:
        #command = "photon -u " + root + " " + arguments
        command = ["photon", "-u", root] + arglist
        results_photon = subprocess.check_output(command)
    except Exception:
        command = ["python3", "core/lib/Photon/photon.py", "-u", root] + arglist
        results_photon = subprocess.check_output(command)
    data = results_photon.decode().replace("<<","").replace(">>","")
    print(data)
    gprint("\n [+] Photon Scan finished! Saving to database...")
    save_data(database, module, lvl1, lvl2, lvl3, root, data)
    
def attack(web):
    web = web.fullurl
    photon(web)
