#!/usr/bin/env python

import subprocess
from core.colors import color

def nikto_ip(target):
    ip = input('\n[#] Enter New Target IP:> ')
    for host in target:
        host.name = ip
        host.ip = ip
    return nikto_menu(target)

def nikto_port(target):
    ports = input('\n[#] List Ports to Scan (e.g. 80,443):> ').replace(' ','')
    for host in target:
        host.port = ports
    return nikto_menu(target)

def nikto_add_options(target):
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

    return nikto_menu(target)


def nikto_menu(target):
    from core.build_menu import buildmenu

    nikto_ip = ''
    nikto_ports = target[0].port or ''
    nikto_options = ''

    target_ip = nikto_ip if nikto_ip else target[0].ip
    target_ports = nikto_ports if nikto_ports else target[0].port
    target_options = nikto_options if nikto_options else target[0].options_str

    current_cmd_str = 'nikto -h ' + target_ip + ' -p ' + target_ports + ' ' + target_options

    for host in target:
        host.help = 'nikto'
        host.lvl2 = 'Nikto'

        if host.port == '':
            host.port = '80'

        nikto_ip = host.ip
        nikto_ports = host.port
        nikto_options = host.options_str
        host.cmd_str = current_cmd_str

    menu = { # '#' : ['module', 'description', 'function']
        '1':['Update Target IP',target_ip,'nikto_ip'],\
        '2':['Update Target Port(s)',target_ports,'nikto_port'],\
        '3':['Update Command Options',target_options,'nikto_add_options'],\
        '4':['Run Nikto','(Run Current Nikto Command)','nikto'],\
    }

    current_cmd = '\n' + '-'*55 + '\n' + color.green('Current nikto Command:  \n') + color.red(current_cmd_str) + '\n' + '-'*55

    print(current_cmd)

    buildmenu(target,menu,'Nikto Scan Configuration','')