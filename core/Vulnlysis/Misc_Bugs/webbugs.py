#!/usr/bin/env python
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import time
import os
import sys
sys.path.append('modules/0x03-Vulnerability+Analysis/0x02-MisconfigurationBugs/')

from icors import *
from ssscript import *
from clickjack import *
from zone import *
from hhi import *
from netmisc import *
from cloudflaremisc import *
from hsts import *
from sessionfix import *
from headers import *
from xsstrace import *
from cookiecheck import *
from mailspoof import *
from core.Core.colors import *
from core.Vulnlysis.Misc_Bugs.webbugsban import *

def webbugs(web):

    print(W+'\n [*] Type Selected : Basic Web Bugs and Misconfigurations...')
    webbugsban()
    v = raw_input(O+B+' [#] \033[4mTID\033[1;0m '+GR+':> ' + color.END)
    print('\n')
    if v.strip() == '1':
        print(B+' [!] Type Selected :'+C+' iCORS')
        icors(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == '2':
        print(B+' [!] Type Selected :'+C+' Same Site Scripting')
        ssscript(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == '3':
        print(B+' [!] Type Selected :'+C+' Clickjack')
        clickjack(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == '4':
        print(B+' [!] Type Selected :'+C+' Zone Transfer')
        zone(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == '5':
        print(B+' [!] Type Selected :'+C+' Cookie Check')
        cookiecheck(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == '6':
        print(B+' [!] Type Selected :'+C+' Sec. Headers')
        headers(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == '7':
        print(B+' [!] Type Selected :'+C+' Cloudflare Misconfig.')
        cloudflaremisc(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == '8':
        print(B+' [!] Type Selected :'+C+' HSTS Check')
        hsts(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == '9':
        print(B+' [!] Type Selected :'+C+' Cross Site Tracing')
        xsstrace(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == '10':
        print(B+' [!] Type Selected :'+C+' Telnet Enabled')
        netmisc(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == '11':
        print(B+' [!] Type Selected :'+C+' Email Spoof')
        mailspoof(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == '12':
        print(B+' [!] Type Selected :'+C+' Host Header Injection')
        hhi(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == '13':
        print(B+' [!] Type Selected :'+C+' Cookie Injection')
        sessionfix(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == 'A':
        print(B+' [!] Type Selected : All Modules')
        time.sleep(0.5)

        print(B+' [*] Firing up module -->'+C+' iCORS')
        icors(web)
        print(B+'\n [!] Module Completed -->'+C+' iCORS\n')
        time.sleep(1)

        print(B+' [*] Firing up module -->'+C+' SSS ')
        ssscript(web)
        print(B+'\n [!] Module Completed -->'+C+' SSS \n')
        time.sleep(1)

        print(B+' [*] Firing up module -->'+C+' ClickJacking')
        clickjack(web)
        print(B+'\n [!] Module Completed -->'+C+' ClickJacking\n')
        time.sleep(1)

        print(B+' [*] Firing up module -->'+C+' Zone Transfer')
        zone(web)
        print(B+'\n [!] Module Completed -->'+C+' Zone Transfer\n')
        time.sleep(1)

        print(B+' [*] Firing up module -->'+C+' Cookie Check')
        cookiecheck(web)
        print(B+'\n [!] Module Completed -->'+C+' Cookie Check\n')
        time.sleep(1)

        print(B+' [*] Firing up module -->'+C+' Security Headers ')
        headers(web)
        print(B+'\n [!] Module Completed -->'+C+' Security Headers \n')
        time.sleep(1)

        print(B+' [*] Firing up module -->'+C+' Cloudflare Misconfig.')
        cloudflaremisc(web)
        print(B+'\n [!] Module Completed -->'+C+' Cloudflare Misconfig.\n')
        time.sleep(1)

        print(B+' [*] Firing up module -->'+C+' Mail Spoofing')
        mailspoof(web)
        print(B+'\n [!] Module Completed -->'+C+' Mail Spoofing\n')
        time.sleep(0.5)

        print(B+' [*] Firing up module -->'+C+' HSTS Checker')
        hsts(web)
        print(B+'\n [!] Module Completed -->'+C+' HSTS Checker\n')
        time.sleep(0.5)

        print(B+' [*] Firing up module -->'+C+' Cross Site Tracing')
        xsstrace(web)
        print(B+'\n [!] Module Completed -->'+C+' Cross Site Tracing\n')
        time.sleep(0.5)

        print(B+' [*] Firing up module -->'+C+' Telnet Enabled')
        netmisc(web)
        print(B+'\n [!] Module Completed -->'+C+' Telnet Enabled\n')
        time.sleep(1)

        print(B+' [*] Firing up module -->'+C+' Host Header Injection')
        hhi(web)
        print(B+'\n [!] Module Completed -->'+C+' Host Header Injection\n')
        time.sleep(1)

        print(B+' [*] Firing up module -->'+C+' Cookie Injection')
        sessionfix(web)
        print(B+'\n [!] Module Completed -->'+C+' Cookie Injection\n')
        time.sleep(1)

        print(G+' [+] All modules successfully completed!')
        time.sleep(0.5)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        webbugs(web)

    elif v.strip() == '99':
        print('[!] Back')
        time.sleep(0.7)

    else:
        print('')
        dope = ['You high dude?','Hey there! Enter a valid option','Whoops! Thats not an option','Sorry fam! You just typed shit']
        print(dope[randint(0,3)])
        time.sleep(0.7)
        os.system('clear')
        webbugs(web)
