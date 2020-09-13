#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_____, ___
   '+ .;.    
    , ;.    
     . :,  
     ;'.    
      ..    
     .;.    
      .;  
       :  
       ,   
       

┌─[TIDoS]─[]
└──╼ VainlyStrain
"""

import os, sys, multiprocessing

global modir
global sploidir
global aidir
global pasdir
global acdir
global vlndir
global scadir
global infdir
global postdir
global phpsploit

global ai
global op
global oa
global od
global sc
global sc1
global sc2
global sp
global vam
global vao
global vas
global po

global dlist
global interface

version = "2.0"
r_version = ""
with open("core/doc/version", "r") as versionfile:
    r_version = versionfile.read().strip()
e_version = r_version + "#lsp"
module = ""
targets = []
processes = multiprocessing.cpu_count()
interface = "wlp4s0"
tor = False
initip = ""

#to avoid permission denied with gui, set to your unprivileged account
username=""
with open("core/doc/local", "r") as localfile:
    username = localfile.read().strip()

modir = os.path.dirname(os.path.realpath(__file__)) + "/../modules/"
sploidir = os.path.dirname(os.path.realpath(__file__)) + "/../modules/SploitLoot/"
scadir = os.path.dirname(os.path.realpath(__file__)) + "/../modules/ScanningEnumeration/"
pasdir = os.path.dirname(os.path.realpath(__file__)) + "/../modules/OSINTFootprinting/PassiveRecon/"
acdir = os.path.dirname(os.path.realpath(__file__)) + "/../modules/OSINTFootprinting/ActiveRecon/"
infdir = os.path.dirname(os.path.realpath(__file__)) + "/../modules/OSINTFootprinting/InfoDisclose/"
vlndir = os.path.dirname(os.path.realpath(__file__)) + "/../modules/VlnAnalysis/"
aidir = os.path.dirname(os.path.realpath(__file__)) + "/../modules/Aid/"
postdir = os.path.dirname(os.path.realpath(__file__)) + "/../modules/PostSploit/"
phpsploit = os.path.dirname(os.path.realpath(__file__)) + "/../../phpsploit/phpsploit"

ai = "modules.Aid."
op = "modules.OSINTFootprinting.PassiveRecon."
oa = "modules.OSINTFootprinting.ActiveRecon."
od = "modules.OSINTFootprinting.InfoDisclose."
sc = "modules.ScanningEnumeration."
sc1 = "modules.ScanningEnumeration.0x01-PortScanning."
sc2 = "modules.ScanningEnumeration.0x02-WebCrawling."
sp = "modules.SploitLoot."
vam = "modules.VlnAnalysis.Misconfig."
vao = "modules.VlnAnalysis.Other."
vas = "modules.VlnAnalysis.Severe."
po = "modules.PostSploit."

dlist = [ai, op, oa, od, po, sc, sc1, sc2, sp, vam, vao, vas]

CMD_CLEAR = "cls" if sys.platform.lower().startswith("win") else "clear"
CMD_LS = "dir /b" if sys.platform.lower().startswith("win") else "\\ls"


database = './core/database/tidos.db'
count = 0
upd = False

vailyndir = ""
with open("core/doc/vailyn", "r") as vailynfile:
    vailyndir = vailynfile.read().strip()
