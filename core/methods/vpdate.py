#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
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

import os
import shutil
import subprocess

subprocess.run(["git", "stash"], cwd="/opt/TIDoS")
subprocess.run(["git", "pull"], cwd="/opt/TIDoS")
shutil.copy("/opt/TIDoS/tmp/TIDoS", "/bin/TIDoS")
os.chmod("/bin/TIDoS", 0o755)
