#!/usr/bin/env python3
# coding: utf-8

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/VainlyStrain/TIDoS



import os
import socket
import time
import string

import core.variables as vars
from core.Core.colors import *


def inputin(target):
    try:
        web = target
        if not str(web).startswith('http'):
            mo = input(GR + ' [?] Does this website use SSL? (y/n) :> ')
            if mo == 'y' or mo == 'Y':
                web = 'https://' + web
            elif mo == 'n':
                web = 'http://' + web
        if 'http://' in web:
            po = web.split('//')[1]
        elif 'https://' in web:
            po = web.split('//')[1]
        else:
            po = ''
        if str(web).endswith('/'):
            web = po[:-1]
            po = po[:-1]
        print(GR + ' [*] Checking server status...')
        time.sleep(0.6)

        try:
            ip = socket.gethostbyname(po)
            print(G + ' [+] Site seems to be up...'+C+color.TR2+C)
            time.sleep(0.5)
            print(O + ' [+] IP Detected :' + C+color.TR3+C+G + ip+C+color.TR2+C)
            time.sleep(0.5)
            print('')
            os.system('cd tmp/logs/ && rm -rf ' + po + '-logs && mkdir ' + po + '-logs/')
            user = input(" [?] Enter username (leave blank if none): ")
            passwd = input(" [?] Enter password (leave blank if none): ")
            webfin = web
            if user != "" and passwd != "":
                wl = web.split("://")
                webfin = wl[0] + "://" + user + ":" + passwd + "@" + wl[1]
            vars.targets.append(webfin)
            print(O+" [+] Target added:"+C+color.TR3+C+G+webfin+C+color.TR2+C)

        except socket.gaierror:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Target seems down...")
            pass

    except KeyboardInterrupt:
        pass

def inputip(target, net=False):
    v4 = target.split(".")
    v6 = target.split(":")
    try:
        if len(v4) == 4 and (i.isdigit() for i in v4):
            if (int(i) in range(0,256) for i in v4):
                if not net:
                    print(" [+] IPv4 detected!")
        elif len(v6) == 8 and (len(i) in range(0,5) for i in v6):
            if (int(i) for i in v6):
                if not net:
                    print(" [+] IPv6 detected!")
        else:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Invalid IP: {}".format(target))
    except ValueError:
        print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Invalid IP: {}".format(target))
        pass

    if net:
        vars.targets.append(target)
        print(O+" [+] Target added:"+C+color.TR3+C+G+target+C+color.TR2+C)
    elif os.system("ping -c 1 " + target) is 0:
        vars.targets.append(target)
        print(O+" [+] Target added:"+C+color.TR3+C+G+target+C+color.TR2+C)
    else:
        print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Target seems down...")

def inputnet(target):
    net = target.split("/")
    if len(net) != 2:
        print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Syntax: NRange/NMask")
    else:
        range = net[0]
        mask = net[1]
        try:
            import modules.ScanningEnumeration.arpscan as sca
            sca.properties["IP"][1] = range
            sca.properties["NMASK"][1] = mask
            targets = sca.attack("")
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('google.com', 0))
            attackerip = s.getsockname()[0].strip()
            for targetip in targets:
                if targetip != attackerip:
                    inputip(targetip, net=True)
                    #print("'{}','{}'".format(targetip, attackerip))
        except Exception as e:
            print(e)