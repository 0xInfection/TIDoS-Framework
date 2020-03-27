#!/usr/bin/env python
from core.colors import color
def traceroute(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # coding:  utf-8

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author : @_tID
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import os
# from time import sleep
# from core.colors import color

# def traceroute(web):

#     print(R+'\n   =====================')
#     print(R+'    T R A C E R O U T E')
#     print(R+'   =====================\n')

#     web = web.replace('https://','')
#     web = web.replace('http://','')
#     m = raw_input(O+' [#] Do you want to fragment the packets? (y/n) :> ')
#     if m == 'y' or m == 'Y':
#         print(GR+' [!] Using fragmented packets...')
#         p = raw_input(O+' [#] Enter the network type to be used [(I)CMP/(T)CP] :> ')
#         if p == 'icmp' or p == 'ICMP' or p == 'I' or p == 'i':
#             print(GR+' [*] Using ICMP ECHO type for traceroute...')
#             w = raw_input(O+' [*] Enable socket level debugging? (y/n) :> ')
#             if w == 'y' or w == 'Y':
#                 print(GR+' [+] Enabling socket level debugging...')
#                 sleep(0.3)
#                 print(GR+' [+] Starting traceroute...'+G)
#                 os.system('traceroute -I -d '+web)
#             elif w == 'n' or w == 'N':
#                 sleep(0.3)
#                 print(GR+' [+] Starting traceroute...'+G)
#                 os.system('traceroute -I '+web)
#             else:
#                 print(R+' [-] Invalid choice...')
#                 traceroute(web)
#         elif p == 'tcp' or p == 'TCP' or p == 't' or p == 'T':
#             print(GR+' [*] Using TCP/SYN for traceroute...')
#             w = raw_input(O+' [*] Enable socket level debugging? (y/n) :> ')
#             if w == 'y' or w == 'Y':
#                 print(GR+' [+] Enabling socket level debugging...')
#                 sleep(0.3)
#                 print(GR+' [+] Starting traceroute...'+G)
#                 os.system('traceroute -T -d '+web)
#             elif w == 'n' or w == 'N':
#                 sleep(0.3)
#                 print(GR+' [+] Starting traceroute...'+G)
#                 os.system('traceroute -T '+web)
#             else:
#                 print(R+' [-] Invalid choice...')
#                 traceroute(web)
#         else:
#             print(R+' [-] Invalid choice...')
#             traceroute(web)
#     elif m == 'n' or m == 'N':
#         print(GR+' [!] Using unfragmented packets...')
#         p = raw_input(O+' [#] Enter the network type to be used (ICMP/TCP) :> ')
#         if p == 'icmp' or p == 'ICMP' or p == 'I' or p == 'i':
#             print(GR+' [*] Using ICMP ECHO type for traceroute...')
#             w = raw_input(O+' [*] Enable socket level debugging? (y/n) :> ')
#             if w == 'y' or w == 'Y':
#                 print(GR+' [+] Enabling socket level debugging...')
#                 sleep(0.3)
#                 print(GR+' [+] Starting traceroute...'+G)
#                 os.system('traceroute -I -d -F '+web)
#             elif w == 'n' or w == 'N':
#                 sleep(0.3)
#                 print(GR+' [+] Starting traceroute...'+G)
#                 os.system('traceroute -I -F '+web)
#             else:
#                 print(R+' [-] Invalid choice...')
#                 traceroute(web)
#         elif p == 'tcp' or p == 'TCP' or p == 't' or p == 'T':
#             print(GR+' [*] Using TCP/SYN for traceroute...')
#             w = raw_input(O+' [*] Enable socket level debugging? (y/n) :> ')
#             if w == 'y' or w == 'Y':
#                 print(GR+' [+] Enabling socket level debugging...')
#                 sleep(0.3)
#                 print(GR+' [+] Starting traceroute...'+G)
#                 os.system('traceroute -T -d -F '+web)
#             elif w == 'n' or w == 'N':
#                 sleep(0.3)
#                 print(GR+' [+] Starting traceroute...'+G)
#                 os.system('traceroute -T -F '+web)
#             else:
#                 print(R+' [-] Invalid choice...')
#                 traceroute(web)
#         else:
#             print(R+' [-] Invalid choice...')
#             traceroute(web)
#     else:
#         print(R+' [-] Invalid choice...')
#         traceroute(web)

#     print(G+' [+] Traceroute done.\n')
