#!/usr/bin/env python
from core.Core.colors import *

def portscan(web):
    from core.Core.build_menu import buildmenu
    print(ORANGE+'\n     +--------------+')
    print(ORANGE+'     |  '+WHITE+'SCAN TYPES'+ORANGE+'  |')
    print(ORANGE+'     +--------------+\n')
    menu = { # '#' : ['module', 'description', 'function']
        '1':['A Simple Port Scan','','simpleport'],\
        '2':['TCP Connect Scan','(Highly Reliable)','tcpconnectscan'],\
        '3':['TCP Stealth Scan','(Highly Reliable)','tcpstealthscan'],\
        '4':['XMAS Flag Scan','(Reliable only on LANS)','xmasscan'],\
        '5':['FIN Flag Scan','(Reliable only on LANS)','finscan'],\
        '6':['Open Ports Services Detector','','servicedetect'],\
    }
    buildmenu(web,menu,'Port Scanning','')          # build menu
    raw_input(O+' [#] Press '+GREEN+'Enter'+ORANGE+' to continue...')