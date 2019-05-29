#!/usr/bin/env python3

from core.colors import color

options_with_val = ['-l','--level','-t','--threads','-d','--delay','--timeout','-c','--cookies','-o','--output','--exclude','--seeds','--user-agent','-r','--regex','e','--export','--stdout']

def photon_website(target):
    website = input('\n[#] Enter New Target Website:> ')
    for host in target:
        host.name = website
        host.website = website
    return photon_menu(target)

def photon_options(target):
    all_options = []
    options_str = ''

    options = input('\n[#] List Command Options to Add (e.g. -t,--level):> ').replace(' ','').split(',')

    for option in options:
        if option in str(options_with_val):
            option_value = input('\n[#] Option ' + option + ' requires a value!:> ')
            all_options.append({option:option_value})
            options_str += option + ' ' + option_value + ' '
        else:
            all_options.append({option:''})
            options_str += option + ' '

    for host in target:
        host.options_list = all_options
        host.options_str = options_str

    return photon_menu(target)

def photon_menu(target):
    from core.build_menu import buildmenu

    photon_site = target[0].ip if not target[0].website else target[0].website
    photon_options = ''

    target_website = photon_site if photon_site else target[0].website
    if 'https://' not in target_website:
        target_website = 'https://' + target_website

    target_options = photon_options if photon_options else target[0].options_str
    target_run_file = target[0].run_file

    display_cmd_str = 'photon -u ' + target_website + ' ' + target_options
    current_cmd_str = 'python3 ' + target_run_file + ' -u ' + target_website + ' ' + target_options

    for host in target:
        # host.module = 'ScanANDEnum'
        # host.lvl1 = 'Scanning & Enumeration'
        host.help = 'python3 lib/Photon/photon.py'
        host.lvl2 = 'Crawler'
        host.lvl3 = 'Photon'
        host.run_file = './lib/Photon/photon.py'

        photon_site = host.website
        photon_options = host.options_str
        host.cmd_str = current_cmd_str

    menu = { # '#' : ['module', 'description', 'function']
        '1':['Update Target Website',target_website,'photon_website'],\
        '2':['Update Command Options',target_options,'photon_options'],\
        '3':['Run Photon','(Run Current Crawler Command)','photon_run'],\
    }

    display_cmd = '\n' + '-'*55 + '\n' + color.green('Current Photon Command:  \n') + color.red(display_cmd_str) + '\n' + '-'*55

    print(display_cmd)

    buildmenu(target,menu,'Photon Scan Configuration','')