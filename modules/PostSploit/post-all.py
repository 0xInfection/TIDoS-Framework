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

from core.methods.select import list as modules
from core.Core.colors import R, B, C, color
import importlib as imp

info = "Launch all post exploitation modules."
searchinfo = "ALL: post"
properties = {}

modlist = modules("post",False)

def attack(web):
    for module in modlist:
        try:
            if "-all" not in module:
                mod = imp.import_module(module)
                mod.attack(web)
        except ImportError:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Failed to import module: {}".format(module))
        except Exception as e:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Module {} failed on target {}:".format(mod, web.fullurl)+"\033[0m"+ color.CURSIVE +"\n{}".format(e) + C)
             
