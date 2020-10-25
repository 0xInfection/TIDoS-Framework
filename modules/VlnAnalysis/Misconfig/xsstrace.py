#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Forked from XSSTracer (to recode the entire stuff again)
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

info = "This module searches Cross Site Tracing vulnerabilities."
searchinfo = "Cross Site Tracing"
properties = {"PORT":["Port to use", " "]}

def xsstrace0x00(target):

    #print(R+'\n    =====================')
    #print(R+'\n     X S S   T R A C E R ')
    #print(R+'    ---<>----<>----<>----\n')

    from core.methods.print import pvln
    pvln("xss tracer") 
                 
    if properties["PORT"][1] == " ":
        port = input(O+' [§] Enter the port number to use (eg. 80) :> ')
    else:
        port = properties["PORT"][1]

    port = int(port)

    if port == 443:
        print(O+" [!] Using HTTPS <port 443>...")
        print(GR+' [*] Setting headers...')
        headers = {
                'User-Agent': 'The Infected Drake [@_tID] on Systems (TIDoS)',
                'Content-Type': 'application/x-www-form-urlencoded',
                }

        print(GR+' [*] Requesting response...')
        conn = http.client.HTTPSConnection(target)
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
        buffer2 = "Test: <script>alert(tID);</script>"
        buffer3 = "Host: " + target
        buffer4 = "GET / HTTP/1.1"

        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(GR+' [*] Making the connection...')
        result=s.connect_ex((target,int(port)))
        s.settimeout(1.0)

        if result == 0:

            print(O+' [*] Making requests with buffers...')
            time.sleep(0.5)
            s.send(buffer1 + "\n")
            s.send(buffer2 + "\n")
            s.send(buffer3 + "\n\n")
            data1 = s.recv(1024)
            s.close()

            script = "alert"
            xframe = "X-Frame-Options"

            if script.lower() in data1.lower():
                print(G+' [+] Site is vulnerable to Cross Site Tracing...')
                save_data(database, module, lvl1, lvl2, lvl3, name, "Site is vulnerable to Cross Site Tracing!")

            else:
                print(R+' [-] Site is immune against Cross-Site Tracing...')
                save_data(database, module, lvl1, lvl2, lvl3, name, "Site is immune against Cross-Site Tracing.")
            print("")

            print(GR+' [*] Obtaining header dump data...')
            time.sleep(1)
            print("")
            print(O+data1)
            save_data(database, module, lvl1, lvl2, lvl3, name, str(data1))
            print("")

        else:
            print(R+' [-] Exception encountered!')
            print(R+' [-] Port '+O+str(port)+' is closed!')

def xsstrace(web):
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

    xsstrace0x00(web)

def attack(web):
    web = web.fullurl
    xsstrace(web)
