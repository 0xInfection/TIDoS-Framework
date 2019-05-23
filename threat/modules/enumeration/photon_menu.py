#!/usr/bin/env python

import subprocess
from core.colors import color
# from os import path
# import sys
# sys.path.append(path.abspath('threat/lib/Photon'))

# from Photon.photon import photon

def photon_website(target):
    website = input('\n[#] Enter New Target Website:> ')
    for host in target:
        host.name = website
        host.website = website
    return photon_menu(target)

def photon_options(target):
    all_options = []
    options_str = ''

    options = input('\n[#] List Command Options to Add (e.g. -dbcheck,-Display+):> ').replace(' ','').split(',')

    for option in options:
        if option.endswith('+'):
            option_value = input('\n[#] Option ' + option + ' requires a value!:> ')
            all_options.append({option.strip('+'):option_value})
            options_str += option.strip('+') + ' ' + option_value + ' '
        else:
            all_options.append({option:''})
            options_str += option + ' '

    for host in target:
        host.options_list = all_options
        host.options_str = options_str

    return photon_menu(target)

def photon_menu(target):
    from core.build_menu import buildmenu

    print('PHOTON MENU')
    print('TARGET DICT', dict(target[0]))

    photon_site = ''
    photon_options = ''

    target_website = photon_site if photon_site else target[0].website
    target_options = photon_options if photon_options else target[0].options_str

    current_cmd_str = 'photon -u ' + target_website + ' ' + target_options

    for host in target:
        # host.module = 'ScanANDEnum'
        # host.lvl1 = 'Scanning & Enumeration'
        host.help = 'photon'
        host.lvl2 = 'Photon'

        photon_site = host.website
        photon_options = host.options_str
        host.cmd_str = current_cmd_str


    menu = { # '#' : ['module', 'description', 'function']
        '1':['Update Target Website',target_website,'photon_website'],\
        '2':['Update Command Options',target_options,'photon_options'],\
        '3':['Run Crawler','(Run Current Crawler Command)','xxx'],\
    }

    current_cmd = '\n' + '-'*55 + '\n' + color.green('Current Photon Command:  \n') + color.red(current_cmd_str) + '\n' + '-'*55

    print(current_cmd)

    buildmenu(target,menu,'Photon Scan Configuration','')