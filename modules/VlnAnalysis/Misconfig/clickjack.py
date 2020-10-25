#!/usr/bin/env python3
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: 0xInfection (@_tID)
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import sys, urllib.request, time
from time import sleep
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module analyses if the target is clickjackable."
searchinfo = "Clickjack Tester"
properties = {}

def clickjack(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = inspect.stack()[0][3]
    global module
    module = "VulnAnalysis"
    global lvl1
    lvl1 = "Basic Bugs & Misconfigurations"
    global lvl3
    lvl3 = ""
    #print(R+'\n      ========================')
    #print(R+'\n      C L I C K J A C K I N G')
    #print(R+'     ---<>----<>----<>----<>--\n')

    from core.methods.print import pvln
    pvln("clickjacking") 
                  
    try:
        dom = web
        print(''+C+' [*] Configuring the web address...')
        time.sleep(0.8)
        if "http" not in dom:
            dom = "http://" + dom
        print(''+GR+' [*] Checking the Web Address...')
        time.sleep(0.4)
        req = urllib.request.urlopen(dom)
        print(''+B+' [*] Requesting headers...')
        time.sleep(0.7)
        headers = req.info()
        print(''+G+'\n [*] Checking for Clickjackability...')
        time.sleep(0.5)
        if not "X-Frame-Options" in headers:

            print(''+O+' [!] The Website is clickjackable!!!')
            time.sleep(0.2)
            print(''+GR+' [*] Generating report...')
            time.sleep(0.4)
            print(''+C+' [*] POC as below... You can save it as a html file :)')
            time.sleep(0.2)
            code1 = """
                <html>
                   <head><title>Clickjack test page</title></head>
                      <body>
                         <p>Website is vulnerable to clickjacking!</p>
                         <iframe src="{}" width="1000" height="500"></iframe>
                      </body>
                </html>
            """.format(web)
            code = """
\033[1;32m<html>
   \033[1;32m<head><title>\033[1;33mClickjack test page\033[1;32m</title></head>
   \033[1;32m<body>
     \033[1;32m<p>\033[1;33mWebsite is vulnerable to clickjacking!\033[1;32m</p>
     \033[1;32m<iframe src=\033[1;36m"{}" \033[1;32mwidth="1000" height="500"></iframe>
   \033[1;32m</body>
\033[1;32m</html>
            """.format(web)
            print(code)

            time.sleep(0.3)

            w = input(""+GR+" [*] Do you want to save this? (y/n) :> ")
            if w == "y":
                print(''+B+' [!] Generating POC ...')
                time.sleep(1.0)
                web0 = web.split('//')[1]
                html_file = open("tmp/logs/"+web0+"-logs/"+web0+"-clickjack-poc.html","w+")
                html_file.write(code1)
                html_file.close()
                print('')
                print(''+G+' [+] POC successfully saved under tmp/logs/'+web0+"-logs/"+web0+'-clickjack-poc.html!')
                print('')
                save_data(database, module, lvl1, lvl2, lvl3, name, "Vulnerable! POC saved in tmp folder.")
            else:
                print(''+B+' [+] Okay :)')
                save_data(database, module, lvl1, lvl2, lvl3, name, "Vulnerable!")
        else:
            print(''+R+' [-] Website not vulnerable to clickjacking...')
            save_data(database, module, lvl1, lvl2, lvl3, name, "Not vulnerable.")

    except Exception as e:
        print(''+R+' [-] Something went wrong!')
        print(G+' [-] Error : '+str(e))

def attack(web):
    web = web.fullurl
    clickjack(web)
