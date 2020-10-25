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


import sys
import os
import subprocess
import re
import texttable as table

from core.Core.colors import R, B, C, color


info = "A simple ARP scanner to detect potential targets on your network (to then proceed with port scanning and web attacks)."
searchinfo = "ARP Network Scanner"
properties = {"IP":["IP of the network's gateway", " "], "NMASK":["Netmask of the network", " "]}

def arp():
    try:
        if properties["IP"][1] == " " or properties["NMASK"][1] == " ":
            ip = input("  [?] IP/Netmask :> ")
            if "/" not in ip:
                print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Syntax: IP/NETMASK")
                sys.exit()
        else:
            ip = properties["IP"][1] + "/" + properties["NMASK"][1]
            
        response = subprocess.check_output(['nmap','-sP','-PI','-PT', ip])
        targets = str(response).split("Nmap scan report for ")
        if len(targets) < 2:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "No targets found...")
            sys.exit()

        names = []
        macs = []
        manifs = []
        tl = targets[1:]
        for target in tl:
            pip = ip.replace(ip.split(".")[3], "")
            tip = pip + target.split(pip)[1].split(")")[0]
            names.append(tip)
            if "MAC Address" in target:
                after = target.split("MAC Address: ")[1]
                mac = after.split("(")[0]
            else:
                after = ""
                mac = "[§:AT:TA:CK:ER:§]"
            macs.append(mac)
            if "(" in after:
                manif = after.split("(")[1].split(")")[0]
            else:
                manif = "???"
            manifs.append(manif)
            
        t = table.Texttable()
        headings = ["IP", "MAC", "Manif."]
        t.header(headings)
        t.set_chars(["-","|","+","-"])
        t.set_deco(table.Texttable.HEADER)
        for row in zip(names, macs, manifs):
            t.add_row(row)
        s = t.draw()
        print("\n" + s + "\n")
        return names
    except SystemExit:
        pass
    except KeyboardInterrupt:
        print("^C")
    
def attack(web):
    from core.methods.print import pscan
    pscan("arp-scan")
    return arp()
