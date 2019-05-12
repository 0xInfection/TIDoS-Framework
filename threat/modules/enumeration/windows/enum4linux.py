#!/usr/bin/env python

import subprocess

def enum4linux(target):
    target[0].ip = '10.10.10.125'       # temp value
    target[0].port = '445'              # temp value

    enum4linux_str = 'enum4linux ' + target[0].ip

    print(enum4linux_str)

    process = subprocess.run(['enum4linux', '10.10.10.125'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout

    print('PROCESS', process)
    print('OUTPUT', output)