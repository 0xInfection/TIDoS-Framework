#!/usr/bin/env python

def vulnysis(target):
    from core.build_menu import buildmenu
    menu = { # '#' : ['module', 'description', 'function']
        '1':['Basic Bugs & Misconfigurations','(Low Priority [P0x3-P0x4])','xxx'],\
        '2':['Critical Vulnerabilities','(High Priority [P0x1-P0x2])','xxx'],\
        '3':['Others','(Bruter Force Tools)','xxx'],\
    }
    buildmenu(target,menu,'Vulnerability Analysis','')          # build menu