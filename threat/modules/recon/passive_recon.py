#!/usr/bin/env python

def passive_recon(target):
    from core.build_menu import buildmenu
    menu = { # '#' : ['module', 'description', 'function']
        '1':['dig','(Open Source Intelligence)','dig'],\
        '2':['whois lookup','(Gather via Interaction)','whois'],\
        '3':['Information Disclosure','(Errors, Emails, etc)','xxx'],\
    }
    buildmenu(target,menu,'Passive Reconnaissance & OSINT','')          # build menu