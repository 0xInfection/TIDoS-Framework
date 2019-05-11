# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author : @_tID
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import re
# import time
# import os
# import sys
# from core.colors import color
# sys.path.append('files/')
# from lib.dnsdump_mod.DNSDumpsterAPI import *

# def dnschk(target):
#     for t in target:
#         domain = t.name.replace('http://','').replace('https://','')
#         res = DNSDumpsterAPI(False).search(domain)
#         try:
#             print(G+'\n [+] DNS Records')
#             for entry in res['dns_records']['dns']:
#                 print(''+O+("{domain} ({ip}) {as} {provider} {country}".format(**entry)))
#             for entry in res['dns_records']['mx']:
#                 print(G+"\n [+] MX Records")
#                 print(''+O+("{domain} ({ip}) {as} {provider} {country}".format(**entry)))
#             print(G+"\n [+] Host Records (A)")
#             for entry in res['dns_records']['host']:
#                 if entry['reverse_dns']:
#                     print((O+"{domain} ({reverse_dns}) ({ip}) {as} {provider} {country}".format(**entry)))
#                 else:
#                     print(O+("{domain} ({ip}) {as} {provider} {country}".format(**entry)))
#             print(G+'\n [+] TXT Records:')
#             for entry in res['dns_records']['txt']:
#                 print(''+O+entry)
#             print(GR+'\n [*] Preparing DNS Map...')
#             time.sleep(0.5)
#             url = 'https://dnsdumpster.com/static/map/' + str(domain) + '.png'
#             print(GR+' [!] Fetching map...')
#             try:
#                 os.system('wget -q ' + url)
#             except:
#                 print(R+' [-] Map generation failed!')
#                 sys.exit(1)
#             st = str(domain) + '.png'
#             st1 = str(domain)+'-dnsmap.jpg'
#             p = 'mv '+st+' '+ st1
#             os.system(p)
#             mov = 'mv '+ st1 + ' tmp/'
#             os.system(mov)
#             print(G+' [+] Map saved under "tmp/' + st1 + '"')
#             try:
#                 print(GR+' [!] Trying to open DNS Map...')
#                 os.system('xdg-open tmp/'+st1)
#             except:
#                 print(R+' [-] Failed to open automatically.')
#                 print(GR+' [!] Please view the map manually.')
#         except TypeError:
#             print(R+' [-] No standard publicly recorded DNS records found.\n')