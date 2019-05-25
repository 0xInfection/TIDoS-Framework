#!/usr/bin/env python3

import subprocess
from database.database_module import save_data

def photon_run(target):
    for host in target:
        host.option = 'Photon'
        PHOTONSCAN = host.cmd_str
        results_photon = subprocess.check_output(PHOTONSCAN, shell=True)
        data=results_photon.decode().replace("<<","").replace(">>","")
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.website, data)
    return