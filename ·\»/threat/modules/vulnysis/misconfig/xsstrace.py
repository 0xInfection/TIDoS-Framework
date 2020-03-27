#!/usr/bin/env python
from core.colors import color
def xsstrace(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # coding: utf-8

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Forked from XSSTracer (to recode the entire stuff again)
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import socket
# import time
# import sys
# import getopt
# import httplib
# from core.Core.colors import *

# def xsstrace0x00(target):

#     print(R+'\n    =====================')
#     print(R+'     X S S   T R A C E R ')
#     print(R+'    =====================\n')

#     port = raw_input(O+' [#] Enter the port number to use (eg. 80) :> ')

#     if port == 443:
#         print(O+" [!] Using HTTPS <port 443>...")
#         print(GR+' [*] Setting headers...')
#         headers = {
#                 'User-Agent': 'The Infected Drake [@_tID] on Systems (TIDoS)',
#                 'Content-Type': 'application/x-www-form-urlencoded',
#                 }

#         print(GR+' [*] Requesting response...')
#         conn = httplib.HTTPSConnection(host)
#         conn.request("GET", "/", "", headers)
#         response = conn.getresponse()
#         print(' [*] Reading the response...')
#         data = response.read()

#         print(O+' [!] Response : '+GR, response.status, response.reason)
#         print(O+' [!] Data (raw) : \n'+GR)
#         print(data + '\n')

#     else:
#         print(GR+' [*] Setting buffers...')
#         buffer1 = "TRACE / HTTP/1.1"
#         buffer2 = "Test: <script>alert(tID);</script>"
#         buffer3 = "Host: " + target
#         buffer4 = "GET / HTTP/1.1"

#         s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         print(GR+' [*] Making the connection...')
#         result=s.connect_ex((target,int(port)))
#         s.settimeout(1.0)

#         if result == 0:

#             print(O+' [*] Making requests with buffers...')
#             time.sleep(0.5)
#             s.send(buffer1 + "\n")
#             s.send(buffer2 + "\n")
#             s.send(buffer3 + "\n\n")
#             data1 = s.recv(1024)
#             s.close()

#             script = "alert"
#             xframe = "X-Frame-Options"

#             if script.lower() in data1.lower():
#                 print(G+' [+] Site is vulnerable to Cross Site Tracing...')

#             else:
#                 print(R+' [-] Site is immune against Cross-Site Tracing...')
#             print("")

#             print(GR+' [*] Obtaining header dump data...')
#             time.sleep(1)
#             print("")
#             print(O+data1)
#             print("")

#         else:
#             print(R+' [-] Exception encountered!')
#             print(R+' [-] Port '+O+str(port)+' is closed!')

# def xsstrace(web):

#     print(GR+' [*] Loading the module...')
#     time.sleep(0.5)
#     if 'http' in web:
#         web = web.replace('http://','')
#         web = web.replace('https://','')

#     xsstrace0x00(web)
