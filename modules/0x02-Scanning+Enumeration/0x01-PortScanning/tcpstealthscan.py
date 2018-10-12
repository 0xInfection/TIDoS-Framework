#!/usr/bin/env python2
# -*- coding : utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This script is a part of TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework

from __future__ import print_function
from scapy.all import *
import sys
from datetime import datetime
import time
from time import sleep
from time import strftime
from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)
from core.Core.colors import *

def scan0x00(target):

    try:

        print(R+'\n    =================================')
        print(R+'     T C P   S T E A L T H   S C A N ')
        print(R+'    =================================\n')
        min_port = raw_input(O+" [#] Enter Minumum Port Number -> ")
        max_port = raw_input(O+" [#] Enter Maximum Port Number -> ")
        open_ports = []
        closed_ports = []
        ip_host = socket.gethostbyname(target)
        chk = raw_input(C+' [#] Do you want a verbose output? (y/n) :> ')
        if chk == 'y':

            try:
                print(GR+' [*] Checking port range...')
                if int(min_port) >= 0 and int(max_port) >= 0 and int(max_port) >= int(min_port) and int(max_port) <= 65536:
                    print('\033[1;32m [!] Port range detected valid...')
                    time.sleep(0.3)
                    print(GR+' [*] Preparing for the the Scan...')
                    pass
                else:
                    print("\n\033[91m [!] Invalid Range of Ports")
                    print(" [!] Exiting...")
                    quit()
            except Exception:
                print("\n\033[91m [!] Invalid Range of Ports")
                print(" [!] Exiting...")
                quit()

            ports = range(int(min_port), int(max_port)+1)
            starting_time = time.time()
            SYNACK = 0x12
            RSTACK = 0x14

            def checkhost(ip):
                conf.verb = 0
                try:
                    ping = sr1(IP(dst = ip)/ICMP())
                    print(''+G+"\n [!] Target server detected online...")
                    time.sleep(0.6)
                    print(O+' [*] Beginning scan...')
                except Exception:
                    print(R+"\n [-] Couldn't Resolve Target")
                    print(" [!] Exiting...")
                    quit()

            def scanport(port):
                try:
                    srcport = RandShort()
                    conf.verb = 0
                    print(GR+' [*] Sending SYN flagged packet to port : ' + str(port))
                    SYNACKpkt = sr1(IP(dst = target)/TCP(sport = srcport, dport = port, flags = "S"), timeout=5)
                    print(C+' [*] Receiving incoming packet from port : ' + str(port))
                    print(B+' [*] Extracting the received packet...')
                    try:
                        pktflags = SYNACKpkt.getlayer(TCP).flags
                        if pktflags == SYNACK:
                            print(G+' [+] Cross Reference Flag SYN-ACK detected!')
                            return True
                        else:
                            print(R+' [!] No cross reference flag detected, port possibly closed...'+R+'')
                            return False
                    except:
                        pass
                    print(O+' [!] Constructing the RST flagged packet to be sent to reset the connection...')
                    time.sleep(0.2)
                    RSTpkt = IP(dst = target)/TCP(sport = srcport, dport = port, flags = "R")
                    print(C+' [!] Sending RST packet to reset the connection...')
                    send(RSTpkt)
                except KeyboardInterrupt:
                    print(''+R+' [-] User requested shutdown...')
                    time.sleep(0.2)
                    print(O+' [*] Stopping jobs...')
                    RSTpkt = IP(dst = target)/TCP(sport = srcport, dport = port, flags = "R")
                    send(RSTpkt)
                    print(R+" [*] Exiting...")
                    quit()

            checkhost(target)
            print(O+" [*] Scanning initiated at " + strftime("%H:%M:%S") + "!\n")

            for port in ports:
                status = scanport(port)
                if status == True:
                    print(G+" [+] Port " + O + str(port) + G+" detected Open !")
                    open_ports.append(port)
                else:
                    print(''+R+' [!] Port ' + str(port) + ' Closed')
                    closed_ports.append(port)

            print(O+"\n [!] Scanning completed at %s" %(time.strftime("%I:%M:%S %p")))
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

            if open_ports:

                for i in sorted(open_ports):

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

            else:
                print(''+R+" [-] Sorry, No open ports found.!!")
            print(O+'\n [!] ' + str(len(closed_ports)) + ' closed ports not shown')
            print(C+" [!] Host %s scanned in %s seconds" %(target, total_time))


        elif chk == 'n':

            try:
                if int(min_port) >= 0 and int(max_port) >= 0 and int(max_port) >= int(min_port):
                    pass
                else:
                    print(R+"\n [-] Invalid Range of Ports")
                    print(" [*] Exiting...")
                    quit()
            except Exception:
                print(R+"\n [-] Invalid Range of Ports")
                print(" [-] Exiting...")
                quit()

            ports = range(int(min_port), int(max_port)+1)
            starting_time = time.time()
            SYNACK = 0x12
            RSTACK = 0x14

            def checkhost(ip):
                conf.verb = 0
                try:
                    ping = sr1(IP(dst = ip)/ICMP())
                    print(''+G+"\n [*] Target is Up, Beginning Scan...")
                except Exception:
                    print(''+R+"\n [!] Couldn't Resolve Target")
                    print(" [!] Exiting...")
                    quit()

            def scanport(port):
                try:
                    srcport = RandShort()
                    conf.verb = 0
                    SYNACKpkt = sr1(IP(dst = target)/TCP(sport = srcport, dport = port, flags = "S"), timeout=5)
                    try:
                        pktflags = SYNACKpkt.getlayer(TCP).flags
                        if pktflags == SYNACK:
                            return True
                        else:
                            return False
                    except:
                        pass
                    RSTpkt = IP(dst = target)/TCP(sport = srcport, dport = port, flags = "R")
                    send(RSTpkt)
                except KeyboardInterrupt:
                    print(''+R+"\n [-] User Requested Shutdown...")
                    print(O+' [*] Stopping jobs...')
                    RSTpkt = IP(dst = target)/TCP(sport = srcport, dport = port, flags = "R")
                    send(RSTpkt)
                    print(R+" [*] Exiting...")
                    quit()

            checkhost(target)
            print(" [*] Scanning Started at " + strftime("%H:%M:%S") + "!\n")
            for port in ports:

                status = scanport(port)
                if status == True:
                    open_ports.append(port)
                else:
                    closed_ports.append(port)

            print(O+"\n [!] Scanning completed at %s" %(time.strftime("%I:%M:%S %p")))
            ending_time = time.time()
            total_time = ending_time - starting_time
            print(GR+' [*] Preparing report...\n')
            time.sleep(1)
            print(O+'    +-------------+')
            print(O+'    |    '+R+'REPORT   '+O+'|')
            print(O+'    +-------------+')
            print(O+'    |')
            print(O+'    +--------+------------------+')
            print(O+'    |  '+GR+'PORT  '+O+'|       '+GR+'STATE      '+O+'|')
            print(O+'    +--------+------------------+')

            if open_ports:
                for i in sorted(open_ports):

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
            else:
                print(''+R+' [-] No open ports found!')

            print(O+'\n [!] ' + str(len(closed_ports)) + ' closed ports not shown')
            print(C+" [!] Host %s scanned in %s seconds\n" %(target, total_time))


    except KeyboardInterrupt:
        print(R+"\n [-] User Requested Shutdown...")
        print(" [*] Exiting...")
        quit()

def tcpstealthscan(web):

    print(GR+' [*] Loading scanner...')
    time.sleep(0.5)
    if 'http://' in web:
        web = web.replace('http://','')
    elif 'https://' in web:
        web = web.replace('https://','')
    else:
        pass
    scan0x00(web)
