#!/usr/bin/env python

import subprocess


'''
TODO:
    1. Write stdout to file/db
    2. Write stderr to file/db
    print(target[0].cmd_options)
    nikto_options = {
        'cmd':'nikto',
        '-h':'10.10.10.123',
        '-p':'80'
    }
    target[0].cmd_options.append(nikto_options)
    print(target[0].cmd_options)

    As of 5/17:
        1. construct target at top level - done
        2. passing constructed target from top level - done
        3. for options, optional options first, then required in order to structre string correctly before running command
        4. still need to account for stdout/stderr write to file/db

    5/18:
        1. import multiprocess into functions.py
        2. import multiprocess into modules that need it
'''

def nikto(target):
    print('NIKTO', dict(target[0]))

    port = input('\nPort 80 or 443?')
    print('PORT', port)

    nikto_dict = {
        name: 'nikto',
        ip: target[0].ip,
        port: port,
        options: {},
        cmd_str: 'nikto '
    }

    print('NIKTO DICT', nikto_dict)

    # for key, value in dict(target[0].cmd_options).items():
    #     print('ITEMS KEY', key)
    #     print('ITEMS VALUE', value)

    #     if key == '-C all' and value == True:
    #         cmd_str += key + ' '
    #     if key == '-h' and value == True:
    #         cmd_str += key + ' ' + ip + ' '
    #     if key == '-p' and value == True:
    #         cmd_str += key + ' ' + port

    # print('CMD STR', cmd_str)

    # process = subprocess.run('nikto -h {}'.format(target[0].ip), shell=True, capture_output=True)
    # process = subprocess.run(cmd_str, shell=True)


    # process = subprocess.run(['nikto', '-h', target[0].ip, target[0].port], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    # output = process.stdout