#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import socket
import time
import sys
import getopt
import http.client
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module tries to determine if the target is vulnerable to Host Header Injection Attacks."
searchinfo = "Host Header Injection"
properties = {}

def hostheader0x00(web):

    #print(R+'\n    ==========================================')
    #print(R+'\n     H O S T  H E A D E R   I N J E C T I O N')
    #print(R+'    ---<>----<>----<>----<>----<>----<>----<>-\n')

    from core.methods.print import pvln
    pvln("host header Injection") 
                 

    port = input(O+' [§] Enter the port to use (eg. 80) :> ')

    if port == 443:
        print(O+" [!] Using HTTPS <port 443>...")
        print(GR+' [*] Setting headers...')
        headers = {
                'User-Agent': 'The Infected Drake [@_tID] on Systems (TIDoS)',
                'Content-Type': 'application/x-www-form-urlencoded',
                }

        print(GR+' [*] Requesting response...')
        conn = http.client.HTTPSConnection(web)
        conn.request("GET", "/", "", headers)
        response = conn.getresponse()
        print(' [*] Reading the response...')
        data = response.read()

        print(O+' [!] Response : '+GR, response.status, response.reason)
        print(O+' [!] Data (raw) : \n'+GR)
        print(data + '\n')
        save_data(database, module, lvl1, lvl2, lvl3, name, str(data))

    else:
        print(GR+' [*] Setting buffers...')
        buffer1 = "TRACE / HTTP/1.1"
        buffer2 = "Test: <script>alert(tID)</script>"
        buffer3 = "Host: " + web
        buffer4 = "GET / HTTP/1.1"

        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(GR+' [*] Making the connection...')
        result=s.connect_ex((web,int(port)))
        s.settimeout(1.0)

        if result == 0:

            print(C+' [*] Setting injection frame buffers...')
            frame_inject = "codesploit"
            buffer1 = "GET / HTTP/1.1"
            print(B+' [+] Buffer Set : '+C+buffer1)
            buffer2 = "Host: teamcodesploit.gq"
            print(B+' [+] Buffer Set : '+C+buffer2)
            time.sleep(0.5)
            print(GR+' [+] Sending buffers...')
            s.send(buffer1 + "\n")
            s.send(buffer2 + "\n\n")
            print(O+' [!] Receiving response...')
            data1 = s.recv(1024)
            s.close()
            time.sleep(0.7)
            print(GR+' [+] Analysing results...')
            if frame_inject.lower() in data1.lower():
                print(G+' [+] Site is vulnerable to Host Header Injection.')
                save_data(database, module, lvl1, lvl2, lvl3, name, "Site is vulnerable to Host Header Injection!")
            else:
                print(R+' [-] Site is immune against Host Header Injection...')
                save_data(database, module, lvl1, lvl2, lvl3, name, "Site is immune against Host Header Injection.")

            print("")
            print(GR+' [*] Obtaining header dump data...')
            print("")
            print(O+data1)
            save_data(database, module, lvl1, lvl2, lvl3, name, str(data1))
            time.sleep(1)

def hhi(web):
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
    time.sleep(0.5)
    if 'http' in web:
        web = web.replace('http://','')
        web = web.replace('https://','')

    hostheader0x00(web)

def attack(web):
    web = web.fullurl
    hhi(web)
