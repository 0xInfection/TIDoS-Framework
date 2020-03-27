#!/usr/bin/env python
from core.colors import color
def sslcert(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# #-:-:-:-:-:-:-:-:-:-:-:#
# #   TIDoS Framework    #
# #-:-:-:-:-:-:-:-:-:-:-:#

# #Author : @_tID
# #This module is a part of TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import socket
# import ssl
# import time
# from core.Core.colors import *

# def sslcert(web):

#     if 'https' not in web:
#         print(R+' [-] Website does not use SSL...')
#     else:
#         if str(web).split("/")[2]:
#             web = str(web).split("/")[2]
#         elif str(web).split("/")[3]:
#             web = str(web).split("/")[2]
#         cerp = []
#         print(R+'\n   =========================================')
#         print(R+'    S S L   C E R T I F I C A T E   I N F O')
#         print(R+'   =========================================\n')
#         time.sleep(0.3)
#         context = ssl.create_default_context()
#         server = context.wrap_socket(socket.socket(), server_hostname=web)
#         server.connect((web, 443))
#         cer = server.getpeercert()
#         cerpec = server.cipher()
#         for x in cerpec:
#             cerp.append(x)
#         print(B+" [+] Certificate Serial Number : "+W+ str(cer.get('serialNumber')))
#         print(B+" [+] Certificate SSL Version : "+W+ str(cer.get('version')))
#         print(B+' [+] SSL Cipher Suite : '+W+ str(cerp[0]))
#         print(B+' [+] Encryption Protocol : '+W+ str(cerp[1]))
#         print(B+' [+] Encryption Type : '+W+ str(cerp[2]) + ' bit')
#         print(B+' [+] Certificate as Raw : \n'+W+str(cer))
