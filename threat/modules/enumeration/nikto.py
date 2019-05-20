#!/usr/bin/env python

import subprocess
from database.database_module import save_data

def nikto(target):
    print('NIKTO')
    port = input('\nPort 80?')

    for host in target:
        print('HOST', dict(host))
        host.port = '80'
        # host.lvl1 = 'Scanning & Enumeration'
        host.lvl2 = 'nikto'
        host.lvl3 = ''
        host.option = 'Nikto'
        print('HOST', dict(host))
        NIKTOSCAN = 'nikto -h ' + host.ip + ' -p ' + host.port
        # results_nikto = subprocess.run(NIKTOSCAN, shell=True)
        results_nikto = subprocess.check_output(NIKTOSCAN, shell=True)
        data=results_nikto.decode().replace("<<","").replace(">>","")
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
    return
