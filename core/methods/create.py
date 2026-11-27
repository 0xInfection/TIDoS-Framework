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

import argparse
import os
import shutil
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('intype',
                   help='Installation Type',
                   metavar='ITP'
                   )
p.add_argument('user',
                   help='Unprivileged user',
                   metavar='USR'
                   )

args = p.parse_args()
print(args.intype)
if args.intype == "OPT":
    synval = Path("/opt/TIDoS/core/sessioncache/syn.val")
else:
    synval = Path("/home/{0}/TIDoS/core/sessioncache/syn.val".format(args.user))
synval.parent.mkdir(parents=True, exist_ok=True)
synval.touch(exist_ok=True)
shutil.chown(synval, user=args.user, group=args.user)
