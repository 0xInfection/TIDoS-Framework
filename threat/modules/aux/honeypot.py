#!/usr/bin/env python
from core.colors import color
def honeypot(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import socket
# import requests
# import time
# from core.Core.colors import *
# from files.API_KEYS import SHODAN_API_KEY

# def honeypot(web):

#     print(R+'    ===================================')
#     print(R+'     H O N E Y P O T   D E T E C T O R')
#     print(R+'    ===================================')
#     print(GR+' [*] Configuring APi request...')
#     time.sleep(0.7)
#     print(O+' [!] Reading APi Key...')
#     if SHODAN_API_KEY != '':
#         print(G+' [+] Key Found : '+O+SHODAN_API_KEY)
#         web0 = web.split('//')[1]
#         ip = socket.gethostbyname(web0)
#         honey = "https://api.shodan.io/labs/honeyscore/"+ip+"?key="+SHODAN_API_KEY
#         req = requests.get(honey).text
#         read = float(req)
#         if read < 5.0:
#             print(G+' [+] Target does not seem to be a potential Honeypot...')
#             print(G+' [+] Honey Score : '+O+str(read*100)+'%')

#         else:
#             print(R+' [-] Potential Honeypot Detected!')
#             print(R+' [+] Honey Score : '+O+str(read*100)+'%')

#     else:
#         print(R+' [-] Shodan APi key not set!')
#         print(R+' [-] Cannot use this module!')
