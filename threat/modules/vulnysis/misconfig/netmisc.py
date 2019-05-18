#!/usr/bin/env python
from core.colors import color
def netmisc(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # coding: utf-8

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import nmap
# import time
# from core.Core.colors import *
# import socket

# def netmisc0x00(web):

#     web = web.replace('http://','')
#     web = web.replace('https://','')
#     ip = socket.gethostbyname(web)
#     port = 23 # telnet port
#     try:
#         print(O+' [!] Configuring scanner for telnet ports...')
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.settimeout(5)
#         print(C+"\n [*] Connecting to '%s' via port %s" % (ip, port))
#         r = sock.connect_ex((ip, port))
#         time.sleep(0.1)
#         if r == 0:
#             print(G+' [+] Telnet port detected open!')
#             time.sleep(0.5)
#             print(O+' [*] Confirming...')
#             nmScan = nmap.PortScanner()
#             nmScan.scan(ip, '23')
#             port = 23
#             thisDict = nmScan[ip]['tcp'][port]
#             print(G+' [+] Telnet network misconfiguration confirmed!')
#             time.sleep(0.5)
#             if thisDict['version']:
#                 print(G+' [+] Port ' + str(port) + ': ' +C+ thisDict['product'] +GR+ ', v' + thisDict['version'])
#             else:
#                 print(G+' [+] Port ' + str(port) + ': ' +C+ thisDict['product'])
#         else:
#             print(R+' [-] Telnet Disabled!')
#         sock.close()

#     except Exception as e:
#         print('\n'+R+' [!] Exception detected at port %s !' % port)
#         print(R+' [-] Error : '+str(e))

# def netmisc(web):

#     print(GR+' [*] Loading module...')
#     print(R+'\n    ===================================')
#     print(R+'     TELNET ENABLED (Network Misconf.)')
#     print(R+'    ===================================\n')

#     print(GR+' [*] Loading up port scanner...')
#     netmisc0x00(web)
#     time.sleep(0.5)
