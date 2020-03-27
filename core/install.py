#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

import os

print('''\033[1m
   ___                     _                _       _    
  |_ _|   _ _      ___    | |_    __ _     | |     | |   
   | |   | ' \\    (_-<    |  _|  / _` |    | |     | |   
  |___|  |_||_|   /__/_   _\\__|  \\__,_|   _|_|_   _|_|_  
_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
''') 


print(" [+] Installing dependencies (1/2): Package Manager")
os.system("apt-get install libncurses5 libxml2 nmap tcpdump libexiv2-dev build-essential python3-pip libmariadbclient18 libmysqlclient-dev tor konsole")

print(" [+] Installing dependencies (2/2): pip3")
os.system("pip3 install -r requirements.txt")

print(" [+] Installing TIDoS...")
os.system('mkdir -v -p /opt/TIDoS/')
os.system('cp -r -v ../* /opt/TIDoS/')
os.system('cp -v ../tmp/tidos /usr/bin/tidos')
os.system('chmod -R 755 /opt/TIDoS/*')
os.system('chmod -v 755 /usr/bin/tidos')

print("Installation process complete. Run 'tidos' to launch the framework.\033[0m")
