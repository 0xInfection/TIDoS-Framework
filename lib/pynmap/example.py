#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""
example.py - 2011.11.09

Author : Alexandre Norman - norman@xael.org
Contributor: Steve 'Ashcrow' Milner - steve@gnulinux.net
Licence : GPL v3 or any later version


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import sys
import os

import nmap                         # import nmap.py module
try:
    nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit(1)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(1)


# Data structure looks like :
#
#      {'addresses': {'ipv4': '127.0.0.1'},
#       'hostnames': [],
#       'osmatch': [{'accuracy': '98',
#                    'line': '36241',
#                    'name': 'Juniper SA4000 SSL VPN gateway (IVE OS 7.0)',
#                    'osclass': [{'accuracy': '98',
#                                 'cpe': ['cpe:/h:juniper:sa4000',
#                                         'cpe:/o:juniper:ive_os:7'],
#                                 'osfamily': 'IVE OS',
#                                 'osgen': '7.X',
#                                 'type': 'firewall',
#                                 'vendor': 'Juniper'}]},
#                   {'accuracy': '91',
#                    'line': '17374',
#                    'name': 'Citrix Access Gateway VPN gateway',
#                    'osclass': [{'accuracy': '91',
#                                 'cpe': [],
#                                 'osfamily': 'embedded',
#                                 'osgen': None,
#                                 'type': 'proxy server',
#                                 'vendor': 'Citrix'}]}],
#       'portused': [{'portid': '443', 'proto': 'tcp', 'state': 'open'},
#                    {'portid': '113', 'proto': 'tcp', 'state': 'closed'}],
#       'status': {'reason': 'syn-ack', 'state': 'up'},
#       'tcp': {113: {'conf': '3',
#                     'cpe': '',
#                     'extrainfo': '',
#                     'name': 'ident',
#                     'product': '',
#                     'reason': 'conn-refused',
#                     'state': 'closed',
#                     'version': ''},
#               443: {'conf': '10',
#                     'cpe': '',
#                     'extrainfo': '',
#                     'name': 'http',
#                     'product': 'Juniper SA2000 or SA4000 VPN gateway http config',
#                     'reason': 'syn-ack',
#                     'state': 'open',
#                     'version': ''}},
#       'vendor': {}}



nm.scan('127.0.0.1', '22-443')      # scan host 127.0.0.1, ports from 22 to 443
nm.command_line()                   # get command line used for the scan : nmap -oX - -p 22-443 127.0.0.1
nm.scaninfo()                       # get nmap scan informations {'tcp': {'services': '22-443', 'method': 'connect'}}
nm.all_hosts()                      # get all hosts that were scanned
nm['127.0.0.1'].hostname()          # get one hostname for host 127.0.0.1, usualy the user record
nm['127.0.0.1'].hostnames()         # get list of hostnames for host 127.0.0.1 as a list of dict [{'name':'hostname1', 'type':'PTR'}, {'name':'hostname2', 'type':'user'}]
nm['127.0.0.1'].state()             # get state of host 127.0.0.1 (up|down|unknown|skipped) 
nm['127.0.0.1'].all_protocols()     # get all scanned protocols ['tcp', 'udp'] in (ip|tcp|udp|sctp)
if ('tcp' in nm['127.0.0.1']):
    list(nm['127.0.0.1']['tcp'].keys()) # get all ports for tcp protocol

nm['127.0.0.1'].all_tcp()           # get all ports for tcp protocol (sorted version)
nm['127.0.0.1'].all_udp()           # get all ports for udp protocol (sorted version)
nm['127.0.0.1'].all_ip()            # get all ports for ip protocol (sorted version)
nm['127.0.0.1'].all_sctp()          # get all ports for sctp protocol (sorted version)
if nm['127.0.0.1'].has_tcp(22):     # is there any information for port 22/tcp on host 127.0.0.1
    nm['127.0.0.1']['tcp'][22]          # get infos about port 22 in tcp on host 127.0.0.1
    nm['127.0.0.1'].tcp(22)             # get infos about port 22 in tcp on host 127.0.0.1
    nm['127.0.0.1']['tcp'][22]['state'] # get state of port 22/tcp on host 127.0.0.1 (open


# a more usefull example :
for host in nm.all_hosts():
    print('----------------------------------------------------')
    print('Host : {0} ({1})'.format(host, nm[host].hostname()))
    print('State : {0}'.format(nm[host].state()))

    for proto in nm[host].all_protocols():
        print('----------')
        print('Protocol : {0}'.format(proto))

        lport = list(nm[host][proto].keys())
        lport.sort()
        for port in lport:
            print('port : {0}\tstate : {1}'.format(port, nm[host][proto][port]))


print('----------------------------------------------------')
# print result as CSV
print(nm.csv())



print('----------------------------------------------------')
# If you want to do a pingsweep on network 192.168.1.0/24:
nm.scan(hosts='192.168.0.0/24', arguments='-n -sP -PE -PA21,23,80,3389')
hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
for host, status in hosts_list:
    print('{0}:{1}'.format(host, status))





print('----------------------------------------------------')
# Asynchronous usage of PortScannerAsync


nma = nmap.PortScannerAsync()

def callback_result(host, scan_result):
    print('------------------')
    print(host, scan_result)

nma.scan(hosts='192.168.0.0/30', arguments='-sP', callback=callback_result)

while nma.still_scanning():
    print("Waiting ...")
    nma.wait(2)   # you can do whatever you want but I choose to wait after the end of the scan

if (os.getuid() == 0):
    print('----------------------------------------------------')
    # Os detection (need root privileges)
    nm.scan("127.0.0.1", arguments="-O")
    if 'osmatch' in nm['127.0.0.1']:
        for osmatch in nm['127.0.0.1']['osmatch']:
            print('OsMatch.name : {0}'.format(osmatch['name']))
            print('OsMatch.accuracy : {0}'.format(osmatch['accuracy']))
            print('OsMatch.line : {0}'.format(osmatch['line']))
            print('')

            if 'osclass' in osmatch:
                for osclass in osmatch['osclass']:
                    print('OsClass.type : {0}'.format(osclass['type']))
                    print('OsClass.vendor : {0}'.format(osclass['vendor']))
                    print('OsClass.osfamily : {0}'.format(osclass['osfamily']))
                    print('OsClass.osgen : {0}'.format(osclass['osgen']))
                    print('OsClass.accuracy : {0}'.format(osclass['accuracy']))
                    print('')


    if 'fingerprint' in nm['127.0.0.1']:
        print('Fingerprint : {0}'.format(nm['127.0.0.1']['fingerprint']))


    # Vendor list for MAC address
    print('scanning localnet')
    nm.scan('192.168.0.0/24', arguments='-O')
    for h in nm.all_hosts():
        print(h)
        if 'mac' in nm[h]['addresses']:
            print(nm[h]['addresses'], nm[h]['vendor'])



print('----------------------------------------------------')
# Read output captured to a file
# Example : nmap -oX - -p 22-443 -sV 127.0.0.1 > nmap_output.xml

with open("./nmap_output.xml", "r") as fd:
    content = fd.read()
    nm.analyse_nmap_xml_scan(content)
    print(nm.csv())



print('----------------------------------------------------')
# Progressive scan with generator
nm = nmap.PortScannerYield()
for progressive_result in nm.scan('127.0.0.1/24', '22-25'):
    print(progressive_result)
