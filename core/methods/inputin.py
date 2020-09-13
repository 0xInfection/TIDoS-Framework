#!/usr/bin/env python3
# coding: utf-8

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework



import os
import socket
import time
import string

import core.variables as vars
from core.Core.colors import *
from core.methods.threat import Target


def inputin(target):
    valid_ip_regex = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    valid_host_regex = r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$'
    
    try:
        web = target
        if not str(web).startswith('http'):
            mo = input(GR + ' [?] Does this website use SSL? (y/n) :> ')
            if mo == 'y' or mo == 'Y':
                web = 'https://' + web
            elif mo == 'n':
                web = 'http://' + web
                
        if 'http://' in web:
            po = web.split('://')[1]
            port = 80
        elif 'https://' in web:
            po = web.split('://')[1]
            port = 443
        else:
            po = ''
            port = 1337
        #if str(web).endswith('/'):
        wspl = web.split("://")
        if "/" in wspl[1]:
            wspl[1] = wspl[1].split("/")[0]
            web = wspl[0] + "://" + wspl[1]
            if po != "":
                po = wspl[1]
        custport = input(" [?] Does the site use a custom port? (enter if not) :> ")
        if custport != "":
            inport = input(" [§] Enter port :> ")
            try:
                port = int(inport)
                assert port in range(1, 65535)
            except:
                print(R+" [!] Not a valid port value"+C)
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
            if port not in [80, 443]:
                webfin = webfin + ":" + str(port)
            #vars.targets.append(webfin)
            newTarget = Target(po, ip)
            newTarget.port = port
            newTarget.urluser = user
            newTarget.urlpasswd = passwd
            newTarget.fullurl = webfin
            vars.targets.append(newTarget)
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

    newTarget = Target(target, target)
    newTarget.fullurl = target

    if net:
        vars.targets.append(newTarget)
        print(O+" [+] Target added:"+C+color.TR3+C+G+target+C+color.TR2+C)
    elif os.system("ping -c 1 -q -W 5 " + target + " > /dev/null") == 0:
        vars.targets.append(newTarget)
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
