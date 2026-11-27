#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""
_____, ___
   '+ .;    
    , ;   
     .   
           
       .    
     .;.    
     .;  
      :  
      ,   
       

┌─[TIDoS]─[]
└──╼ VainlyStrain
"""

import glob
import os
import shutil
import subprocess

print('''\033[1m
   ___                     _                _       _    
  |_ _|   _ _      ___    | |_    __ _     | |     | |   
   | |   | ' \\    (_-<    |  _|  / _` |    | |     | |   
  |___|  |_||_|   /__/_   _\\__|  \\__,_|   _|_|_   _|_|_  
_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
''') 


print(" [+] Installing dependencies (1/2): Package Manager")
subprocess.run(["apt-get", "install", "-y",
                "libxml2", "nmap", "tcpdump", "libexiv2-dev", "build-essential",
                "pkg-config", "python3-pip", "python3-venv",
                "default-libmysqlclient-dev", "tor", "dnsutils",
                "traceroute", "iputils-ping"])

print(" [+] Installing dependencies (2/2): pip3")
subprocess.run(["pip3", "install", "-r", "requirements.txt"])

print(" [+] Installing TIDoS...")
os.makedirs("/opt/TIDoS", exist_ok=True)
for entry in glob.glob("../*"):            # mirror `cp -r ../*` (skips dotfiles)
    dest = os.path.join("/opt/TIDoS", os.path.basename(entry))
    if os.path.isdir(entry):
        shutil.copytree(entry, dest, dirs_exist_ok=True)
    else:
        shutil.copy2(entry, dest)
shutil.copy2("../tmp/tidos", "/usr/bin/tidos")
for root, dirs, files in os.walk("/opt/TIDoS"):
    for name in dirs + files:
        os.chmod(os.path.join(root, name), 0o755)
os.chmod("/usr/bin/tidos", 0o755)

print("Installation process complete. Run 'tidos' to launch the framework.\033[0m")
