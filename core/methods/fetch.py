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

import core.variables as varis
from core.methods.tor import session


def fetchinit(a):
    try:
        localver = varis.e_version.split("#")[0]
        s = session()
        onver = s.get("https://raw.githubusercontent.com/VainlyStrain/TIDoS-Framework/dev/core/doc/version", timeout=5).text.strip()
        localmain = localver.split("-")[0]
        localrev = localver.split("-")[1]
        locallist = localmain.split(".")
        onmain = onver.split("-")[0]
        onrev = onver.split("-")[1]
        onlist = onmain.split(".")
        uptodate = True
        for i in range(0, len(locallist)):
            if int(locallist[i]) < int(onlist[i]):
                uptodate = False
        if uptodate:
            if int(localrev) < int(onrev):
                uptodate = False
        if not uptodate:
            varis.upd = True
    except:
        pass
