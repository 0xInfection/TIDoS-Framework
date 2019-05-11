#!/usr/bin/env python
from core.Core.arts import vulnban_art

def vuln(web):
    from core.Core.build_menu import buildmenu
    menu = { # '#' : ['module', 'description', 'function']
        '1':['Basic Bugs & Misconfigurations','(Low Priority [P0x3-P0x4])','webbugs'],\
        '2':['Critical Vulnerabilities','(High Priority [P0x1-P0x2])','serbugs'],\
        '3':['Others','(Bruter Force Tools)','othbugs'],\
    }
    buildmenu(web,menu,'Vulnerability Analysis',vulnban_art)          # build menu