#!/usr/bin/env python

def recon(target):
    from core.build_menu import buildmenu
    menu = { # '#' : ['module', 'description', 'function']
        '1':['Passive Reconnaissance','(Open Source Intelligence)','passive_recon'],\
        '2':['Active Reconnaissance','(Gather via Interaction)','active_recon'],\
        '3':['Information Disclosure','(Errors, Emails, etc)','info_disclosure'],\
    }
    buildmenu(target,menu,'Reconnaissance & OSINT','')          # build menu