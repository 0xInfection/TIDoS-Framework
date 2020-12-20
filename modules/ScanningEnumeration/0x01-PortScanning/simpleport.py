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

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "A simple port scanner."
searchinfo = "Simple Port Scanner"
properties = {"INIT":["Start of port range to scan.", " "], "FIN":["End of the port range to scan.", " "], "VERBOSE":["Verbose Output? [1/0]", " "]}

def portloop(portlist, host, verbose):
    open = []
    closed = []
    for p in portlist:
        if verbose:
            response = check_portv(host, p)
        else:
            response = check_port(host, p)
        if response == 0:
            print(''+O+' [!] Port ' + str(p)+color.TR3 +G+ ' detected Open !'+color.TR2 + C)
            open.append(p)
        else:
            if verbose:
                print(''+R+' [!] Port ' +O+ str(p) +R+ ' detected Closed !')
            closed.append(p)
    return (open, closed)

def check_portv(host, port, result = 1):

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        print(C+"\n [*] Connecting to '%s' via port %s" % (host, port))
        r = sock.connect_ex((host, port))
        #print(GR+' [*] Analysing results...')
        time.sleep(0.0015)

        if r == 0:
            result = r

        sock.close()

    except Exception as e:
        print(''+R+' [!] Exception detected at port %s !' % port)
        pass

    return result

def check_port(host, port, result = 1):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        r = sock.connect_ex((host, port))
        if r == 0:
            result = r
        sock.close()
    except Exception:
        pass

    return result

def scan0x00(host):

    #print(R+'\n   =======================================')
    #print(R + "    S I M P L E   P O R T   S C A N N E R")
    #print(R + '   =======================================\n')
    from core.methods.print import pscan
    pscan("simple port scanner")
    if properties["INIT"][1] == " ":
        start_port = input(C+' [§] Enter initial port :> ')
    else:
        start_port = properties["INIT"][1]
    if properties["FIN"][1] == " ":
        end_port = input(C+' [§] Enter ending port :> ')
    else:
        end_port = properties["FIN"][1]

    start_port = int(start_port)
    end_port = int(end_port)

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

    if properties["VERBOSE"][1] == " ":
        mn = input(C+'\n [?] Do you want a verbose output (enter if not) :> ')
        verbose = mn != ""
    else:
        verbose = properties["VERBOSE"][1] == "1"
    if verbose:
        print(''+P+'\n [+] Verbose mode selected !\n')
        print(GR+" [!] Scanning %s from port %s - %s: " % (host, start_port, end_port))
    print(G+" [*] Scanning started at %s" %(time.strftime("%I:%M:%S %p"))+C+color.TR2+C)
    starting_time = time.time()
    try:
        if verbose:
            print(O+" [*] Scan in progress.."+C)
            time.sleep(0.8)
        portrange = range(start_port, end_port+1)
        prtlst = listsplit(portrange, round(len(portrange)/processes))
        with Pool(processes=processes) as pool:
            res = [pool.apply_async(portloop, args=(l,host,verbose,)) for l in prtlst]
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
        #print(O+' ---+-------------+')
        #print(O+'    [ SCAN REPORT ]    simplescan')
        #print(O+'    +-------------+   -------------')
        #print(O+'             ')
        #print()
        openports = "   {}{}{}{}{}{}{}{} ports open.".format(color.TR5,C, G, str(len(open_ports)), color.END, color.TR2, color.END, color.CURSIVE)
        summary("simpleport", openports)
        print()
        print(P+'    +--------+----------+')
        print(P+'    |  '+C+'PORT'+P+'  '+'|  '+C+'STATE'+P+'   '+'|')
        print(P+'    +--------+----------+')

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
            print(R+"\n [-] No open ports found.!!\n")
            save_data(database, module, lvl1, lvl2, lvl3, name, "No open ports found.")
        print(B+'\n [!] ' + str(len(closed_ports)) + ' closed ports not shown')
        print(G+" [+] Host %s scanned in %s seconds" %(host, total_time)+C+color.TR2+C+"\n")

    except KeyboardInterrupt:
        print(R+"\n [-] User requested shutdown... ")
        print(' [-] Exiting...\n')
        quit()

def simpleport(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = "simpleport"
    global module
    module = "ScanANDEnum"
    global lvl1
    lvl1 = "Port Scanning"
    global lvl3
    lvl3 = ""
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
    simpleport(web)
