#!/usr/bin/env python

import subprocess
from database.database_module import save_data

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

    import subprocess
    from database.database_module import save_data

    def dig(target):
        for host in target:
            host.lvl2='dig'
            host.lvl3=''
            DIGSCAN = "dig "+host.name
            results_dig = subprocess.check_output(DIGSCAN, shell=True)
            data=results_dig.decode().replace("<<","").replace(">>","")
            save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
        return
'''

def nikto(target):
    from core.build_menu import buildmenu
    print('NIKTO', dict(target[0]))

    for host in target:
        host.lvl2 = 'nikto'
        host.lvl3 = ''
        NIKTOSCAN = 'nikto -h ' + host.ip + ' -p ' + host.port
        print('NIKTOSCAN', NIKTOSCAN)
        # results_nikto = subprocess.run(NIKTOSCAN, shell=True)
        return NIKTOSCAN
    buildmenu(target,target[0].main_menu,'Main Menu','')


    # process = subprocess.run('nikto -h {}'.format(target[0].ip), shell=True, capture_output=True)
    # process = subprocess.run(cmd_str, shell=True)


    # process = subprocess.run(['nikto', '-h', target[0].ip, target[0].port], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    # output = process.stdout