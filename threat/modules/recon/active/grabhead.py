#!/usr/bin/env python
from core.colors import color
def grabhead(target):
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
# import urllib2
# import time
# import sys
# from time import sleep
# from core.Core.colors import *

# def grabhead(web):
#     time.sleep(0.4)
#     print(R+'\n      ==================================')
#     print(R+'      G R A B   H T T P   H E A D E R S')
#     print(R+'     ===================================\n')
#     print(GR + color.BOLD + ' [*] Grabbing HTTP Headers...')
#     time.sleep(0.4)
#     web = web.rstrip()
#     try:
#         header = str(urllib2.urlopen(web).info()).splitlines()
#         print('')
#         for m in header:
#             n = m.split(':')
#             print('  '+C+n[0]+': '+O+n[1])
#         print('')
#     except urllib2.HTTPError as e:
#         print(R+' [-] '+e.__str__())
