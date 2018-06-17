#!/usr/bin/env python2

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import os
import time
import random
from random import *
from vulnban import *
from webbugs import *
from vulnban1 import *
from webbugsban import *
from serbugsban import *
from auxilban import *
from tid_alt import tid_alt
from serbugs import *
from auxil import *
from colors import *
from subprocess import call

def vul_alt(web):

    v = raw_input(''+O+' \033[4mTID\033[1;0m '+GR+':> ' + color.END)
    print '\n'

    if v == '1':
	webbugsban()
	webbugs(web)

    elif v == '2':
	serbugsban()
	serbugs(web)

    elif v == '3':
	auxilban()
	auxil(web)

    elif v == '99':
	print '[!] Back'
	time.sleep(0.7)
	tld_alt(web)

    else:
	dope = ['You high dude?','Hey there! Enter a valid option','Whoops! Thats not an option','Sorry fam! You just typed shit']
	print dope[randint(0,3)]
	time.sleep(0.7)
	os.system('clear')
	vulnban1()
	vul_alt(web)

