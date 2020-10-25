#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import nmap
import time
from core.Core.colors import *
import socket
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module discovers possible Telnet misconfiguration."
searchinfo = "Telnet Checker"
properties = {}

def netmisc0x00(web):

    web = web.replace('http://','')
    web = web.replace('https://','')
    ip = socket.gethostbyname(web)
    port = 23 # telnet port
    try:
        print(O+' [!] Configuring scanner for telnet ports...')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        print(C+"\n [*] Connecting to '%s' via port %s" % (ip, port))
        r = sock.connect_ex((ip, port))
        time.sleep(0.1)
        if r == 0:
            print(G+' [+] Telnet port detected open!')
            time.sleep(0.5)
            print(O+' [*] Confirming...')
            nmScan = nmap.PortScanner()
            nmScan.scan(ip, '23')
            port = 23
            thisDict = nmScan[ip]['tcp'][port]
            print(G+' [+] Telnet network misconfiguration confirmed!')
            save_data(database, module, lvl1, lvl2, lvl3, name, "Telnet misconfiguration confirmed!")
            time.sleep(0.5)
            if thisDict['version']:
                print(G+' [+] Port ' + str(port) + ': ' +C+ thisDict['product'] +GR+ ', v' + thisDict['version'])
                data = "Port " + str(port) + ": " + thisDict["product"] + ", v" + thisDict["version"]
                save_data(database, module, lvl1, lvl2, lvl3, name, data)
            else:
                print(G+' [+] Port ' + str(port) + ': ' +C+ thisDict['product'])
                data = "Port " + str(port) + ": " + thisDict["product"]
                save_data(database, module, lvl1, lvl2, lvl3, name, data)
        else:
            print(R+' [-] Telnet Disabled!')
            save_data(database, module, lvl1, lvl2, lvl3, name, "Telnet disabled.")
        sock.close()

    except Exception as e:
        print('\n'+R+' [!] Exception detected at port %s !' % port)
        print(R+' [-] Error : '+str(e))

def netmisc(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = inspect.stack()[0][3]
    global module
    module = "VulnAnalysis"
    global lvl1
    lvl1 = "Basic Bugs & Misconfigurations"
    global lvl3
    lvl3 = ""
    #print(R+'\n    ===================================')
    #print(R+'\n     TELNET ENABLED (Network Misconf.)')
    #print(R+'    ---<>----<>----<>----<>----<>----<>\n')

    from core.methods.print import pvln
    pvln("network misconf.") 
                 

    print(GR+' [*] Loading up port scanner...')
    netmisc0x00(web)
    time.sleep(0.5)

def attack(web):
    web = web.fullurl
    netmisc(web)
