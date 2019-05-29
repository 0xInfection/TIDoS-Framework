#!/usr/bin/env python

def aux(target):
    from core.build_menu import buildmenu
    for host in target:
        host.module = 'AuxModules'
    menu = { # '#' : ['module', 'description', 'function']
        '1':['Generate Hashes','Generate Hashes from String','hashes'],\
        '2':['Encode/Decode Strings','Base64, Base32, Base16/Hex, URL','encodeall'],\
        # '3':['Extract Metadata','','imgext'],\
        '4':['Honeypot Detector','Shodan Honeypot Check','honeypot'],\
    }
    buildmenu(target,menu,'Aux Modules','')          # build menu