#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework

import sys, time
sys.path.append('core/')
from tidos_main import *

try:
    tidos_main()
except KeyboardInterrupt:
    print R+' [-] User Interruption Detected!'
    print C+' [+] Exiting...'
    time.sleep(0.5)
    print B+'\n [!] "Alvida", mate... See ya...\n'
    sys.exit(1)
