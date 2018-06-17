#!/usr/bin/env python2
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import os
import time

from activeo import *
from infodisc import *
from footprintban import *
from footprint import *
from colors import *
from footprintban1 import *

def footprint_dup(web):

	m = raw_input(''+O+' [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
	print ''
	if m == '1':
	    passiveo(web)

	elif m == '2':
	    activeo(web)

	elif m == '3':
	    infodisc(web) 

	elif m == '99':
	    print ' [+] Back!'

	else:
	    print ''
	    dope = [' [*] You high dude?',' [*] Hey there! Enter a valid option',' [*] Whoops! Thats not an option',' [*] Sorry fam! You just typed shit']
	    print dope[randint(0,3)]
	    time.sleep(0.5)
	    footprintban1()
	    footprint_dup(web)
