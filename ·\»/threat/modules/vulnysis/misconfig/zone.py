#!/usr/bin/env python
from core.colors import color
def zone(target):
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
# import time
# import requests
# import subprocess
# import os
# from core.Core.colors import *

# def zone(web):

#     web = web.replace('http://','')
#     web = web.replace('https://','')
#     try:
#         print(R+'\n   ===========================')
#         print(R+'    Z O N E   T R A N S F E R')
#         print(R+'   ===========================\n')
#         time.sleep(0.4)
#         print(O+' [!] Looking up for name servers on which website is hosted...\n'+G)
#         time.sleep(0.7)
#         os.system('dig +nocmd '+web+' ns +noall +answer')
#         h = raw_input(O+'\n [*] Enter the DNS Server you want to test for :> ')
#         time.sleep(0.4)
#         print(GR+' {*] Attempting zone transfer...')
#         time.sleep(0.9)
#         cm = subprocess.Popen(['host','-t','axfr',web,h,'+answer','+noall','+nocmd'], stdout = subprocess.PIPE).communicate()[0]
#         if 'failed' in str(cm):
#             print(R+'\n [-] Zone transfer for '+O+h+R+' failed!')
#             print(R+' [-] This website is immune to sone transfers!')
#         else:
#             print('\n'+G+cm)

#     except Exception as e:
#         print(R+' [-] Error encountered!')
#         print(R+' [-] Error : '+str(e))
