#!/usr/bin/env python

import subprocess
from database.database_module import save_data

def nmap(target):
    for host in target:
        host.lvl2 = 'nmap'
        host.lvl3 = ''
        host.option = 'NMAP'
        NMAP_STRING = host.nmap
        results_nmap = subprocess.check_output(NMAP_STRING, shell=True)
        # data=results_nmap.decode().replace("<<","").replace(">>","")
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, results_nmap)
    # buildmenu(target,target[0].main_menu,'Main Menu','')
 