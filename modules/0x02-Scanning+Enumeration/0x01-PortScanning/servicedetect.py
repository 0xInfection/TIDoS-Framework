#!/usr/bin/env python2
# -*- coding : utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This script is a part of TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework

from __future__ import print_function
import time
import sys
import os
import socket
import scapy
from scapy.all import *
from core.Core.colors import *

def service0x00(host):

    print(R+'\n   ===================================')
    print(R + "    S E R V I C E   D E T E C T I O N")
    print(R + '   ===================================\n')
    start_port = raw_input(O+' [#] Enter initial port :> ')
    end_port = raw_input(O+' [#] Enter ending port :> ')

    start_port = int(start_port)
    end_port = int(end_port)

    try:
        ip = socket.gethostbyname(host)
        print(G+'\n [+] Target server detected up and running...')
        print(GR+' [*] Preparing for scan...')
        pass
    except:
        print(R+' [-] Server not responding...')
        time.sleep(0.3)
        print(R+' [*] Exiting...')
        quit()

    open_ports = []
    closed_ports = []

    # feel free to add your own :)
    common_ports = {
    '20': 'FTP',
    '21': 'FTP',
    '22': 'SSH',
    '23': 'TELNET',
    '25': 'SMTP',
    '53': 'DNS',
    '67': 'DHCP',
    '68': 'DHCP',
    '69': 'TFTP',
    '80': 'HTTP',
    '109': 'POP2',
    '110': 'POP3',
    '111': 'RPCBIND',
    '123': 'NTP',
    '137': 'NETBIOS-NS',
    '138': 'NETBIOS-DGM',
    '139': 'NETBIOS-SSN',
    '143': 'IMAP',
    '156': 'SQL-SERVER',
    '161': 'SNMP',
    '162': 'SNMP II',
    '179': 'BGP',
    '389': 'LDAP',
    '443': 'HTTPS',
    '445': 'NETBIOS-SSN',
    '512': 'EXEC',
    '513': 'LOGIN',
    '546': 'DHCP-CLIENT',
    '547': 'DHCP-SERVER',
    '636': 'LDAPS',
    '995': 'POP3-SSL',
    '993': 'IMAP-SSL',
    '1099': 'RMI-REGISTRY',
    '2121': 'FTP',
    '2049': 'NFS',
    '2086': 'WHM/CPANEL',
    '2087': 'WHM/CPANEL',
    '2082': 'CPANEL',
    '2083': 'CPANEL',
    '3306': 'MYSQL',
    '3632': 'DISTCC',
    '5061': 'SIP-TLS',
    '5432': 'POSTGRESQL',
    '5900': 'VNC',
    '6000': 'X11',
    '6667': 'IRC',
    '8009': 'AJP13',
    '8080': 'HTTP PROXY',
    '8180': 'HTTP',
    '8443': 'PLESK',
    '10000': 'VIRTUALMIN/WEBMIN'
    }

    def get_servicev(port):
        port = str(port)
        if port in common_ports:
            return common_ports[port]
        else:
            return 0

    def check_portv(host, port, result = 1):

        try:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            print(C+"\n [*] Connecting to '%s' via port %s" % (host, port))
            r = sock.connect_ex((host, port))
            print(GR+' [*] Analysing results...')
            time.sleep(0.05)
            print(O+' [*] Adding up results together...')
            time.sleep(0.1)

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
        except Exception as e:
            pass

        return result

    def get_service(port):
        port = str(port)
        if port in common_ports:
            return common_ports[port]
        else:
            return 0

    mn = raw_input(O+'\n [*] Do you want a verbose output (y/n) :> ')
    if mn == 'y':

        print(''+G+'\n [+] Verbose mode selected !\n')
        print(GR+" [!] Scanning %s from port %s - %s: " % (host, start_port, end_port))
        print(B+" [*] Scanning started at %s" %(time.strftime("%I:%M:%S %p")))
        starting_time = time.time()
        try:
            print(O+" [*] Scan in progress..")
            time.sleep(0.8)
            for p in range(start_port, end_port+1):
                sys.stdout.flush()
                print(p, end=' ')
                response = check_portv(host, p)
                if response == 0:
                    print(''+G+' [!] Port ' +O+ str(p) +G+ ' detected Open !')
                    open_ports.append(p)
                else:
                    print(''+R+' [!] Port ' +O+ str(p) +R+ ' detected Closed !')
                    closed_ports.append(p)
                if not p == end_port:
                    sys.stdout.write('\b' * len(str(p)))

            print(G+"\n [+] Scanning completed at %s" %(time.strftime("%I:%M:%S %p")))
            ending_time = time.time()
            total_time = ending_time - starting_time
            print(G+' [*] Preparing report...\n')
            time.sleep(1)
            print(O+'    +-------------+')
            print(O+'    | '+R+'SCAN REPORT '+O+'|')
            print(O+'    +-------------+')
            print(O+'    |')
            print(O+'    +--------+----------+-----------+')
            print(O+'    |  '+GR+'PORT  '+O+'|  '+GR+'STATE   '+O+'|  '+GR+'SERVICE  '+O+'|')
            print(O+'    +--------+----------+-----------+')

            if open_ports:
                for i in sorted(open_ports):
                    service = get_servicev(i)
                    if not service:
                        service = "Unknown"
                    m = str(service)
                    c = str(i)
                    if len(c) == 1:
                        print(O+'    |   '+C+c+O+'    |   '+G+'OPEN   '+O+'|  '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
                        time.sleep(0.2)
                    elif len(c) == 2:
                        print(O+'    |   '+C+c+'   '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
                        time.sleep(0.2)
                    elif len(c) == 3:
                        print(O+'    |  '+C+c+'   '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
                        time.sleep(0.2)
                    elif len(c) == 4:
                        print(O+'    |  '+C+c+'  '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
                        time.sleep(0.2)
                    elif len(c) == 5:
                        print(O+'    | '+C+c+'  '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
                        time.sleep(0.2)
            else:
                print(R+"\n [-] No open ports found.!!\n")
            print(B+'\n [!] ' + str(len(closed_ports)) + ' closed ports not shown')
            print(G+" [+] Host %s scanned in %s seconds\n" %(host, total_time))

        except KeyboardInterrupt:
            print(R+"\n [-] User requested shutdown... ")
            print(' [-] Exiting...\n')
            quit()

    elif mn == 'n':

        print(O+'\n [!] No verbose mode selected !\n')
        print(GR+" [!] Scanning %s from port %s - %s: " % (host, start_port, end_port))
        print(B+" [*] Scanning started at %s" %(time.strftime("%I:%M:%S %p")))
        starting_time = time.time()

        try:
            print(O+" [*] Scan in progress..")
            print(C+" [*] Trying connections to Port:"+B+" ", end=' ')

            for p in range(start_port, end_port+1):
                sys.stdout.flush()
                print(p, end=' ')
                response = check_port(host, p)
                if response == 0:
                    open_ports.append(p)
                if not p == end_port:
                    sys.stdout.write('\b' * len(str(p)))

            print(G+"\n [+] Scanning completed at %s" %(time.strftime("%I:%M:%S %p")))
            ending_time = time.time()
            total_time = ending_time - starting_time
            print(GR+' [*] Preparing report...')
            time.sleep(0.4)
            print('\n')
            print(O+'    +-------------+')
            print(O+'    | SCAN REPORT '+O+'|')
            print(O+'    +-------------+')
            print(O+'    |')
            print(O+'    +--------+----------+-----------+')
            print(O+'    |  PORT  '+O+'|  STATE   '+O+'|  SERVICE  '+O+'|')
            print(O+'    +--------+----------+-----------+')

            if open_ports:
                for i in sorted(open_ports):
                    service = get_service(i)
                    if not service:
                        service = "Unknown"
                    m = str(service)
                    c = str(i)
                    if len(c) == 1:
                        print(O+'    |   '+C+c+O+'    |   '+G+'OPEN   '+O+'|  '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
                    elif len(c) == 2:
                        print(O+'    |   '+C+c+'   '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
                    elif len(c) == 3:
                        print(O+'    |  '+C+c+'   '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
                    elif len(c) == 4:
                        print(O+'    |  '+C+c+'  '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
                    elif len(c) == 5:
                        print(O+'    | '+C+c+'  '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
            else:
                print(R+" [-] Sorry, No open ports found.!!")
            print(O+'\n [!] ' + str(len(closed_ports)) + ' closed ports not shown')
            print(C+" [!] Host %s scanned in %s seconds\n" %(host, total_time))

        except KeyboardInterrupt:
            print(R+'\n [!] User requested shutdown...')
            print(' [!] Exiting...\n')
            sys.exit(1)

    else:
        print(R+'\n [-] No input detected! ')
        print(O+' [!] Using no verbose mode...')
        print(GR+" [!] Scanning %s from port %s - %s: " % (host, start_port, end_port))
        print(B+" [*] Scanning started at %s" %(time.strftime("%I:%M:%S %p")))
        starting_time = time.time()

        try:
            print(O+" [*] Scan in progress..")
            print(C+" [*] Trying connections to Port:"+B+" ", end=' ')

            for p in range(start_port, end_port+1):
                sys.stdout.flush()
                print(p, end=' ')
                response = check_port(host, p)
                if response == 0:
                    open_ports.append(p)
                if not p == end_port:
                    sys.stdout.write('\b' * len(str(p)))

            print(G+"\n [+] Scanning completed at %s" %(time.strftime("%I:%M:%S %p")))
            ending_time = time.time()
            total_time = ending_time - starting_time
            print(GR+' [*] Preparing report...')
            time.sleep(0.4)
            print('\n')
            print(O+'    +-------------+')
            print(O+'    | SCAN REPORT '+O+'|')
            print(O+'    +-------------+')
            print(O+'    |')
            print(O+'    +--------+----------+-----------+')
            print(O+'    |  PORT  '+O+'|  STATE   '+O+'|  SERVICE  '+O+'|')
            print(O+'    +--------+----------+-----------+')

            if open_ports:
                for i in sorted(open_ports):
                    service = get_service(i)
                    if not service:
                        service = "Unknown"
                    m = str(service)
                    c = str(i)
                    if len(c) == 1:
                        print(O+'    |   '+C+c+O+'    |   '+G+'OPEN   '+O+'|  '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
                    elif len(c) == 2:
                        print(O+'    |   '+C+c+'   '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
                    elif len(c) == 3:
                        print(O+'    |  '+C+c+'   '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
                    elif len(c) == 4:
                        print(O+'    |  '+C+c+'  '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
                    elif len(c) == 5:
                        print(O+'    | '+C+c+'  '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                        print(O+'    +--------+----------+-----------+')
            else:
                print(R+" [-] Sorry, No open ports found.!!")
            print(O+'\n [!] ' + str(len(closed_ports)) + ' closed ports not shown')
            print(C+" [!] Host %s scanned in %s seconds\n" %(host, total_time))

        except KeyboardInterrupt:
            print(R+'\n [!] User requested shutdown...')
            print(' [!] Exiting...\n')
            sys.exit(1)


def servicedetect(web):

    print(GR+' [*] Loading up scanner...')
    time.sleep(0.5)
    if 'http://' in web:
        web = web.replace('http://','')
    elif 'https://' in web:
        web = web.replace('https://','')
    else:
        pass
    service0x00(web)
