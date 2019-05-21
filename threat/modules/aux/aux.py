#!/usr/bin/env python

def aux(target):
    from core.build_menu import buildmenu
    for host in target:
        host.module = 'AuxModules'
    menu = { # '#' : ['module', 'description', 'function']
        '1':['Generate Hashes','','hashes'],\
        '2':['Encode Strings','','encodeall'],\
        '3':['Extract Metadata','','imgext'],\
        '4':['Honeypot Detector','','honeypot'],\
    }
    buildmenu(target,menu,'Aux Modules','')          # build menu