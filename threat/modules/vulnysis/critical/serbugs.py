#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import sys
import time
import os
sys.path.append('modules/0x03-Vulnerability+Analysis/0x01-TopPriorityBugs/')

from serbugsban import *
from lfi import *
from rfi import *
from ldap import *
from rce import *
from csrf import *
from sqli import *
from crlf import *
from subdomover import *
from strutsshock import *
from phpi import *
from htmli import *
from xpathi import *
from shellshock import *
from core.Core.colors import *
from xss import *
from openredirect import *
from pathtrav import *

def serbugs(web):

    print(GR+'\n [*] Loading module...')
    serbugsban()
    v = raw_input(''+O+' \033[4mTID\033[1;0m '+GR+':> ' + color.END)
    print('\n')
    if v.strip() == '1':
        print(' Type Selected : LFI')
        lfi(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '2':
        print(' Type Selected : RFI')
        rfi(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '3':
        print(' Type Selected : RCE')
        rce(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '4':
        print(' Type Selected : Path Traversal')
        pathtrav(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '5':
        print(' Type Selected : CSRF')
        csrf(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '6':
        print(' Type Selected : XSS')
        xss(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '7':
        print(' Type Selected : SQLi')
        sqli(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '8':
        print(' Type Selected : LDAP Injection')
        ldap(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '9':
        print(' Type Selected : HTML Code Injection')
        htmli(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '10':
        print(' Type Selected : HTTP Response Splitting')
        crlf(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '11':
        print(' Type Selected : PHP Code Injection')
        phpi(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '12':
        print(' Type Selected : XPATH Injection')
        xpathi(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '13':
        print(' Type Selected : Shellshock')
        shellshock(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '14':
        print(' Type Selected : Apache Struts Shock')
        strutsshock(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '15':
        print(' Type Selected : URL Validation')
        redirect(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '16':
        print(' Type Selected : Subdomain Takeover')
        subdomover(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == 'A':
        print(' [!] Type Selected : All Modules')
        time.sleep(0.5)

        print(' [*] Firing up module --> LFI')
        lfi(web)
        print(' [!] Module Completed --> LFI\n')
        time.sleep(1)

        print(' [*] Firing up module --> RFI ')
        rfi(web)
        print(' [!] Module Completed --> RFI \n')
        time.sleep(1)

        print(' [*] Firing up module --> RCE')
        rce(web)
        print(' [!] Module Completed --> RCE\n')
        time.sleep(1)

        print(' [*] Firing up module --> Path Traversal')
        pathtrav(web)
        print(' [!] Module Completed --> Path Traversal\n')
        time.sleep(1)

        print(' [*] Firing up module --> CSRF')
        csrf(web)
        print(' [!] Module Completed --> CSRF\n')
        time.sleep(1)

        print(' [*] Firing up module --> XSS ')
        xss(web)
        print(' [!] Module Completed --> XSS \n')
        time.sleep(1)

        print(' [*] Firing up module --> SQLi')
        sqli(web)
        print(' [!] Module Completed --> SQLi\n')
        time.sleep(1)

        print(' [*] Firing up module --> LDAPi')
        ldap(web)
        print(' [!] Module Completed --> LDAPi\n')
        time.sleep(1)

        print(' [*] Firing up module --> CRLF')
        crlf(web)
        print(' [!] Module Completed --> CRLF\n')
        time.sleep(1)

        print(' [*] Firing up module --> PHP Code Injection')
        phpi(web)
        print(' [!] Module Completed --> PHP Code Injection\n')
        time.sleep(0.5)

        print(' [*] Firing up module --> XPATH Injection')
        xpathi(web)
        print(' [!] Module Completed --> XPATH Injection\n')
        time.sleep(0.5)

        print(' [*] Firing up module --> ShellShock')
        shellshock(web)
        print(' [!] Module Completed --> ShellShock\n')
        time.sleep(1)

        print(' [*] Firing up module --> URL Forwards')
        redirect(web)
        print(' [!] Module Completed --> Url Forwards\n')
        time.sleep(0.5)
        print(G+' [+] All modules successfully completed!')
        time.sleep(4)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        serbugs(web)

    elif v.strip() == '99':
        print('[!] Back')
        time.sleep(0.7)

    else:
        print('')
        dope = ['You high dude?','Hey there! Enter a valid option','Whoops! Thats not an option','Sorry fam! You just typed shit']
        print(dope[randint(0,3)])
        time.sleep(0.7)
        os.system('clear')

        time.sleep(1)
        serbugs(web)
