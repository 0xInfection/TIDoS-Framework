#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import sys, warnings
warnings.filterwarnings("ignore")
from core.tidos_main import *
from core.Core.colors import *

if __name__=='__main__':
    try:
        tidos_main()
    except KeyboardInterrupt:
        print(RED+' [-] User Interruption Detected!')
        print(BLUE+'\n [!] "Alvida", mate... See ya...\n')
        sys.exit(1)
