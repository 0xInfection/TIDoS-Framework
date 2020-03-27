#!/usr/bin/env python
from core.colors import color
def piweb(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author : @_tID
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import requests
# import time
# from core.Core.colors import *

# def piweb(web):

#     dom = web.split('//')[1]
#     print(R+'\n   =====================')
#     print(R+'    P I N G   C H E C K ')
#     print(R+'   =====================\n')
#     time.sleep(0.4)
#     print(GR + color.BOLD + ' [!] Pinging website using external APi...')
#     time.sleep(0.4)
#     print(GR + color.BOLD + " [~] Result: "+ color.END)
#     text = requests.get('http://api.hackertarget.com/nping/?q=' + dom).text
#     nping = str(text)
#     if 'error' not in nping:
#         print(G+ nping)
#     else:
#         print(R+' [-] Outbound Query Exception!')
#         time.sleep(0.8)
