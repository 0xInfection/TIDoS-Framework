#!/usr/bin/env python2
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import os, requests, time
from time import sleep
from colors import *

def piwebenum(web):

    time.sleep(0.4)
    d = web.strip('http://')
    d = web.strip('https://')
    print R+'\n   ============================================='
    print R+'    P I N G / N P I N G   E N U M E R A T I O N'
    print R+'   =============================================\n'
    print GR + color.BOLD + ' [!] Pinging website...'
    time.sleep(0.5)
    print O+' [*] Using adaptative ping and debug mode with count 5...'
    time.sleep(0.4)
    print GR+' [!] Press Ctrl+C to stop\n'+C
    os.system('ping -D -c 5 '+ str(d))
    print ''
    time.sleep(0.6)
    print O+' [*] Trying NPing (NMap Ping)...'
    print C+" [~] Result: \n"
    print ''
    text = requests.get('http://api.hackertarget.com/nping/?q=' + d).text
    nping = str(text)
    print G+ nping +'\n'
