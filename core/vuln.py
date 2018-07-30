#!/usr/bin/env python2

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import os
import time
import random
from random import *
from webbugs import *
from vulnban import *
from othbugs import *
from serbugs import *
from auxil import *
from colors import *

def vuln(web):

    v = raw_input(''+O+' \033[4mTID\033[1;0m '+GR+':> ' + color.END)
    print '\n'

    if v == '1':
	webbugs(web)

    elif v == '2':
	serbugs(web)

    elif v == '3':
	othbugs(web)

    elif v == '99':
	print '[!] Back'
	time.sleep(0.7)
	os.system('clear')

    else:
	dope = ['You high dude?','Hey there! Enter a valid option','Whoops! Thats not an option','Sorry fam! You just typed shit']
	print dope[randint(0,3)]
	time.sleep(0.7)
	os.system('clear')
	vulnban()
	vuln(web)

