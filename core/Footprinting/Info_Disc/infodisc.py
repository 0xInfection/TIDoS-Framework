#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework

from __future__ import print_function
import sys
import os
import time
import subprocess
import random
from random import randint
sys.path.append('modules/0x01-OSINT+Footprinting/0x03-InformationDisclosure/')
from creditcards import *
from emailext import *
from errors import *
from phone import *
from ssn import *
from internalip import *
from core.Core.colors import *
from core.Footprinting.Info_Disc.infodiscban import *

def infodisc(web):

    print(" [!] Module Selected : Information Disclosure\n\n")
    infodiscban()
    print('')
    time.sleep(0.3)
    v = raw_input (''+GR+'  [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
    print('')
    if v == '1':
        print(C+' [!] Type Selected :'+B+' Credit Card Enumeration')
        creditcards(web)
        print('\n\n')
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        infodisc(web)

    elif v == '2':
        print(C+' [!] Type Selected :'+B+' Extract All Emails')
        emailext(web)
        print('\n\n')
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        infodisc(web)

    elif v == '3':
        print(C+' [!] Type Selected :'+B+' Enumerate Errors + FPD')
        errors(web)
        print('\n\n')
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        infodisc(web)

    elif v == '4':
        print(C+' [!] Type Selected :'+B+' Internal IP disclosure')
        internalip(web)
        print('\n\n')
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        infodisc(web)

    elif v == '5':
        print(C+' [!] Type Selected :'+B+' Phone Numbers Extract')
        phone(web)
        print('\n\n')
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        infodisc(web)

    elif v == '6':
        print(C+' [!] Type Selected :'+B+' Social Security Numbers')
        ssn(web)
        print('\n\n')
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        infodisc(web)

    elif v == 'A':
        print(C+' [!] Type Selected :'+B+' All Modules')
        time.sleep(0.5)
        print(C+' [*] Firing up module -->'+B+' Credit Cards')
        creditcards(web)
        print(C+' [!] Module Completed -->'+B+' Credit Cards\n')

        time.sleep(1)
        print(C+' [*] Firing up module -->'+B+' Email Extraction')
        emailext(web)
        print(C+' [!] Module Completed -->'+B+' Email Hunt\n')

        time.sleep(1)
        print(C+' [*] Firing up module -->'+B+' Errors Enumeration + FPD')
        errors(web)
        print(C+' [!] Module Completed -->'+B+' Errors Enumeration\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+B+' Extract Phone Numbers')
        phone(web)
        print(C+' [!] Module Completed -->'+B+' Extract Phone Numbers\n')
        time.sleep(1)

        print(C+' [*] Firing up module -->'+B+' Extract Social Security Numbers')
        ssn(web)
        print(C+' [!] Module Completed -->'+B+' Extract SSN\n')
        time.sleep(1)

        print(C+' [!] All scantypes have been tested on target...')
        time.sleep(1)
        print(C+' [*] Going back to menu...')
        infodisc(web)

    elif v == '99':
        print(C+' [*] Back to the menu !')
        time.sleep(0.8)
        os.system('clear')

    else:
        dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
        print(dope[randint(0,3)])
        time.sleep(0.7)
        os.system('clear')
        infodisc(web)
