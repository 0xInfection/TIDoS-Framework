#!/usr/bin/env python

import subprocess
from core.colors import color

def nmap_menu(target):
    from core.build_menu import buildmenu
    menu = { # '#' : ['module', 'description', 'function']
        '1':['Run NMAP','Run your nmap string','nmap'],\
        '2':['Edit NMAP String','Create or Edit your NMAP String','nmap_editor']
    }

    buildmenu(target,menu,'NMAP Configuration','')          # build menu