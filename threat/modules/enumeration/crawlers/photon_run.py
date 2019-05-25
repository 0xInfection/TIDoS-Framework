#!/usr/bin/env python3

import subprocess
from os import path
import sys
sys.path.append(path.abspath('.'))
from database.database_module import save_data

import lib.Photon

# menu 4

def photon_run(target):
    # from core.build_menu import buildmenu

    print('PHOTON RUN TARGET', dict(target[0]))

    subprocess.run('ls', shell=True)

    for host in target:
        print('\nRunning Command...\n', host.cmd_str + '\n')
        # print('CURRENT PATH',sys.path)

        host.lvl3 = 'photon'
        host.option = 'Photon'
        PHOTONSCAN = host.cmd_str
        results_photon = subprocess.run(host.cmd_str, shell=True)
        # results_photon = subprocess.check_output(PHOTONSCAN, shell=True)
        # data=results_photon.decode().replace("<<","").replace(">>","")
        # save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.website, data)
    # return

    # photon(target)