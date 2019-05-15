#!/usr/bin/env python

import subprocess

def enum4linux(target):
    target[0].ip = '10.10.10.125'       # temp value
    target[0].port = '445'              # temp value

    process = subprocess.run(['enum4linux {}'.format(target[0].ip)], shell=True)

if __name__=='__main__':
    try:
        enum4linux(target)
    except (KeyboardInterrupt, SystemExit):
        print("\nKeyboard interrupted")
        exit()
        raise