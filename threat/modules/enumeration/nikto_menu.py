#!/usr/bin/env python

import subprocess
from core.colors import color

def nikto_ip(target):
    print('NIKTO IP')
    ip = input('\n[#] Enter New Target IP:> ')
    for host in target:
        host.name = ip
        host.ip = ip
    nikto_menu(target)

def nikto_port(target):
    print('NIKTO PORT')
    ports = input('\n[#] List Ports to Scan (e.g. 80,443):> ').replace(' ','')
    for host in target:
        host.port = ports
    nikto_menu(target)

def nikto_add_options(target):
    print('NIKTO OPTIONS')

    all_options = []
    options_str = ''

    options = input('\n[#] List Command Options to Add (e.g. -dbcheck,-Display+):> ').replace(' ','').split(',')

    print('OPTIONS',options)

    for option in options:
        if option.endswith('+'):
            print('OPTION', option)
            option_value = input('\n[#] Option ' + option + ' requires a value!:> ')
            all_options.append({option.strip('+'):option_value})
            options_str += option.strip('+') + ' ' + option_value + ' '
        else:
            all_options.append({option:''})
            options_str += option + ' '

    for host in target:
        host.options_list = all_options
        host.options_str = options_str

    print('ALL OPTIONS',target[0].options_list)
    nikto_menu(target)


def nikto_menu(target):
    print('NIKTO MENU')
    from core.build_menu import buildmenu

    current_cmd_str = ''
    cmd_options_str = ''

    nikto_ip = ''
    nikto_ports = ''
    nikto_options = ''

    for host in target:
        print('NIKTO MENU HOST', dict(host))
        host.help = 'Nikto'
        host.lvl2 = 'Nikto'

        nikto_ip = host.ip
        nikto_ports = host.port
        nikto_options = host.options_str

        print('NIKTO MENU HOST', dict(host))


    target_ip = nikto_ip if nikto_ip else target[0].ip
    target_ports = nikto_ports if nikto_ports else '80'
    target_options = nikto_options if nikto_options else ''

    if target_ip != '':
        current_cmd_str = 'nikto -h ' + target_ip + ' -p ' + target_ports + ' ' + nikto_options

    print('target IP', target_ip)
    print('target PORTS', target_ports)
    print('target OPTIONS', target_options)

    # if not target[0].cmd_options:
    #     pass
    # else:
    #     for key, value in target[0].cmd_options:
    #         print('OPTIONS KEY', key)
    #         print('OPTIONS VALUE', value)
    #         cmd_options_str += cmd_options_str + key.replace(' ', '')
    #     print('CMD OPTIONS STR', cmd_options_str)


    menu = { # '#' : ['module', 'description', 'function']
        '1':['Update Target IP',target_ip,'nikto_ip'],\
        '2':['Update Target Port(s)',target_ports,'nikto_port'],\
        '3':['Update Command Options',target_options,'nikto_add_options'],\
        '4':['Nikto Menu','(Web Server Vulnerability Scans Menu)','nikto_menu'],\
        '5':['Windows Enumeration','(Windows Specific Enumeration)','windows_enum'],\
    }

    current_cmd = '\n' + '-'*55 + '\n' + color.green('Current nikto Command:  \n') + color.red(current_cmd_str) + '\n' + '-'*55

    print(current_cmd)

    buildmenu(target,menu,'Nikto Scan Configuration','')          # build menu

    '''
    TODO:
        1. display current_cmd_str nicely
        2. add cmd options
        3. remove cmd options
    '''