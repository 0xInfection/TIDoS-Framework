#!/usr/bin/env python
from core.colors import color
def piwebenum(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # coding:  utf-8

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author : @_tID
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import os, requests, time
# from time import sleep
# from core.Core.colors import *

# def piwebenum(web):

#     time.sleep(0.4)
#     web = web.split('//')[1]
#     print(R+'\n   =============================================')
#     print(R+'    P I N G / N P I N G   E N U M E R A T I O N')
#     print(R+'   =============================================\n')
#     print(GR + ' [!] Pinging website...')
#     time.sleep(0.5)
#     print(O+' [*] Using adaptative ping and debug mode with count 5...')
#     time.sleep(0.4)
#     print(GR+' [!] Press Ctrl+C to stop\n'+C)
#     os.system('ping -D -c 5 '+ web)
#     print('')
#     time.sleep(0.6)
#     print(O+' [*] Trying NPing (NMap Ping)...')
#     print(C+" [~] Result: \n")
#     print('')
#     text = requests.get('http://api.hackertarget.com/nping/?q=' + web).text
#     nping = str(text)
#     print(G+ nping +'\n')
