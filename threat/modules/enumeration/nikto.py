#!/usr/bin/env python

import subprocess

def nikto(target):
    target[0].ip = '10.10.10.123'

    process = subprocess.run('nikto -h {}'.format(target[0].ip), shell=True)

if __name__=='__main__':
    try:
        nikto(target)
    except (KeyboardInterrupt, SystemExit):
        print("\nKeyboard interrupted")
        exit()
        raise