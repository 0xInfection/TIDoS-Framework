#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This script is a part of TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework

import sys
import time
from errorsqli import *
from blindsqli import *
from colors import *

def sqli(web):

	print GR+'\n [*] Loading module...'
	time.sleep(0.7)
	print R+'\n    ==========================='
	print R+'     S Q L   ! N J E C T I O N'
	print R+'    ===========================\n'
	time.sleep(0.6)
	print O+' Choose from the options:\n'
	print B+'  [1] '+C+'Error Based SQLi'+W+' (Manual + Automated)'
	print B+'  [2] '+C+'Blind Based SQLi'+W+' (Manual + Automated)\n'
	v = raw_input(O+' [#] TID :> ')

	if v.strip() == '1':
		errorsqli(web)
	elif v.strip() == '2':
		blindsqli(web)
	else:
		print R+' [-] U high dude?'

