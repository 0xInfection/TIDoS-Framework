#!/usr/bin/env python2
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import os
import time

def footprint(web):

	from passiveo import *
	from activeo import *
	from infodisc import *
	from footprintban import *
	from colors import *

	m = raw_input(O+' [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
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
	    footprintban()
	    footprint(web)
