#!/usr/bin/env python

import subprocess
from database.database_module import save_data

def nikto(target):
    # from core.build_menu import buildmenu

    # print('NIKTO')

    for host in target:
        # print('NIKTO HOST', dict(host))
        # print('NIKTO HOST CMD', host.cmd_str)
        host.lvl2 = 'nikto'
        host.lvl3 = ''
        host.option = 'Nikto'
        NIKTOSCAN = host.cmd_str
        # print('NIKTOSCAN', host.cmd_str)
        # results_nikto = subprocess.run(NIKTOSCAN, shell=True)
        results_nikto = subprocess.check_output(NIKTOSCAN, shell=True)
        data=results_nikto.decode().replace("<<","").replace(">>","")
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
    # buildmenu(target,target[0].main_menu,'Main Menu','')
