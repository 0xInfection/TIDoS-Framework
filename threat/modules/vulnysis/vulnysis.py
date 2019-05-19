#!/usr/bin/env python

def vulnysis(target):
    from core.build_menu import buildmenu
    art=''
    for host in target:
        host.module = 'VulnAnalysis'
    menu = { # '#' : ['module', 'description', 'function']
        '1':['Basic Bugs & Misconfigurations','(Low Priority [P0x3-P0x4])','misconfig'],\
        '2':['Critical Vulnerabilities','(High Priority [P0x1-P0x2])','critical'],\
        '3':['Others','(Bruter Force Tools)','other'],\
    }
    buildmenu(target,menu,'Vulnerability Analysis',art)          # build menu