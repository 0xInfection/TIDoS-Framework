#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This script is a part of TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


import sys
import time
from modules.VlnAnalysis.Severe.errorsqli import errorsqli
from modules.VlnAnalysis.Severe.blindsqli import blindsqli
from core.Core.colors import *

info = "This module scans the target for SQL Injection flaws, supporting both blind and error-based injection."
searchinfo = "SQL Injection Scanner"
properties = {"PARAM":["Directory and Parameter to attack (eg /vuln/page.php?q=lmao)", " "], "PARALLEL":["Parallelise Attack? [1/0]", " "]}

def sqli(web):

    print(GR+'\n [*] Loading module...')
    time.sleep(0.7)
    #print(R+'\n    ===========================')
    #print(R+'\n     S Q L   ! N J E C T I O N')
    #print(R+'    ——·‹›·––·‹›·——·‹›·——·‹›·——·\n')

    from core.methods.print import pvln
    pvln("sql !njection") 
                 
    time.sleep(0.6)
    print(O+' Choose from the options:\n')
    print(B+'  [1] '+C+'Error Based SQLi'+W+' (Manual + Automated)')
    print(B+'  [2] '+C+'Blind Based SQLi'+W+' (Manual + Automated)\n')
    print(B+'  [99] '+C+'Back to Console\n')
    v = input(O+' [§] TID :> ')

    if v.strip() == '1':
        errorsqli(web, properties)
    elif v.strip() == '2':
        blindsqli(web, properties)
    elif v.strip() == '99':
        pass
    else:
        print(R+' [-] U high dude?')

def attack(web):
    sqli(web)