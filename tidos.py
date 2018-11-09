#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import sys, time, warnings
warnings.filterwarnings("ignore")
from core.tidos_main import *

try:
    tidos_main()
except KeyboardInterrupt:
    print(R+' [-] User Interruption Detected!')
    time.sleep(0.5)
    print(B+'\n [!] "Alvida", mate... See ya...\n')
    sys.exit(1)
