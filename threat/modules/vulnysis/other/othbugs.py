#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import sys
import os
import time
import subprocess
import random
from random import randint
sys.path.append('modules/0x03-Vulnerability+Analysis/0x03-OtherWebBugs/')
from popbrute import *
from ftpbrute import *
from sqlbrute import *
from sshbrute import *
from smtpbrute import *
from xmppbrute import *
from telnetbrute import *
from core.Core.colors import *
from core.Vulnlysis.Oth_Bugs.othbugsban import *

def othbugs(web):

    print(" [!] Module Selected : Bruteforce Modules\n\n")
    othbugsban()
    print('')
    time.sleep(0.3)
    v = raw_input (GR+'  [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
    print('')
    if v == '1':
        print(B+' [!] Type Selected :'+C+' FTP Brute')
        ftpbrute(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        print('\n\n')
        othbugs(web)

    elif v == '2':
        print(B+' [!] Type Selected :'+C+' SSH Brute')
        sshbrute(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        print('\n\n')
        othbugs(web)

    elif v == '3':
        print(B+' [!] Type Selected :'+C+' SQL Brute')
        sqlbrute(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        print('\n\n')
        othbugs(web)

    elif v == '4':
        print(B+' [!] Type Selected :'+C+' POP 3/2 Brute')
        popbrute(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        print('\n\n')
        othbugs(web)

    elif v == '5':
        print(B+' [!] Type Selected :'+C+' SMTP Brute')
        smtpbrute(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        print('\n\n')
        othbugs(web)

    elif v == '6':
        print(B+' [!] Type Selected :'+C+' TELNET Brute')
        telnetbrute(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        print('\n\n')
        othbugs(web)

    elif v == '7':
        print(B+' [!] Type Selected :'+C+' XMPP Brute')
        xmppbrute(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        print('\n\n')
        othbugs(web)

    elif v == 'A':
        print(B+' [!] Type Selected :'+C+' All Modules')
        time.sleep(0.5)
        print(B+' [*] Firing up module -->'+C+' FTP Brute')
        ftpbrute(web)
        print(B+' [!] Module Completed -->'+C+' FTP Brute\n')
        time.sleep(2)

        print(B+' [*] Firing up module -->'+C+' SSH Brute')
        sshbrute(web)
        print(B+' [!] Module Completed -->'+C+' SSH Brute\n')
        time.sleep(2)

        print(B+' [*] Firing up module -->'+C+' SQL Brute')
        sqlbrute(web)
        print(B+' [!] Module Completed -->'+C+' SQL Brute\n')
        time.sleep(2)

        print(B+' [*] Firing up module -->'+C+' POP Brute')
        popbrute(web)
        print(B+' [!] Module Completed -->'+C+' POP Brute\n')
        time.sleep(2)

        print(B+' [*] Firing up module -->'+C+' SMTP Brute')
        smtpbrute(web)
        print(B+' [!] Module Completed -->'+C+' SMTP Brute\n')
        time.sleep(2)

        print(B+' [*] Firing up module -->'+C+' TElNET Brute')
        telnetbrute(web)
        print(B+' [!] Module Completed -->'+C+' TELNET Brute\n')
        time.sleep(2)

        print(B+' [*] Firing up module -->'+C+' XMPP Brute')
        xmppbrute(web)
        print(B+' [!] Module Completed -->'+C+' XMPP Brute\n')
        time.sleep(2)

        print(B+' [!] All scantypes have been tested on target...')
        time.sleep(4)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        print(B+' [*] Going back to menu...')
        othbugs(web)

    elif v == '99':
        print(GR+' [*] Going back...')
        time.sleep(0.5)
        os.system('clear')

    else:
        dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
        print(dope[randint(0,3)])
        time.sleep(0.7)
        os.system('clear')
        othbugs(web)
