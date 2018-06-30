#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import sys
import os
import time
import subprocess
import random
from random import randint
sys.path.append('modules/AuxilMods/')
from popbrute import *
from ftpbrute import *
from sqlbrute import *
from auxil_alt import *
from sshbrute import *
from brutemodsban import *
from colors import *
from smtpbrute import *
from xmppbrute import *
from telnetbrute import *

def brutemods(web):

    print " [!] Module Selected : Bruteforce Modules\n\n"
    brutemodsban()
    print ''
    time.sleep(0.3)
    v = raw_input (''+GR+'  [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
    print ''
    if v == '1':
	print B+' [!] Type Selected :'+C+' FTP Brute'
	ftpbrute(web)
	time.sleep(2)
	print '\n\n'
	auxil_alt(web)

    elif v == '2':
	print B+' [!] Type Selected :'+C+' SSH Brute'
	sshbrute(web)
	time.sleep(2)
	print '\n\n'
	auxil_alt(web)

    elif v == '3':
	print B+' [!] Type Selected :'+C+' SQL Brute'
	sqlbrute(web)
	time.sleep(2)
	print '\n\n'
	auxil_alt(web)

    elif v == '4':
	print B+' [!] Type Selected :'+C+' POP 3/2 Brute'
	popbrute(web)
	time.sleep(2)
	print '\n\n'
	auxil_alt(web)

    elif v == '5':
	print B+' [!] Type Selected :'+C+' SMTP Brute'
	smtpbrute(web)
	time.sleep(2)
	print '\n\n'
	auxil_alt(web)

    elif v == '6':
	print B+' [!] Type Selected :'+C+' TELNET Brute'
	telnetbrute(web)
	time.sleep(2)
	print '\n\n'
	auxil_alt(web)

    elif v == '7':
	print B+' [!] Type Selected :'+C+' XMPP Brute'
	xmppbrute(web)
	time.sleep(2)
	print '\n\n'
	auxil_alt(web)

    elif v == 'A':
	print B+' [!] Type Selected :'+C+' All Modules'
	time.sleep(0.5)
	print B+' [*] Firing up module -->'+C+' FTP Brute'
	ftpbrute(web)
	print B+' [!] Module Completed -->'+C+' FTP Brute\n'

	print B+' [*] Firing up module -->'+C+' SSH Brute'
	sshbrute(web)
	print B+' [!] Module Completed -->'+C+' SSH Brute\n'
	time.sleep(2)

	print B+' [*] Firing up module -->'+C+' SQL Brute'
	sqlbrute(web)
	print B+' [!] Module Completed -->'+C+' SQL Brute\n'
	time.sleep(2)

	print B+' [*] Firing up module -->'+C+' POP Brute'
	popbrute(web)
	print B+' [!] Module Completed -->'+C+' POP Brute\n'
	time.sleep(2)

	print B+' [*] Firing up module -->'+C+' SMTP Brute'
	smtpbrute(web)
	print B+' [!] Module Completed -->'+C+' SMTP Brute\n'
	time.sleep(2)

	print B+' [*] Firing up module -->'+C+' TElNET Brute'
	telnetbrute(web)
	print B+' [!] Module Completed -->'+C+' TELNET Brute\n'
	time.sleep(2)

	print B+' [*] Firing up module -->'+C+' XMPP Brute'
	xmppbrute(web)
	print B+' [!] Module Completed -->'+C+' XMPP Brute\n'
	time.sleep(2)

	print B+' [!] All scantypes have been tested on target...'
	time.sleep(4)
	print B+' [*] Going back to menu...'
	auxil_alt(web)

    elif v == '99':
	print B+' [*] Back to the menu !'
	auxil_alt(web) 

    else:
	dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
	print dope[randint(0,3)]
	time.sleep(0.7)
	os.system('clear')
	brutemods(web)

