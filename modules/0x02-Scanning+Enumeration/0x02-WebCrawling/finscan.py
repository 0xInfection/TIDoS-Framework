#!/usr/bin/env python
# -*- coding : utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This script is a part of TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
from scapy.all import *
import sys
from datetime import datetime
import time
import socket
from core.Core.colors import *
from time import sleep
from time import strftime
from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)

def scan0x00(target):
    try:

        print(''+R+'\n          =================')
        print(''+R + '           F I N   S C A N ')
        print(''+R + '          =================')
        print(''+R + '   [Reliable only in LA Networks]\n')
        min_port = raw_input(O+" [*] Enter Minumum Port Number -> ")
        max_port = raw_input(O+" [*] Enter Maximum Port Number -> ")
        openfil_ports = []
        filter_ports = []
        closed_ports = []
        ip_host = socket.gethostbyname(target)
        chk = raw_input(GR+' [*] Do you want a verbose output? (y/n) :> ')
        if chk == 'y':

            try:
                print(GR+' [*] Checking port range...')
                if int(min_port) >= 0 and int(max_port) >= 0 and int(max_port) >= int(min_port) and int(max_port) <= 65536:
                    print('\033[1;32m [!] Port range detected valid...\033[0m')
                    time.sleep(0.3)
                    print(GR+' [*] Preparing for the the FIN Scan...')
                    pass
                else: # If range didn't raise error, but didn't meet criteria
                    print("\n\033[91m [!] Invalid Range of Ports\033[0m")
                    print(O+" [!] Exiting...")
                    quit()
            except Exception: # If input range raises an error
                print("\n\033[91m [!] Invalid Range of Ports\033[0m")
                print(O+" [!] Exiting...")
                quit()


            ports = range(int(min_port), int(max_port)+1) # Build range from given port numbers
            starting_time = time.time() # Start clock for scan time
            SYNACK = 0x12 # Set flag values for later reference
            RSTACK = 0x14

            def checkhost(ip): # Function to check if target is up
                conf.verb = 0 # Hide output
                try:
                    ping = sr1(IP(dst = ip)/ICMP()) # Ping the target
                    print(G+"\n [+] Target server detected online...")
                    time.sleep(0.6)
                    print(GR+' [*] Beginning scan...')
                except Exception: # If ping fails
                    print(R+"\n [-] Couldn't Resolve Target")
                    print(R+" [-] Exiting...")
                    quit()

            def scanport(port): # Function to scan a given port
                try:


                    srcport = RandShort()
                    conf.verb = 0
                    print(C+' [*] Sending FIN flagged packet to port : ' + str(port))
                    fin_scan_resp = sr1(IP(dst=ip_host)/TCP(sport = srcport, dport=port,flags="F"),timeout=10)
                    print(C+' [*] Receiving incoming packet from port : ' + str(port))
                    print(B+' [*] Extracting the received packet...')
                    try:

                        if (str(type(fin_scan_resp))=="<type 'NoneType'>"):
                            print("\033[1;92m [!] Port \033[33m%s \033[1;92mdetected Open...\033[0m" % port)
                            openfil_ports.append(port)

                        elif(fin_scan_resp.haslayer(TCP)):
                            if(fin_scan_resp.getlayer(TCP).flags == RSTACK):
                                print(''+R+" [!] Port %s detected Closed..."+O+'' % port)
                                closed_ports.append(port)
                                pass

                        elif(fin_scan_resp.haslayer(ICMP)):
                            if(int(fin_scan_resp.getlayer(ICMP).type)==3 and int(fin_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                                print("\n\033[1;32m [!] Port \033[33m%s \033[1;92mdetected Filtered !\033[0m" % port)
                                filter_ports.append(port)

                    except:
                        pass

                except KeyboardInterrupt: # In case the user needs to quit

                    print('\033[91m [*] User requested shutdown...\033[0m')
                    print(O+" [*] Exiting...")
                    quit()

            checkhost(ip_host) # Run checkhost() function from earlier
            print(O+" [*] Scanning initiated at " + strftime("%H:%M:%S") + "!\n") # Confirm scan start

            for port in ports:
                scanport(port) # Feed each port into scanning function

            print("\n [!] Scanning completed at %s" %(time.strftime("%I:%M:%S %p")))
            ending_time = time.time()
            total_time = ending_time - starting_time
            print(GR+' [*] Preparing report...\n')
            time.sleep(1)
            print(O+'    +-------------+')
            print(O+'    | '+R+'SCAN REPORT '+O+'|')
            print(O+'    +-------------+')
            print(O+'    |')
            print(O+'    +--------+------------------+')
            print(O+'    |  '+GR+'PORT  '+O+'|       '+GR+'STATE      '+O+'|')
            print(O+'    +--------+------------------+')

            if openfil_ports:
                for i in sorted(openfil_ports):

                    c = str(i)
                    if len(c) == 1:
                        print(O+'    |   '+C+c+O+'    |       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 2:
                        print(O+'    |   '+C+c+'   '+O+'|       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 3:
                        print(O+'    |  '+C+c+'   '+O+'|       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 4:
                        print(O+'    |  '+C+c+'  '+O+'|       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 5:
                        print(O+'    | '+C+c+'  '+O+'|       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)

            if filter_ports:
                for i in sorted(filter_ports):
                    c = str(i)
                    if len(c) == 1:
                        print(O+'    |   '+C+c+O+'    |     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 2:
                        print(O+'    |   '+C+c+'   '+O+'|     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 3:
                        print(O+'    |  '+C+c+'   '+O+'|     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 4:
                        print(O+'    |  '+C+c+'  '+O+'|     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 5:
                        print(O+'    | '+C+c+'  '+O+'|     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)

            else:
                print(''+R+" [-] No filtered ports found.!!"+O+'')
            print(B+"\n [!] " + str(len(closed_ports)) + ' closed ports not shown')
            print(O+" [!] Host %s scanned in %s seconds\n" %(target, total_time))


        elif chk == 'n':

            try:
                if int(min_port) >= 0 and int(max_port) >= 0 and int(max_port) >= int(min_port): # Test for valid range of ports
                    pass
                else: # If range didn't raise error, but didn't meet criteria
                    print("\n\033[91m [!] Invalid Range of Ports\033[0m")
                    print(O+" [!] Exiting...")
                    quit()
            except Exception: # If input range raises an error
                print("\n\033[91m [!] Invalid Range of Ports\033[0m")
                print(O+" [!] Exiting...")
                quit()

            ports = range(int(min_port), int(max_port)+1) # Build range from given port numbers
            starting_time = time.time() # Start clock for scan time
            SYNACK = 0x12 # Set flag values for later reference
            RSTACK = 0x14

            def checkhost(ip): # Function to check if target is up
                conf.verb = 0 # Hide output
                try:
                    ping = sr1(IP(dst = ip)/ICMP()) # Ping the target
                    print("\n\033[1;92m [*] Target is Up, Beginning Scan...\033[0m")
                except Exception: # If ping fails
                    print(''+R+"\n [!] Couldn't Resolve Target"+O+'')
                    print(O+" [!] Exiting...")
                    quit()

            def scanport(port): # Function to scan a given port
                try:
                    srcport = RandShort() # Generate Port Number
                    conf.verb = 0 # Hide output
                    fin_scan_resp = sr1(IP(dst=ip_host)/TCP(sport = srcport, dport=port,flags="F"),timeout=10)
                    try:

                        if (str(type(fin_scan_resp))=="<type 'NoneType'>"):
                            openfil_ports.append(port)

                        elif(fin_scan_resp.haslayer(TCP)):
                            if(fin_scan_resp.getlayer(TCP).flags == RSTACK):
                                closed_ports.append(port)
                                pass

                        elif(fin_scan_resp.haslayer(ICMP)):
                            if(int(fin_scan_resp.getlayer(ICMP).type)==3 and int(fin_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                                filter_ports.append(port)

                    except:
                        pass
                except KeyboardInterrupt: # In case the user needs to quit
                    print("\n\033[91m [*] User Requested Shutdown...\033[0m")
                    print(O+" [*] Exiting...")
                    quit()

            checkhost(ip_host)
            print(O+" [*] Scanning Started at " + strftime("%H:%M:%S") + "!\n")
            for port in ports: # Iterate through range of ports
                scanport(port)

            print("\n [!] Scanning completed at %s" %(time.strftime("%I:%M:%S %p")))
            ending_time = time.time()
            total_time = ending_time - starting_time
            print(GR+' [*] Preparing report...\n')
            time.sleep(1)
            print(O+'    +-------------+')
            print(O+'    |    REPORT   '+O+'|')
            print(O+'    +-------------+')
            print(O+'    |')
            print(O+'    +--------+------------------+')
            print(O+'    |  '+GR+'PORT  '+O+'|       '+GR+'STATE      '+O+'|')
            print(O+'    +--------+------------------+')

            if openfil_ports:
                for i in sorted(openfil_ports):

                    c = str(i)
                    if len(c) == 1:
                        print(O+'    |   '+C+c+O+'    |       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 2:
                        print(O+'    |   '+C+c+'   '+O+'|       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 3:
                        print(O+'    |  '+C+c+'   '+O+'|       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 4:
                        print(O+'    |  '+C+c+'  '+O+'|       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 5:
                        print(O+'    | '+C+c+'  '+O+'|       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
            if filter_ports:
                for i in sorted(filter_ports):

                    c = str(i)
                    if len(c) == 1:
                        print(O+'    |   '+C+c+O+'    |     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 2:
                        print(O+'    |   '+C+c+'   '+O+'|     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 3:
                        print(O+'    |  '+C+c+'   '+O+'|     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 4:
                        print(O+'    |  '+C+c+'  '+O+'|     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 5:
                        print(O+'    | '+C+c+'  '+O+'|     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)

            else:
                print(''+R+" [-] No filtered ports found !!"+O+'')
            print(B+"\n [!] " + str(len(closed_ports)) + ' closed ports not shown')
            print(O+" [!] Host %s scanned in %s seconds\n" %(target, total_time))

        else:
            print(R+' [-] No input given...')
            print(R+' [-] Using no-verbose mode...')
            time.sleep(0.5)
            try:
                if int(min_port) >= 0 and int(max_port) >= 0 and int(max_port) >= int(min_port): # Test for valid range of ports
                    pass
                else: # If range didn't raise error, but didn't meet criteria
                    print("\n\033[91m [!] Invalid Range of Ports\033[0m")
                    print(O+" [!] Exiting...")
                    quit()
            except Exception: # If input range raises an error
                print("\n\033[91m [!] Invalid Range of Ports\033[0m")
                print(O+" [!] Exiting...")
                quit()

            ports = range(int(min_port), int(max_port)+1) # Build range from given port numbers
            starting_time = time.time() # Start clock for scan time
            SYNACK = 0x12 # Set flag values for later reference
            RSTACK = 0x14

            def checkhost(ip): # Function to check if target is up
                conf.verb = 0 # Hide output
                try:
                    ping = sr1(IP(dst = ip)/ICMP()) # Ping the target
                    print("\n\033[1;92m [*] Target is Up, Beginning Scan...\033[0m")
                except Exception: # If ping fails
                    print(''+R+"\n [!] Couldn't Resolve Target"+O+'')
                    print(O+" [!] Exiting...")
                    quit()

            def scanport(port): # Function to scan a given port
                try:
                    srcport = RandShort() # Generate Port Number
                    conf.verb = 0 # Hide output
                    fin_scan_resp = sr1(IP(dst=ip_host)/TCP(sport = srcport, dport=port,flags="F"),timeout=10)
                    try:

                        if (str(type(fin_scan_resp))=="<type 'NoneType'>"):
                            openfil_ports.append(port)

                        elif(fin_scan_resp.haslayer(TCP)):
                            if(fin_scan_resp.getlayer(TCP).flags == RSTACK):
                                closed_ports.append(port)
                                pass

                        elif(fin_scan_resp.haslayer(ICMP)):
                            if(int(fin_scan_resp.getlayer(ICMP).type)==3 and int(fin_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                                filter_ports.append(port)

                    except:
                        pass
                except KeyboardInterrupt: # In case the user needs to quit
                    print("\n\033[91m [*] User Requested Shutdown...\033[0m")
                    print(O+" [*] Exiting...")
                    quit()

            checkhost(ip_host)
            print(O+" [*] Scanning Started at " + strftime("%H:%M:%S") + "!\n")
            for port in ports: # Iterate through range of ports
                scanport(port)

            print("\n [!] Scanning completed at %s" %(time.strftime("%I:%M:%S %p")))
            ending_time = time.time()
            total_time = ending_time - starting_time
            print(GR+' [*] Preparing report...\n')
            time.sleep(1)
            print(O+'    +-------------+')
            print(O+'    |    REPORT   '+O+'|')
            print(O+'    +-------------+')
            print(O+'    |')
            print(O+'    +--------+------------------+')
            print(O+'    |  '+GR+'PORT  '+O+'|       '+GR+'STATE      '+O+'|')
            print(O+'    +--------+------------------+')

            if openfil_ports:
                for i in sorted(openfil_ports):

                    c = str(i)
                    if len(c) == 1:
                        print(O+'    |   '+C+c+O+'    |       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 2:
                        print(O+'    |   '+C+c+'   '+O+'|       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 3:
                        print(O+'    |  '+C+c+'   '+O+'|       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 4:
                        print(O+'    |  '+C+c+'  '+O+'|       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 5:
                        print(O+'    | '+C+c+'  '+O+'|       '+G+'OPEN       '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
            if filter_ports:
                for i in sorted(filter_ports):

                    c = str(i)
                    if len(c) == 1:
                        print(O+'    |   '+C+c+O+'    |     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 2:
                        print(O+'    |   '+C+c+'   '+O+'|     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 3:
                        print(O+'    |  '+C+c+'   '+O+'|     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 4:
                        print(O+'    |  '+C+c+'  '+O+'|     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)
                    elif len(c) == 5:
                        print(O+'    | '+C+c+'  '+O+'|     '+GR+'FILTERED     '+O+'|')
                        print(O+'    +--------+------------------+')
                        time.sleep(0.2)

            else:
                print(''+R+" [-] No filtered ports found !!"+O+'')
            print(B+"\n [!] " + str(len(closed_ports)) + ' closed ports not shown')
            print(O+" [!] Host %s scanned in %s seconds\n" %(target, total_time))

    except KeyboardInterrupt:
        print("\n\033[91m[*] User Requested Shutdown...\033[0m")
        print(O+" [*] Exiting...")
        quit()

def finscan(web):
    print(GR+' [*] Loading scanner...')
    time.sleep(0.5)
    if 'http://' in web:
        web = web.replace('http://','')
    elif 'https://' in web:
        web = web.replace('https://','')
    else:
        pass

    scan0x00(web)
