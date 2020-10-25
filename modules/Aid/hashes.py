#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
import hashlib
from core.Core.colors import *

info = "This module calculates the checksum of a given message using common hash functions."
searchinfo = "Hash Calculator"
properties = {}

def hashes():

    #print(R+'\n    =============================')
    print(R+'\n     H A S H   G E N E R A T O R')
    print(R+'    ---<>----<>----<>----<>----<>\n')
    message = input(O+" [§] Enter the string :> ")
    print(GR+' [+] Generating hashes...')
    time.sleep(0.6)

    md5 = hashlib.md5(message)
    md5 = md5.hexdigest()

    sha1 = hashlib.sha1(message)
    sha1 = sha1.hexdigest()

    sha256 = hashlib.sha256(message)
    sha256 = sha256.hexdigest()

    sha512 = hashlib.sha512(message)
    sha512 = sha512.hexdigest()

    print(G+" [+] MD5 Hash : "+O, md5)
    print(G+" [+] SHA1 Hash : "+O, sha1)
    print(G+" [+] SHA256 Hash : "+O, sha256)
    print(G+" [+] SHA512 Hash : "+O, sha512)

def attack(web):
    hashes()
