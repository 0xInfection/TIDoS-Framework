#!/usr/bin/env python
from core.colors import color
def googledorker(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # coding: utf-8

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author : @_tID
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# try:
#     from google import search
# except:
#     from googlesearch import search
# import os
# import time
# import urllib2
# from random import randint
# from time import sleep
# from core.Core.colors import *

# def googledorker(web):

#     site = str(web)
#     def clear_cookie():
#         fo = open(".google-cookie", "w")
#         fo.close()


#     def google_it (site,dork):
#         clear_cookie()
#         for title in search(dork, stop=30):
#             print(GR+' [!] Site Found :> '+B+title)
#             time.sleep(0.1)

#     try:

#         print(R+'\n   ===========================')
#         print(R+'    G O O G L E   D O R K E R')
#         print(R+'   ===========================\n')
#         print(O+' [-] Warning! You may get a captcha if you are being too frequent...')
#         print(GR+' [*] Initializing google dorking...')

#         print (C+" [*] Finding Login Pages for "+site+"...\n")
#         google_it (site,"site:"+site+" inurl:wp- OR inurl:login OR inurl:signin OR inurl:checkin OR inurl:join")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))

#         print (C+" [*] Finding Subdomains for "+site+"...\n")
#         google_it (site,"site:*."+site+"")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))

#         print (C+" [*] Finding Sub-subdomains for "+site+"...\n")
#         google_it (site,"site:*.*."+site+"")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))

#         print (C+" [*] Finding Upload/Download Pages for "+site+"...\n")
#         google_it (site,"site:"+site+" inurl:wp- OR inurl:plugin OR inurl:upload OR inurl:download")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))

#         print (C+" [*] Finding Backdoors for "+site+"...\n")
#         google_it (site,"site:"+site+" inurl:shell OR inurl:backdoor OR inurl:wso OR inurl:cmd OR shadow OR passwd OR boot.ini OR inurl:backdoor")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))

#         print (C+" [*] Finding Install / Setup files for "+site+"...\n")
#         google_it (site,"site:"+site+" inurl:readme OR inurl:license OR inurl:install OR inurl:setup OR inurl:config")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))

#         print (C+" [*] Finding WORDPRESS PLUGINS/UPLOADS/DOWNLOADS for "+site+"...\n")
#         google_it (site,"site:"+site+" inurl:wp- OR inurl:plugin OR inurl:upload OR inurl:download")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))

#         print (C+" [*] Finding OPEN REDIRECTS for "+site+"...\n")
#         google_it (site,"site:"+site+" inurl:redir OR inurl:url OR inurl:redirect OR inurl:return OR inurl:src=http OR inurl:r=http")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))

#         print (C+" [*] Finding FILES BY EXTENSION for "+site+"...\n")
#         google_it (site,"site:"+site+" ext:cgi OR ext:php OR ext:asp OR ext:aspx OR ext:jsp OR ext:jspx OR ext:swf OR ext:fla OR ext:xml")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))

#         print (C+" [*] Finding DOCUMENTS BY EXTENSION for "+site+"...\n")
#         google_it (site,"site:"+site+" ext:doc OR ext:docx OR ext:csv OR ext:pdf OR ext:txt OR ext:log OR ext:bak")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))

#         print (C+" [*] Finding EMPLOYEES ON LINKEDIN for "+site+"...\n")
#         google_it (site,"site:linkedin.com employees "+site+"")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))

#         print (C+" [*] Finding PHPINFO Files for "+site+"...\n")
#         google_it (site,"inurl:'/phpinfo.php' "+site+"")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))

#         print (C+" [*] Finding Files containing passwords for "+site+"...\n")
#         google_it (site,"intext:'connectionString' AND inurl:'web' AND ext:'config'")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))

#         print (C+" [*] Finding .htaccess & sensitive fields for "+site+"...\n")
#         google_it (site,"inurl:'/phpinfo.php' OR inurl:'.htaccess' OR inurl:'/.git' "+site+" -github")
#         print(O+' [!] Pausing to avoid captcha...')
#         sleep(randint(20,50))
#         google_it(site, "site:"+site+" inurl:callback")
#         time.sleep(5)

#     except urllib2.HTTPError as err:
#         if err.code == 503:
#             print(R+' [-] Captcha appeared...\n')
#             pass
