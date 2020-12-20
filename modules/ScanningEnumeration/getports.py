#!/usr/bin/env python3
# -*- coding : utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This script is a part of TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
import sys
import os
import socket
import scapy
from scapy.all import *
from multiprocessing import Pool, TimeoutError
from core.methods.multiproc import listsplit
from core.variables import processes
from core.Core.colors import *
from core.methods.print import summary

info = "This module checks if common ports are open."
searchinfo = "Port Scanner"
properties = {}

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect


def check_portv(host, port, result = 1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        print(C+"\n [*] Scanning port " + str(port)+'...')
        r = sock.connect_ex((host, port))
        #print(GR+' [*] Analysing response...')
        time.sleep(0.5)
        #print(O+' [*] Adding up results together...')
        time.sleep(0.1)
        if r == 0:
            result = r

        sock.close()

    except Exception as e:
        print(''+R+' [!] Exception detected at port %s !' % port)
        pass

    return result

def portloop(portlist, host):
    open = []
    closed = []
    for p in portlist:
        sys.stdout.flush()
        response = check_portv(host, p)
        if response == 0:
            print(''+O+' [!] Port ' + str(p)+color.TR3 +G+ ' detected Open !'+color.TR2 + C)
            open.append(p)
        else:
            print(''+R+' [!] Port ' +O+ str(p) +R+ ' detected Closed !')
            closed.append(p)
    return (open, closed)

def scan0x00(host):

    #print(R+'\n   =========================')
    #print(R+'    P O R T   S C A N N E R')
    #print(R+'   =========================\n')
    from core.methods.print import pscan
    pscan("port scanner")
    print(GR+' [*] Using most common ports...')

    ports = [20,21,23,25,53,67,68,69,80,109,110,111,123,137,143,156,161,162,179,389,443,445,512,513,546,547,636,993,995,1099,2121,2049,3306, 5432,5900,6000,6667,8080,8180,8443,10000]
    mlprts = listsplit(ports, round(len(ports)/processes))
    #print(mlprts)
    print(C+' [+] Scanning %s ports...' % len(ports))
    try:
        ip = socket.gethostbyname(host)
        print(G+'\n [+] Target server detected up and running...'+C+color.TR2+C)
        print(O+' [*] Preparing for scan...'+C)
        pass
    except Exception:
        print(R+' [-] Server not responding...')
        time.sleep(0.3)
        print(R+' [*] Exiting...')
        quit()

    open_ports = []
    closed_ports = []

    print(G+" [*] Scanning started at %s" %(time.strftime("%I:%M:%S %p"))+C+color.TR2+C)
    starting_time = time.time()
    try:
        print(O+" [*] Scan in progress.."+C)
        time.sleep(0.8)
        with Pool(processes=processes) as pool:
            res = [pool.apply_async(portloop, args=(l,host,)) for l in mlprts]
            #res1 = pool.apply_async(portloop, )
            for i in res:
                j = i.get()
                open_ports += j[0]
                closed_ports += j[1]

        print(G+"\n [+] Scanning completed at %s" %(time.strftime("%I:%M:%S %p"))+C+color.TR2+C)
        ending_time = time.time()
        total_time = ending_time - starting_time
        print(P+' [*] Preparing report...\n'+C)
        time.sleep(1)

        openports = "   {}{}{}{}{}{}{}{} ports open.".format(color.TR5,C, G, str(len(open_ports)), color.END, color.TR2, color.END, color.CURSIVE)
        summary("simpleport", openports)
        print()
        print(P+'    +--------+----------+')
        print(P+'    |  '+C+'PORT'+P+'  '+'|  '+C+'STATE'+P+'   '+'|')
        print(P+'    +--------+----------+')
        lvl2 = "getports"
        module = "ScanANDEnum"
        lvl1 = "Scanning & Enumeration"
        lvl3 = ""
        if open_ports:
            for i in sorted(open_ports):
                c = str(i)
                if len(c) == 1:
                    print(P+'    |   '+C+c+P+'    |   '+C+'OPEN'+P+'   '+'|')
                    print(P+'    +--------+----------+')
                    time.sleep(0.2)
                elif len(c) == 2:
                    print(P+'    |   '+C+c+P+'   '+P+'|   '+C+'OPEN'+P+'   '+'| ')
                    print(P+'    +--------+----------+')
                    time.sleep(0.2)
                elif len(c) == 3:
                    print(P+'    |  '+C+c+P+'   '+'|   '+C+'OPEN'+P+'   '+'| ')
                    print(P+'    +--------+----------+')
                    time.sleep(0.2)
                elif len(c) == 4:
                    print(P+'    |  '+C+c+P+'  '+'|   '+C+'OPEN'+P+'   '+'| ')
                    print(P+'    +--------+----------+')
                    time.sleep(0.2)
                elif len(c) == 5:
                    print(P+'    | '+C+c+P+'  '+'|   '+C+'OPEN'+P+'   '+'| ')
                    print(P+'    +--------+----------+')
                    time.sleep(0.2)
            data = "Open Ports: " + str(open_ports)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)
        else:
            save_data(database, module, lvl1, lvl2, lvl3, name, "No open ports found.")
            print(R+"\n [-] No open ports found.!!\n")
        print(B+'\n [!] ' + str(len(closed_ports)) + ' closed ports not shown')
        print(G+" [+] Host %s scanned in %s seconds" %(host, total_time)+C+color.TR2+C+"\n")

    except KeyboardInterrupt:
        print(R+"\n [-] User requested shutdown... ")
        print(' [-] Exiting...\n')
        quit()

def getports(web):
    global name
    name = targetname(web)
    time.sleep(0.5)
    if 'http://' in web:
        web = web.replace('http://','')
    elif 'https://' in web:
        web = web.replace('https://','')
    else:
        pass
    scan0x00(web)

def attack(web):
    web = web.fullurl
    getports(web)
