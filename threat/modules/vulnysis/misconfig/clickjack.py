#!/usr/bin/env python
from core.colors import color
def clickjack(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # coding:  utf-8

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author: 0xInfection (@_tID)
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import sys, urllib2, time
# from time import sleep
# from core.Core.colors import *

# def clickjack(web):

#     print(R+'\n      ========================')
#     print(R+'      C L I C K J A C K I N G')
#     print(R+'     =========================\n')
#     try:
#         dom = web
#         print(''+C+' [*] Configuring the web address...')
#         time.sleep(0.8)
#         if "http" not in dom:
#             dom = "http://" + dom
#         print(''+GR+' [*] Checking the Web Address...')
#         time.sleep(0.4)
#         req = urllib2.urlopen(dom)
#         print(''+B+' [*] Requesting headers...')
#         time.sleep(0.7)
#         headers = req.info()
#         print(''+G+'\n [*] Checking for Clickjackability...')
#         time.sleep(0.5)
#         if not "X-Frame-Options" in headers:

#             print(''+O+' [!] The Website is clickjackable!!!')
#             time.sleep(0.2)
#             print(''+GR+' [*] Generating report...')
#             time.sleep(0.4)
#             print(''+C+' [*] POC as below... You can save it as a html file :)')
#             time.sleep(0.2)
#             code1 = """
#                 <html>
#                    <head><title>Clickjack test page</title></head>
#                       <body>
#                          <p>Website is vulnerable to clickjacking!</p>
#                          <iframe src="{}" width="1000" height="500"></iframe>
#                       </body>
#                 </html>
#             """.format(web)
#             code = """
# \033[1;32m<html>
#    \033[1;32m<head><title>\033[1;33mClickjack test page\033[1;32m</title></head>
#    \033[1;32m<body>
#      \033[1;32m<p>\033[1;33mWebsite is vulnerable to clickjacking!\033[1;32m</p>
#      \033[1;32m<iframe src=\033[1;36m"{}" \033[1;32mwidth="1000" height="500"></iframe>
#    \033[1;32m</body>
# \033[1;32m</html>
#             """.format(web)
#             print(code)

#             time.sleep(0.3)
#             w = raw_input(""+GR+" [*] Do you want to save this? (y/n) :> ")
#             if w == "y":
#                 print(''+B+' [!] Generating POC ...')
#                 time.sleep(1.0)
#                 web0 = web.split('//')[1]
#                 html_file = open("tmp/logs/"+web0+"-logs/"+web0+"-clickjack-poc.html","w+")
#                 html_file.write(code1)
#                 html_file.close()
#                 print('')
#                 print(''+G+' [+] POC successfully saved under tmp/logs/'+web0+"-logs/"+web0+'-clickjack-poc.html!')
#                 print('')
#             else:
#                 print(''+B+' [+] Okay :)')
#         else:
#             print(''+R+' [-] Website not vulnerable to clickjacking...')

#     except Exception as e:
#         print(''+R+' [-] Something went wrong!')
#         print(G+' [-] Error : '+str(e))
