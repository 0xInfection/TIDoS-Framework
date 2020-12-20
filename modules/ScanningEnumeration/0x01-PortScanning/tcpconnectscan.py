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

info = "TCP Connect Scanner."
searchinfo = "TCP Connect Scanner"
properties = {"INIT":["Start of port range to scan.", " "], "FIN":["End of the port range to scan.", " "], "VERBOSE":["Verbose Output? [1/0]", " "]}


def checkhost(ip): # Function to check if target is up
    conf.verb = 0 # Hide output
    try:
        ping = sr1(IP(dst = ip)/ICMP()) # Ping the target
        print("\n"+G+" [+] Target server detected online..."+C+color.TR2+C)
        time.sleep(0.6)
        print(O+' [*] Beginning scan...'+C)
    except Exception: # If ping fails
        print("\n"+R+" [!] Couldn't Resolve Target")
        print(" [!] Exiting...")
        quit()

def portloop(portlist, verbose, ip_host): # Function to scan a given port
    closed = []
    open = []
    try:
        for port in portlist:
            srcport = RandShort()
            conf.verb = 0
            if verbose:
                print(C+' [*] Sending SYN flagged packet to port : ' + str(port))
                print(GR+' [*] Trying handshake...')
            tcp_connect_scan_resp = sr1(IP(dst=ip_host)/TCP(sport = srcport, dport=port,flags="S"),timeout=5)
            if verbose:
                print(GR+' [*] Receiving incoming packet from port : ' + str(port))
                print(B+' [*] Extracting the received packet...')
            try:

                if(str(type(tcp_connect_scan_resp))=="<type 'NoneType'>"):
                    closed.append(port)
                    if verbose:
                        print(''+R+' [!] Port ' +O+ str(port) +R+ ' detected Closed !')

                elif(tcp_connect_scan_resp.haslayer(TCP)):

                    if(tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):
                        print(''+O+' [!] Port ' + str(port)+color.TR3 +G+ ' detected Open !'+color.TR2 + C)
                        open.append(port)
                        if verbose:
                            print(P+' [*] Sending back a ACK flag to confirm the connection...'+C)
                        send_rst = sr(IP(dst=ip_host)/TCP(sport=srcport, dport=port, flags="AR"),timeout=5)

                    elif (tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):
                        closed.append(port)
                        if verbose:
                            print(''+R+' [!] Port ' +O+ str(port) +R+ ' detected Closed !')
            except Exception:
                pass
        
    except KeyboardInterrupt: # In case the user needs to quit
        print(R+' [*] User requested shutdown...')
        print(" [*] Exiting...")
        quit()
    return (open, closed)


def scan0x00(target):

    try:

        #print(R+'\n    =================================')
        #print(R+'     T C P   C O N N E C T   S C A N ')
        #print(R+'    =================================\n')
        from core.methods.print import pscan
        pscan("tcp connect scan")
        if properties["INIT"][1] == " ":
            min_port = input(C+' [§] Enter initial port :> ')
        else:
            min_port = properties["INIT"][1]
        if properties["FIN"][1] == " ":
            max_port = input(C+' [§] Enter ending port :> ')
        else:
            max_port = properties["FIN"][1]
        open_ports = []
        closed_ports = []
        ip_host = socket.gethostbyname(target)
        if properties["VERBOSE"][1] == " ":
            chk = input(C+' [?] Do you want a verbose output? (enter if not) :> ')
            verbose = chk != ""
        else:
            verbose = properties["VERBOSE"][1] == "1"
        print(GR+' [*] Checking port range...')
        if int(min_port) >= 0 and int(max_port) >= 0 and int(max_port) >= int(min_port) and int(max_port) <= 65536:
            print(P+' [!] Port range detected valid...'+C)
            time.sleep(0.3)
            print(GR+' [*] Preparing for the scan...')

            ports = range(int(min_port), int(max_port)+1) # Build range from given port numbers
            prtlst = listsplit(ports, round(len(ports)/processes))
            starting_time = time.time() # Start clock for scan time
            SYNACK = 0x12 # Set flag values for later reference
            RSTACK = 0x14

            checkhost(ip_host) # Run checkhost() function from earlier
            print(G+" [!] Scanning initiated at " + strftime("%H:%M:%S") + "!"+C+color.TR2+C+"\n") # Confirm scan start

            with Pool(processes=processes) as pool:
                res = [pool.apply_async(portloop, args=(l,verbose,ip_host,)) for l in prtlst]
                #res1 = pool.apply_async(portloop, )
                for i in res:
                    j = i.get()
                    open_ports += j[0]
                    closed_ports += j[1]

            print(G+"\n [!] Scanning completed at %s" %(time.strftime("%I:%M:%S %p"))+C+color.TR2+C)
            ending_time = time.time()
            total_time = ending_time - starting_time
            print(P+' [*] Preparing report...\n'+C)
            time.sleep(1)
            openports = "   {}{}{}{}{}{}{}{} ports open.".format(color.TR5,C, G, str(len(open_ports)), color.END, color.TR2, color.END, color.CURSIVE)
            summary("tcp connect", openports)
            print()
            print(P+'    +--------+------------------+')
            print(P+'    |  '+GR+'PORT  '+P+'|       '+C+'STATE      '+P+'|')
            print(P+'    +--------+------------------+')

            if open_ports:
                for i in sorted(open_ports):

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
                print('')
                data = "Open Ports: " + str(open_ports)
                save_data(database, module, lvl1, lvl2, lvl3, name, data)
            else:
                save_data(database, module, lvl1, lvl2, lvl3, name, "No open ports found.")
                print(R+' [-] No open ports found!')

            print(B+' [!] '+ str(len(closed_ports)) + ' closed ports not shown')
            print(G+" [+] Host %s scanned in %s seconds" %(target, total_time)+C+color.TR2+C+"\n")

        else: # If range didn't raise error, but didn't meet criteria
            print(R+"\n [!] Invalid Range of Ports")
            print(" [!] Exiting...")
            quit()
    except Exception as e: # If input range raises an error
        print(e)
        quit()

def tcpconnectscan(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = "tcpconnectscan"
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
    tcpconnectscan(web)
