#!/usr/bin/env python
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import sys
import time
import os
from random import randint
sys.path.append('modules/0x01-OSINT+Footprinting/0x01-PassiveReconnaissance/')

from dnschk import *
from piweb import *
from getgeoip import *
from revip import *
from revdns import *
from getconinfo import *
from subdom import *
from googlenum import *
from links import *
from censysdom import *
from subnet import *
from hackedmail import *
from iphistory import *
from mailtodom import *
from checkuser import *
from googlegroups import *
from threatintel import *
from webarchive import *
from googledorker import *
from googleSearch import *
from whoischeckup import *
from pastebin import *
from linkedin import *
from core.Core.colors import *
from core.Footprinting.Passive_Recon.passiveban import *

def passiveo(web):

    print(" [!] Module Selected : Passive Reconnaissance\n")
    passiveban()
    v = raw_input (''+GR+'  [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
    print('\n\n')
    if v.strip() == '1':
        print(C+' [!] Type Selected '+B+': Ping Check')
        piweb(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '2':
        print(C+' [!] Type Selected '+B+': WhoIS Checkup')
        whoischeckup(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '3':
        print(C+' [!] Type Selected '+B+': GeoIP Lookup')
        getgeoip(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '4':
        print(C+' [!] Type Selected '+B+': DNS Lookup')
        dnschk(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '5':
        print(C+' [!] Type Selected '+B+': Subdomain Scan')
        subdom(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '6':
        print(C+' [!] Type Selected '+B+': Reverse DNS Lookup')
        revdns(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '7':
        print(C+' [!] Type Selected : Subnet Enumeration')
        subnet(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '8':
        print(C+' [!] Type Selected '+B+': Reverse IP Lookup')
        revip(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '9':
        print(C+' [!] Type Selected '+B+': IP History')
        iphistory(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '10':
        print(C+' [!] Type Selected '+B+': Page Links')
        links(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '11':
        print(C+' [!] Type Selected '+B+': Google Search')
        googleSearch()
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '12':
        print(C+' [!] Type Selected '+B+': Google Dorker')
        googledorker(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '13':
        print(C+' [!] Type Selected '+B+': Wayback Machine')
        webarchive(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '14':
        print(C+' [!] Type Selected '+B+': Hacked Email Check')
        hackedmail()
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '15':
        print(C+' [!] Type Selected '+B+': Mail to Domain')
        mailtodom()
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '16':
        print(C+' [!] Type Selected '+B+': Google Groups Enum')
        googlegroups(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '17':
        print(C+' [!] Type Selected '+B+': Check Username')
        checkuser(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '18':
        print(C+' [!] Type Selected '+B+': PasteBin Posts')
        pastebin(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '19':
        print(C+' [!] Type Selected '+B+': LinkedIn Gathering')
        linkedin(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '20':
        print(C+' [!] Type Selected '+B+': Google Plus Gathering')
        googlenum(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '21':
        print(C+' [!] Type Selected '+B+': Public Contact Info')
        getconinfo(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '22':
        print(C+' [!] Type Selected '+B+': CENSYS Gathering')
        censysdom(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '23':
        print(C+' [!] Type Selected '+B+': Threat Intel Gathering')
        threatintel(web)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        passiveo(web)

    elif v.strip() == '99':
        print(C+' [*] Back!')
        time.sleep(0.7)
        os.system('clear')

    elif v.strip() == 'A':
        print(C+' [!] Type Selected '+B+': All Modules\n')
        time.sleep(0.5)

        print(C+' [*] Firing up module -->'+O+' Ping Check')
        piweb(web)
        print(C+'\n [!] Module Completed -->'+O+' Piweb\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' WHOIS ')
        whoischeckup(web)
        print(C+'\n [!] Module Completed -->'+O+' WHOIS\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' GeoIP Lookup ')
        getgeoip(web)
        print(C+'\n [!] Module Completed -->'+O+' GeoIP\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' DNS Enumeration ')
        dnschk(web)
        print(C+'\n [!] Module Completed -->'+O+' DNS Enum\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' Subdomain Scan ')
        subdom(web)
        print(C+'\n [!] Module Completed -->'+O+' Subdom\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' Subnet Calc. ')
        subnet(web)
        print(C+'\n [!] Module Completed -->'+O+' Subnet Calculation\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' Reverse DNS Lookup ')
        revdns(web)
        print(C+'\n [!] Module Completed -->'+O+' RevDNS\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' IP History Lookup ')
        iphistory(web)
        print(C+'\n [!] Module Completed -->'+O+' RevIP\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' Reverse IP Lookup ')
        revip(web)
        print(C+'\n [!] Module Completed -->'+O+' RevIP\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' Web Links ')
        links(web)
        print(C+'\n [!] Module Completed -->'+O+' Web Links\n')
        time.sleep(1)

        print(C+' [!] Firing up module -->'+O+' Google Search')
        googleSearch()
        print(C+'\n [!] Module Completed -->'+O+' GSearch\n')
        time.sleep(1)

        print(C+' [!] Firing up module -->'+O+' WayBack Machine')
        webarchive(web)
        print(C+'\n [!] Module Completed -->'+O+' WayBack Machine\n')
        time.sleep(1)

        print(C+' [!] Firing up module -->'+O+' Hacked Email Checker')
        hackedmail()
        print(C+'\n [!] Module Completed -->'+O+' Hacked Email\n')
        time.sleep(1)

        print(C+' [!] Firing up module -->'+O+' Mail to Domain')
        mailtodom()
        print(C+'\n [!] Module Completed -->'+O+' Mail to Domain\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' Google Groups Enum')
        googlegroups(web)
        print(C+'\n [!] Module Completed -->'+O+' GGroups\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' Check Username')
        checkuser(web)
        print(C+'\n [!] Module Completed -->'+O+' Username\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' LinkedIn gathering')
        linkedin(web)
        print(C+'\n [!] Module Completed -->'+O+' LinkedIn\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' Pastebin Posts')
        pastebin(web)
        print(C+'\n [!] Module Completed -->'+O+' Pastebin\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' Google Plus Gathering')
        googlenum(web)
        print(C+'\n [!] Module Completed -->'+O+' Google Plus Gathering\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' Google Dorker')
        googledorker(web)
        print(C+'\n [!] Module Completed -->'+O+' GDorker\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' Public Contact Info')
        getconinfo(web)
        print(C+'\n [!] Module Completed -->'+O+' Public Contact info\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' Gathering via CENSYS')
        censysdom(web)
        print(C+'\n [!] Module Completed -->'+O+' CENSYS Gathering\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+O+' Threat Intelligence')
        threatintel(web)
        print(C+'\n [!] Module Completed -->'+O+' Threat Intelligence\n')
        time.sleep(1)

        print(G+' [+] All modules successfully completed!')
        time.sleep(3)
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        print(GR+' [*] Going back...')
        os.system('clear')
        passiveo(web)

    else:
        dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
        print(C+'\n [!] '+dope[randint(0,3)])
        os.system('clear')
        passiveo(web)
