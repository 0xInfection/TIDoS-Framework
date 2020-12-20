#!/usr/bin/env python3
# -*- coding : utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This script is a part of TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


from scapy.all import *
import sys
from datetime import datetime
import time
import socket
from time import sleep
from time import strftime
from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)
from multiprocessing import Pool, TimeoutError
from core.methods.multiproc import listsplit
from core.variables import processes
from core.Core.colors import *
from core.methods.print import summary

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "XMAS Scanner."
searchinfo = "XMAS Scanner"
properties = {"INIT":["Start of port range to scan.", " "], "FIN":["End of the port range to scan.", " "], "VERBOSE":["Verbose Output? [1/0]", " "]}

def scanport(port, verbose, ip_host): # Function to scan a given port
    closed = []
    filtered = []
    open = []
    try:
        srcport = RandShort()
        conf.verb = 0
        if verbose:
            print(C+' [*] Sending FIN flagged packet to port : ' + str(port))
        xmas_scan_resp = sr1(IP(dst=ip_host)/TCP(sport = srcport, dport=port,flags="FPU"),timeout=10)
        if verbose:
            print(B+' [*] Receiving incoming packet from port : ' + str(port))
            print(B+' [*] Extracting the received packet...')
        try:

            if (str(type(xmas_scan_resp))=="<type 'NoneType'>"):
                print(''+O+' [!] Port ' + str(port)+color.TR3 +G+ ' detected Open !'+color.TR2 + C)
                open.append(port)

            elif(xmas_scan_resp.haslayer(TCP)):
                if(xmas_scan_resp.getlayer(TCP).flags == 0x14):
                    if verbose:
                        print(''+R+' [!] Port ' +O+ str(port) +R+ ' detected Closed !')
                    closed.append(port)
                    pass

            elif(xmas_scan_resp.haslayer(ICMP)):
                if(int(xmas_scan_resp.getlayer(ICMP).type)==3 and int(xmas_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                    if verbose:
                        print(''+O+' [!] Port ' + str(port)+color.TR3 +G+ ' detected Filtered !'+color.TR2 + C)
                    filter.append(port)
        except Exception:
            pass

    except KeyboardInterrupt: # In case the user needs to quit

        print(R+' [*] User requested shutdown...')
        print(" [*] Exiting...")
        quit()
    return (open, filtered, closed)

def portloop(portlist, verbose, ip_host):
    closed = []
    open = []
    filtered = []
    for port in portlist:
        res = scanport(port, verbose, ip_host)
        closed += res[2]
        filtered += res[1]
        open += res[0]
    return (open, filtered, closed)

def scan0x00(target):
    try:

        #print(R+'\n        ===================')
        #print(R+'         X M A S   S C A N ')
        #print(R+'        ===================\n')
        from core.methods.print import pscan
        pscan("xmas scan")
        print(R+'   [Reliable only in LA Networks]\n')
        if properties["INIT"][1] == " ":
            min_port = input(C+' [§] Enter initial port :> ')
        else:
            min_port = properties["INIT"][1]
        if properties["FIN"][1] == " ":
            max_port = input(C+' [§] Enter ending port :> ')
        else:
            max_port = properties["FIN"][1]
        openfil_ports = []
        filter_ports = []
        closed_ports = []
        ip_host = socket.gethostbyname(target)
        if properties["VERBOSE"][1] == " ":
            chk = input(C+' [?] Do you want a verbose output? (enter if not) :> ')
            verbose = chk != ""
        else:
            verbose = properties["VERBOSE"][1] == "1"

        try:
            print(GR+' [*] Checking port range...')
            if int(min_port) >= 0 and int(max_port) >= 0 and int(max_port) >= int(min_port) and int(max_port) <= 65536:
                print(P+' [+] Port range detected valid...'+C)
                time.sleep(0.3)
                print(GR+' [*] Preparing for the the FIN Scan...')
                pass
            else:
                print(R+"\n [!] Invalid Range of Ports")
                print(" [!] Exiting...")
                quit()
        except Exception: # If input range raises an error
            print(R+"\n [!] Invalid Range of Ports")
            print(" [!] Exiting...")
            quit()


        ports = range(int(min_port), int(max_port)+1) # Build range from given port numbers
        prtlst = listsplit(ports, round(len(ports)/processes))
        starting_time = time.time() # Start clock for scan time
        SYNACK = 0x12 # Set flag values for later reference
        RSTACK = 0x14

        def checkhost(ip): # Function to check if target is up
            conf.verb = 0 # Hide output
            try:
                ping = sr1(IP(dst = ip)/ICMP()) # Ping the target
                print("\n"+G+" [+] Target detected online!"+C+color.TR2+C)
                time.sleep(0.6)
                print(O+' [*] Beginning scan...'+C)
            except Exception: # If ping fails
                print(R+"\n [!] Couldn't Resolve Target")
                print(" [!] Exiting...")
                quit()

        checkhost(ip_host) # Run checkhost() function from earlier
        print(G+" [!] Scanning initiated at " + strftime("%H:%M:%S") + "!"+C+color.TR2+C+"\n") # Confirm scan start

        with Pool(processes=processes) as pool:
            res = [pool.apply_async(portloop, args=(l,verbose,ip_host,)) for l in prtlst]
            #res1 = pool.apply_async(portloop, )
            for i in res:
                j = i.get()
                openfil_ports += j[0]
                filter_ports += j[1]
                closed_ports += j[2]

        print(G+"\n [!] Scanning completed at %s" %(time.strftime("%I:%M:%S %p"))+C+color.TR2+C)
        ending_time = time.time()
        total_time = ending_time - starting_time
        print(P+' [*] Preparing report...\n'+C)
        time.sleep(1)
        openports = "   {}{}{}{}{}{}{}{} ports open.".format(color.TR5,C, G, str(len(openfil_ports)), color.END, color.TR2, color.END, color.CURSIVE)
        summary("xmasscan", openports)
        print()
        print(P+'    +--------+------------------+')
        print(P+'    |  '+C+'PORT  '+P+'|       '+C+'STATE      '+P+'|')
        print(P+'    +--------+------------------+')

        if openfil_ports:
            for i in sorted(openfil_ports):

                c = str(i)
                if len(c) == 1:
                    print(P+'    |   '+C+c+P+'    |       '+C+'OPEN       '+P+'|')
                    print(P+'    +--------+------------------+')
                    time.sleep(0.2)
                elif len(c) == 2:
                    print(P+'    |   '+C+c+'   '+P+'|       '+C+'OPEN       '+P+'|')
                    print(P+'    +--------+------------------+')
                    time.sleep(0.2)
                elif len(c) == 3:
                    print(P+'    |  '+C+c+'   '+P+'|       '+C+'OPEN       '+P+'|')
                    print(P+'    +--------+------------------+')
                    time.sleep(0.2)
                elif len(c) == 4:
                    print(P+'    |  '+C+c+'  '+P+'|       '+C+'OPEN       '+P+'|')
                    print(P+'    +--------+------------------+')
                    time.sleep(0.2)
                elif len(c) == 5:
                    print(P+'    | '+C+c+'  '+P+'|       '+C+'OPEN       '+P+'|')
                    print(P+'    +--------+------------------+')
                    time.sleep(0.2)
            data = "Open Ports: " + str(openfil_ports)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)

        if filter_ports:
            for i in sorted(filter_ports):
                c = str(i)
                if len(c) == 1:
                    print(P+'    |   '+C+c+P+'    |       '+C+'FILTERED   '+P+'|')
                    print(P+'    +--------+------------------+')
                    time.sleep(0.2)
                elif len(c) == 2:
                    print(P+'    |   '+C+c+'   '+P+'|       '+C+'FILTERED   '+P+'|')
                    print(P+'    +--------+------------------+')
                    time.sleep(0.2)
                elif len(c) == 3:
                    print(P+'    |  '+C+c+'   '+P+'|       '+C+'FILTERED   '+P+'|')
                    print(P+'    +--------+------------------+')
                    time.sleep(0.2)
                elif len(c) == 4:
                    print(P+'    |  '+C+c+'  '+P+'|       '+C+'FILTERED   '+P+'|')
                    print(P+'    +--------+------------------+')
                    time.sleep(0.2)
                elif len(c) == 5:
                    print(P+'    | '+C+c+'  '+P+'|       '+C+'FILTERED   '+P+'|')
                    print(P+'    +--------+------------------+')
                    time.sleep(0.2)
            print('')
            data = "Filtered Ports: " + str(filter_ports)
            save_data(database, module, lvl1, lvl2, lvl3, name, data)

        else:
            save_data(database, module, lvl1, lvl2, lvl3, name, "No open/filtered ports found.")
            print(''+R+" [-] No open/filtered ports found.!!"+R+'')
        print(B+"\n [!] " + str(len(closed_ports)) + ' closed ports not shown')
        print(G+" [+] Host %s scanned in %s seconds" %(target, total_time)+C+color.TR2+C+"\n")


    except KeyboardInterrupt: # In case the user wants to quit
        print(R+"\n [*] User Requested Shutdown...")
        print(" [*] Exiting...")
        quit()

def xmasscan(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = "xmasscan"
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
    xmasscan(web)
