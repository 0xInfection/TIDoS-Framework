#!/usr/bin/env python

import subprocess
from database.database_module import save_data

def nikto(target):
    for host in target:
        host.help = 'Nikto'
        host.lvl2 = 'Nikto'
        host.lvl3 = ''
        host.option = 'Nikto'
        NIKTOSCAN = host.cmd_str
        results_nikto = subprocess.check_output(NIKTOSCAN, shell=True)
        data=results_nikto.decode().replace("<<","").replace(">>","")
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
    return