#!/usr/bin/env python
from core.colors import color
def getports(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # -*- coding : utf-8

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author : @_tID
# #This script is a part of TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import time
# import sys
# import os
# import socket
# import scapy
# from scapy.all import *
# from core.Core.colors import *

# def scan0x00(host):

#     print(R+'\n   =========================')
#     print(R+'    P O R T   S C A N N E R')
#     print(R+'   =========================\n')
#     print(GR+' [*] Using most common ports...')

#     ports = [20,21,23,25,53,67,68,69,80,109,110,111,123,137,143,156,161,162,179,389,443,445,512,513,546,547,636,993,995,1099,2121,2049,3306, 5432,5900,6000,6667,8080,8180,8443,10000]
#     print(O+' [+] Scanning %s ports...' % len(ports))
#     try:
#         ip = socket.gethostbyname(host)
#         print(G+'\n [+] Target server detected up and running...')
#         print(GR+' [*] Preparing for scan...')
#         pass
#     except:
#         print(R+' [-] Server not responding...')
#         time.sleep(0.3)
#         print(R+' [*] Exiting...')
#         quit()

#     open_ports = []
#     closed_ports = []

#     def check_portv(host, port, result = 1):
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(0.5)
#             print(C+"\n [*] Scanning port " + str(port)+'...')
#             r = sock.connect_ex((host, port))
#             print(GR+' [*] Analysing response...')
#             time.sleep(0.5)
#             print(O+' [*] Adding up results together...')
#             time.sleep(0.1)
#             if r == 0:
#                 result = r

#             sock.close()

#         except Exception as e:
#             print(''+R+' [!] Exception detected at port %s !' % port)
#             pass

#         return result

#     print(B+" [*] Scanning started at %s" %(time.strftime("%I:%M:%S %p")))
#     starting_time = time.time()
#     try:
#         print(O+" [*] Scan in progress..")
#         time.sleep(0.8)
#         for p in ports:
#             sys.stdout.flush()
#             response = check_portv(host, p)
#             if response == 0:
#                 print(G+' [!] Port ' +O+ str(p) +G+ ' detected Open !')
#                 open_ports.append(p)
#             else:
#                 print(R+' [!] Port ' +O+ str(p) +R+ ' detected Closed !')
#                 closed_ports.append(p)

#         print(C+"\n [+] Scanning completed at %s" %(time.strftime("%I:%M:%S %p")))
#         ending_time = time.time()
#         total_time = ending_time - starting_time
#         print(O+' [*] Preparing report...\n')
#         time.sleep(1)

#         print(O+'    +--------+----------+')
#         print(O+'    |  '+GR+'PORT  '+O+'|  '+GR+'STATE   '+O+'|')
#         print(O+'    +--------+----------+')

#         if open_ports:
#             for i in sorted(open_ports):
#                 c = str(i)
#                 if len(c) == 1:
#                     print(O+'    |   '+C+c+O+'    |   '+G+'OPEN   '+O+'|')
#                     print(O+'    +--------+----------+')
#                     time.sleep(0.2)
#                 elif len(c) == 2:
#                     print(O+'    |   '+C+c+'   '+O+'|   '+G+'OPEN   '+O+'| ')
#                     print(O+'    +--------+----------+')
#                     time.sleep(0.2)
#                 elif len(c) == 3:
#                     print(O+'    |  '+C+c+'   '+O+'|   '+G+'OPEN   '+O+'| ')
#                     print(O+'    +--------+----------+')
#                     time.sleep(0.2)
#                 elif len(c) == 4:
#                     print(O+'    |  '+C+c+'  '+O+'|   '+G+'OPEN   '+O+'| ')
#                     print(O+'    +--------+----------+')
#                     time.sleep(0.2)
#                 elif len(c) == 5:
#                     print(O+'    | '+C+c+'  '+O+'|   '+G+'OPEN   '+O+'| ')
#                     print(O+'    +--------+----------+')
#                     time.sleep(0.2)
#         else:
#             print(R+"\n [-] No open ports found.!!\n")
#         print(B+'\n [!] ' + str(len(closed_ports)) + ' closed ports not shown')
#         print(G+" [+] Host %s scanned in %s seconds\n" %(host, total_time))

#     except KeyboardInterrupt:
#         print(R+"\n [-] User requested shutdown... ")
#         print(' [-] Exiting...\n')
#         quit()

# def getports(web):

#     print(GR+' [*] Loading up scanner...')
#     time.sleep(0.5)
#     if 'http://' in web:
#         web = web.replace('http://','')
#     elif 'https://' in web:
#         web = web.replace('https://','')
#     else:
#         pass
#     scan0x00(web)
