#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
import os
import sys
from random import randint
from core.Core.colors import *
from modules.OSINTFootprinting.ActiveRecon.backupbrute import backupbrute
from modules.OSINTFootprinting.ActiveRecon.backbrute import backbrute
from modules.OSINTFootprinting.ActiveRecon.dotbrute import dotbrute
from modules.OSINTFootprinting.ActiveRecon.indexmulbrute import indexmulbrute
from modules.OSINTFootprinting.ActiveRecon.logbrute import logbrute
from modules.OSINTFootprinting.ActiveRecon.proxybrute import proxybrute
from modules.OSINTFootprinting.ActiveRecon.passbrute import passbrute

info = "This module looks for several interesting files on the webserver, like backdoors, backups and hidden files."
searchinfo = "Bruteforce Recon"
properties = {}

def filebrute(web):

    print(GR+' [*] Loading module...')
    print(B+" [!] Module Selected : "+C+"Bruteforce Modules\n\n")
    time.sleep(0.7)
    #print(R+'\n    ==================================')
    #print(R+'     B R U T E F O R C E   R E C O N.')
    #print(R+'    ==================================\n')
    from core.methods.print import posintact
    posintact("bruteforce recon") 

    print(O+' Choose from the following options :\n')
    print(B+'  [1]'+C+' Common Backdoor Paths '+W+' (.shell, c99.php, etc)')
    print(B+'  [2]'+C+' Common Backup Locations'+W+' (.bak, .db, etc)')
    print(B+'  [3]'+C+' Common Dot Files'+W+' (.phpinfo, .htaccess, etc)')
    print(B+'  [4]'+C+' Common Password Paths'+W+' (.skg, .pgp etc)')
    print(B+'  [5]'+C+' Common Proxy Config. Locations'+W+' (.pac, etc)')
    print(B+'  [6]'+C+' Multiple Index Locations'+W+' (index1, index2, etc)')
    print(B+'  [7]'+C+' Common Log Locations'+W+' (.log, changelogs, etc)\n')
    print(B+'  [A]'+C+' The Auto-Awesome Module\n')
    print(B+'  [99]'+C+' Back\n')
    time.sleep(0.3)
    v = input(C+'  [§] TID'+C+' :> ' + color.END)
    print('')
    if v.strip() == '1':
        print(B+' [!] Type Selected :'+C+' Backdoor Brute')
        backbrute(web)
        input(C+' [§] Press '+GR+'Enter'+C+' to continue...')
        print('\n\n')
        filebrute(web)

    elif v.strip() == '2':
        print(B+' [!] Type Selected :'+C+' Backup Brute')
        backupbrute(web)
        input(C+' [§] Press '+GR+'Enter'+C+' to continue...')
        print('\n\n')
        filebrute(web)

    elif v.strip() == '3':
        print(B+' [!] Type Selected :'+C+' Dot File Brute')
        dotbrute(web)
        input(C+' [§] Press '+GR+'Enter'+C+' to continue...')
        print('\n\n')
        filebrute(web)

    elif v.strip() == '4':
        print(B+' [!] Type Selected :'+C+' Password Brute')
        passbrute(web)
        input(C+' [§] Press '+GR+'Enter'+C+' to continue...')
        print('\n\n')
        filebrute(web)

    elif v.strip() == '5':
        print(B+' [!] Type Selected :'+C+' Proxy Brute')
        proxybrute(web)
        input(C+' [§] Press '+GR+'Enter'+C+' to continue...')
        print('\n\n')
        filebrute(web)

    elif v.strip() == '6':
        print(B+' [!] Type Selected :'+C+' Multiple Indices')
        indexmulbrute(web)
        input(C+' [§] Press '+GR+'Enter'+C+' to continue...')
        print('\n\n')
        filebrute(web)

    elif v.strip() == '7':
        print(B+' [!] Type Selected :'+C+' Log Locations')
        logbrute(web)
        input(C+' [§] Press '+GR+'Enter'+C+' to continue...')
        print('\n\n')
        filebrute(web)

    elif v == 'A':
        print(B+' [!] Type Selected :'+C+' All Modules')
        time.sleep(0.5)
        print(B+' [*] Firing up module -->'+C+' Backdoor Brute')
        backbrute(web)
        print(B+' [!] Module Completed -->'+C+' Backdoor Brute\n')
        time.sleep(2)

        print(B+' [*] Firing up module -->'+C+' Backup Brute')
        backupbrute(web)
        print(B+' [!] Module Completed -->'+C+' Backup Brute\n')
        time.sleep(2)

        print(B+' [*] Firing up module -->'+C+' Dot Brute')
        dotbrute(web)
        print(B+' [!] Module Completed -->'+C+' Dot Brute\n')
        time.sleep(2)

        print(B+' [*] Firing up module -->'+C+' Pass Brute')
        passbrute(web)
        print(B+' [!] Module Completed -->'+C+' Pass Brute\n')
        time.sleep(2)

        print(B+' [*] Firing up module -->'+C+' Proxy Brute')
        proxybrute(web)
        print(B+' [!] Module Completed -->'+C+' Proxy Brute\n')
        time.sleep(2)

        print(B+' [*] Firing up module -->'+C+' Multiple Index Brute')
        indexmulbrute(web)
        print(B+' [!] Module Completed -->'+C+' Multiple Index Brute\n')
        time.sleep(2)

        print(B+' [*] Firing up module -->'+C+' Log Brute')
        logbrute(web)
        print(B+' [!] Module Completed -->'+C+' Log Brute\n')
        time.sleep(2)

        print(B+' [!] All scantypes have been tested on target...')
        time.sleep(4)
        input(C+' [§] Press '+GR+'Enter'+C+' to continue...')
        print(B+' [*] Going back to menu...')

    elif v == '99':
        print(B+' [*] Back to the menu !')

    else:
        dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
        print(' [-] '+ dope[randint(0,3)])
        time.sleep(0.7)
        os.system('clear')
        filebrute(web)

def attack(web):
    web = web.fullurl
    filebrute(web)