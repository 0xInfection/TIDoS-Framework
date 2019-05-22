#!/usr/bin/env python

import subprocess

def nikto_help(target):
    from core.build_menu import buildmenu

    nikto_help = subprocess('nikto -H', shell=True)

    print(" " + color.custom('[B] Back',bold=True,white=True,bg_red=True)+'\n')

    buildmenu(target,target[0].last_menu,'','')