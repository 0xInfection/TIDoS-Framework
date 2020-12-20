#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


try:
    from google import search
except Exception:
    from googlesearch import search
import os
import time
import urllib.request
from random import randint
from time import sleep
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Finding interesting pages using Google, like logins, open redirects or backdoors."
searchinfo = "Information Gathering with Google"
properties = {}

def googledorker(web):
    name = targetname(web)
    lvl2=inspect.stack()[0][3]
    webx = web
    if "@" in webx:
        web = web.split("@")[1]
        if "https" in webx:
            web = "https://" + web
        else:
            web = "http://" + web
    site = str(web)
    def clear_cookie():
        fo = open(".google-cookie", "w")
        fo.close()


    def google_it (site,dork,lvl2, name):
        data = []
        module = "ReconANDOSINT"
        lvl1 = "Passive Reconnaissance & OSINT"
        lvl3=''
        clear_cookie()
        for title in search(dork, stop=30):
            print(O+' [!] Site Found :>'+C+color.TR3+C+G+title+C+color.TR2+C)
            data.append(title)
            time.sleep(0.1)
        save_data(database, module, lvl1, lvl2, lvl3, name, str(data))

    try:

        #print(R+'\n   ===========================')
        #print(R+'    G O O G L E   D O R K E R')
        #print(R+'   ===========================\n')
        from core.methods.print import posintpas
        posintpas("google dorker")
        print(P+' [-] Warning! You may get a captcha if you are being too frequent...'+C)
        print(GR+' [*] Initializing google dorking...')

        print (C+" [*] Finding Login Pages for "+site+"...\n")
        google_it (site,"site:"+site+" inurl:wp- OR inurl:login OR inurl:signin OR inurl:checkin OR inurl:join",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))

        print (C+" [*] Finding Subdomains for "+site+"...\n")
        google_it (site,"site:*."+site+"",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))

        print (C+" [*] Finding Sub-subdomains for "+site+"...\n")
        google_it (site,"site:*.*."+site+"",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))

        print (C+" [*] Finding Upload/Download Pages for "+site+"...\n")
        google_it (site,"site:"+site+" inurl:wp- OR inurl:plugin OR inurl:upload OR inurl:download",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))

        print (C+" [*] Finding Backdoors for "+site+"...\n")
        google_it (site,"site:"+site+" inurl:shell OR inurl:backdoor OR inurl:wso OR inurl:cmd OR shadow OR passwd OR boot.ini OR inurl:backdoor",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))

        print (C+" [*] Finding Install / Setup files for "+site+"...\n")
        google_it (site,"site:"+site+" inurl:readme OR inurl:license OR inurl:install OR inurl:setup OR inurl:config",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))

        print (C+" [*] Finding WORDPRESS PLUGINS/UPLOADS/DOWNLOADS for "+site+"...\n")
        google_it (site,"site:"+site+" inurl:wp- OR inurl:plugin OR inurl:upload OR inurl:download",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))

        print (C+" [*] Finding OPEN REDIRECTS for "+site+"...\n")
        google_it (site,"site:"+site+" inurl:redir OR inurl:url OR inurl:redirect OR inurl:return OR inurl:src=http OR inurl:r=http",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))

        print (C+" [*] Finding FILES BY EXTENSION for "+site+"...\n")
        google_it (site,"site:"+site+" ext:cgi OR ext:php OR ext:asp OR ext:aspx OR ext:jsp OR ext:jspx OR ext:swf OR ext:fla OR ext:xml",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))

        print (C+" [*] Finding DOCUMENTS BY EXTENSION for "+site+"...\n")
        google_it (site,"site:"+site+" ext:doc OR ext:docx OR ext:csv OR ext:pdf OR ext:txt OR ext:log OR ext:bak",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))

        print (C+" [*] Finding EMPLOYEES ON LINKEDIN for "+site+"...\n")
        google_it (site,"site:linkedin.com employees "+site+"",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))

        print (C+" [*] Finding PHPINFO Files for "+site+"...\n")
        google_it (site,"inurl:'/phpinfo.php' "+site+"",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))

        print (C+" [*] Finding Files containing passwords for "+site+"...\n")
        google_it (site,"intext:'connectionString' AND inurl:'web' AND ext:'config'",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))

        print (C+" [*] Finding .htaccess & sensitive fields for "+site+"...\n")
        google_it (site,"inurl:'/phpinfo.php' OR inurl:'.htaccess' OR inurl:'/.git' "+site+" -github",lvl2, name)
        print(P+' [!] Pausing to avoid captcha...'+C)
        sleep(randint(20,50))
        google_it(site, "site:"+site+" inurl:callback",lvl2, name)
        time.sleep(5)

    except urllib.error.HTTPError as err:
        if err.code == 503:
            print(R+' [-] Captcha appeared...\n')
            pass

def attack(web):
    web = web.fullurl
    googledorker(web)
