#!/usr/bin/env python

# menu 3

def windows_enum(target):
    from core.build_menu import buildmenu
    print('MENU 3')
    menu = { # '#' : ['module', 'description', 'function']
        '1':['enum4linux','(SMB Enumeration)','enum4linux'],\
    }
    buildmenu(target,menu,'Windows Enumeration','')         # build menu