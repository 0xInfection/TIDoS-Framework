
#!/usr/bin/env python
from core.colors import color
def encodeall(target):
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
# import urllib
# from core.Core.colors import *
# from cgi import escape
# from time import sleep
# try:
#     import StringIO # python2
# except ImportError:
#     from io import StringIO
#     # python3
# import gzip
# import os

# def url0x00(url):

#     encoded = urllib.quote_plus(url)
#     print(G+" [+] Encoded string : "+O, encoded)

# def html0x00(st):

#     encod = ''
#     stri = list(st)
#     for i in stri:
#         encod = encod + escape(i)
#     print(G+' [+] Encoded String : '+O, encod)

# def base640x00(st):

#     m = st.encode('base64', 'strict')
#     print(G+' [+] Encoded String : '+O+m)

# def ascii0x00(st):

#     m = st.decode('unicode_escape')
#     print(G+' [+] Encoded String : '+O+m)

# def hex0x00(st):

#     m = st.encode('hex', 'strict')
#     print(G+' [+] Encoded String : '+O+m)

# def octal0x00(st):

#     result = []
#     for char in st:
#         result.append('\%o' % ord(char))
#     print(G+' [+] Octal Encoded String : '+O+str(''.join(result)))

# def binary0x00(st):

#     m = ''.join(format(ord(x),'b') for x in st)
#     print(G+' [+] Encoded String : '+O+m)

# def gzip0x00(st):

#     m = st.encode('zlib','strict')
#     print(G+' [+] Encoded String : '+O+m)


# def encodeall():
#     try:
#         print(R+'\n    =============================')
#         print(R+'     S T R I N G   E N C O D E R')
#         print(R+'    =============================\n')
#         st = raw_input(O+' [-] Enter a string to be encoded :> ')

#         def encode0x00(st):
#             print(O+'\n  Choose from the options to encode to:\n')
#             print(B+'    [1]'+C+' URL Encode')
#             print(B+'    [2]'+C+' HTML Encode')
#             print(B+'    [3]'+C+' Base64 Encode')
#             print(B+'    [4]'+C+' Plain ASCII Encode')
#             print(B+'    [5]'+C+' Hex Encode')
#             print(B+'    [6]'+C+' Octal Encode')
#             print(B+'    [7]'+C+' Binary Encode')
#             print(B+'    [8]'+C+' GZip Encode\n')
#             print(B+'    [99]'+C+' Back\n')
#             r = raw_input(O+' [#] Enter your option :> ')
#             print(GR+' [*] Encoding string...')
#             sleep(0.5)
#             if r == '1':
#                 url0x00(st)
#                 raw_input(O+'\n [+] Press '+GR+'Enter'+O+' to Continue...')
#                 encode0x00(st)
#             elif r == '2':
#                 html0x00(st)
#                 raw_input(O+'\n [+] Press '+GR+'Enter'+O+' to Continue...')
#                 encode0x00(st)
#             elif r == '3':
#                 base640x00(st)
#                 raw_input(O+'\n [+] Press '+GR+'Enter'+O+' to Continue...')
#                 encode0x00(st)
#             elif r == '4':
#                 ascii0x00(st)
#                 raw_input(O+'\n [+] Press '+GR+'Enter'+O+' to Continue...')
#                 encode0x00(st)
#             elif r == '5':
#                 hex0x00(st)
#                 raw_input(O+'\n [+] Press '+GR+'Enter'+O+' to Continue...')
#                 encode0x00(st)
#             elif r == '6':
#                 octal0x00(st)
#                 raw_input(O+'\n [+] Press '+GR+'Enter'+O+' to Continue...')
#                 encode0x00(st)
#             elif r == '7':
#                 binary0x00(st)
#                 raw_input(O+'\n [+] Press '+GR+'Enter'+O+' to Continue...')
#                 encode0x00(st)
#             elif r == '8':
#                 gzip0x00(st)
#                 raw_input(O+'\n [+] Press '+GR+'Enter'+O+' to Continue...')
#                 encode0x00(st)
#             elif r == '99':
#                 print(G+' [+] Back!')
#                 os.system('clear')
#         encode0x00(st)

#     except Exception as e:
#         print(R+" [-] Caught Exception : "+str(e))
