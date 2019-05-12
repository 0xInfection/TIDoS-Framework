#!/usr/bin/env python

import subprocess

def nikto(target):
    target[0].ip = '10.10.10.123'       # temp value
    target[0].port = '80'               # temp value

    nikto_str = 'nikto -h ' + target[0].ip + ' -p ' + target[0].port

    print(nikto_str)

    process = subprocess.run(['nikto', '-h', target[0].ip, target[0].port], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout