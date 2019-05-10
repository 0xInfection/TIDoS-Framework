#!/usr/bin/env python
from core.colors import color
def proxybrute(target):
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
# import time
# import requests
# import sys
# sys.path.append('lib/fileutils_mod/')
# from FileUtils import FileUtils
# from core.Core.colors import *
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# file_paths = []
# dir_path = []

# def check0x00(web, dirpath, headers):

#     try:
#         for dirs in dirpath:
#             web0x00 = web + dirs
#             req = requests.get(web0x00, headers=headers, allow_redirects=False, timeout=7, verify=False)
#             try:
#                 if (req.headers['content-length'] is not None):
#                     size = int(req.headers['content-length'])
#                 else:
#                     size = 0

#             except (KeyError, ValueError, TypeError):
#                 size = len(req.content)
#             finally:
#                 size = FileUtils.sizeHuman(size)

#             resp = str(req.status_code)
#             if (resp == '200' or resp == '302' or resp == '304'):
#                 print(G+' [*] Found : ' + O + web0x00 +GR+' - '+ size + G + ' ('+resp+')')
#                 file_paths.append(web0x00)

#             else:
#                 print(C+' [*] Checking : ' + B + web0x00 + R + ' ('+resp+')')
#         return file_paths

#     except Exception as e:
#         print(R+' [-] Unknown Exception Encountered!')
#         print(R+' [-] Exception : '+str(e))
#         return file_paths

# def getFile0x00(filepath):

#     if os.path.exists(filepath) == True:
#         time.sleep(0.5)
#         print(GR+' [*] Importing wordlist...')
#         with open(filepath, 'r') as f0:
#             for f in f0:
#                 f = f.strip('\n')
#                 if f.startswith('/'):
#                     dir_path.append(f)
#                 else:
#                     f = '/' + f
#                     dir_path.append(f)

#     else:
#         print(R+' [-] No file path found under ' +filepath+'!')
#     return dir_path

# def proxybrute(web):

#     print(GR+' [*] Loading module...')
#     time.sleep(0.5)
#     print(R+'\n    ================================================')
#     print(R+'     P R O X Y   C O N F I G.   B R U T E F O R C E')
#     print(R+'    ================================================\n')

#     print(O+' [*] Path to file to be used '+R+'(Default: files/fuzz-db/proxy_paths.lst)...')
#     fil = raw_input(O+' [#] Your input (Press Enter if default) :> ')
#     if fil == '':
#         fil = 'files/fuzz-db/proxy_paths.lst'
#     else:
#         print(GR+' [*] Checking filepath...')
#         if os.path.exists(fil) == True:
#             print(G+' [+] File found!')
#         else:
#             print(R+' [-] File not found!')

#     mo = getFile0x00(fil)
#     gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
#                       'Accept-Language':'en-US;',
#                       'Accept-Encoding': 'gzip, deflate',
#                       'Accept': 'text/html, application/xhtml+xml, application/xml;',
#                       'Connection':'close'}
#     try:
#         ul = check0x00(web, mo, gen_headers)
#     except KeyboardInterrupt:
#         print(GR+' [*] Stopping Bruteforce...')
#         pass
#     if ul:
#         print(G+' [+] The following possible proxy config. paths were found!')
#         for u in ul:
#             print(G+' [+] Proxy config path : '+O+u)
#     else:
#         print(R+' [-] No common proxy config paths were found!')
#     print(G+' [+] Done!')
