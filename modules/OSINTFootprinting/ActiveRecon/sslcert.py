#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:#
#   TIDoS Framework    #
#-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module is a part of TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import socket
import ssl
import time
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Displays info on the website's certificate."
searchinfo = "SSL Cert Info"
properties = {}

def sslcert(web):
    name = targetname(web)
    lvl2 = "sslcert"
    module = "ReconANDOSINT"
    lvl1 = "Active Reconnaissance"
    lvl3 = ""
    if 'https' not in web:
        print(R+' [-] Website does not use SSL...')
    else:
        if str(web).split("/")[2]:
            web = str(web).split("/")[2]
        elif str(web).split("/")[3]:
            web = str(web).split("/")[2]
        cerp = []
        #print(R+'\n   =========================================')
        #print(R+'    S S L   C E R T I F I C A T E   I N F O')
        #print(R+'   =========================================\n')
        from core.methods.print import posintact
        posintact("ssl certificate info") 
        time.sleep(0.3)
        context = ssl.create_default_context()
        server = context.wrap_socket(socket.socket(), server_hostname=web)
        server.connect((web, 443))
        cer = server.getpeercert()
        cerpec = server.cipher()
        for x in cerpec:
            cerp.append(x)
        sn = str(cer.get('serialNumber'))
        vers = str(cer.get('version'))
        cs = str(cerp[0])
        proto = str(cerp[1])
        etype = str(cerp[2])
        print(B+" [+] Certificate Serial Number : "+W+ sn)
        print(B+" [+] Certificate SSL Version : "+W+ vers)
        print(B+' [+] SSL Cipher Suite : '+W+ cs)
        print(B+' [+] Encryption Protocol : '+W+ proto)
        print(B+' [+] Encryption Type : '+W+ etype + ' bit')
        print(B+' [+] Certificate as Raw : \n'+W+str(cer))
        data = "Serial Number :> {}\nVersion :> {}\nCipher Suite :> {}\n".format(sn, vers, cs) 
        data = data + "Encryption Protocol :> {}\nEncryption Type :> {}\n\n{}".format(proto, etype, str(cer))
        save_data(database, module, lvl1, lvl2, lvl3, name, data)

def attack(web):
    web = web.fullurl
    sslcert(web)