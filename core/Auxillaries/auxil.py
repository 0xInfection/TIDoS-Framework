#!/usr/bin/env python
from core.Core.arts import auxilban_art
# import subprocess
# from subprocess import call
def auxil(web):
    from core.Core.build_menu import buildmenu
    menu = { # '#' : ['module', 'description', 'function']
        '1':['Generate Hashes','','hashes'],\
        '2':['Encode Strings','','encodeall'],\
        '3':['Extract Metadata','','imgext'],\
        '4':['Honeypot Detector','','honeypot'],\
    }
    buildmenu(web,menu,'Auxillaries',auxilban_art)          # build menu