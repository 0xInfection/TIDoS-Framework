#!/usr/bin/env python
from core.Core.arts import footprintban_art

def footprint(web):
    from core.Core.build_menu import buildmenu
    menu = { # '#' : ['module', 'description', 'function']
        '1':['Passive Footprinting','(Open Source Intelligence)','passiveo'],\
        '2':['Active Reconnaissance','(Gather via Interaction)','activeo'],\
        '3':['Information Disclosure','(Errors, Emails, etc)','infodisc'],\
    }
    buildmenu(web,menu,'Footprinting',footprintban_art)          # build menu