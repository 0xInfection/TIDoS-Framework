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


import core.variables as vars
import importlib
from core.methods.select import bareimport

def load(i):
    targets = []
    with open("core/sessioncache/{}".format(i),"r") as f:
        targets = [line.rstrip("\n") for line in f]
    for vic in targets:
        vars.targets.append(vic)

    
def save(i):
    with open("core/sessioncache/{}".format(i),"w") as f:
        for vic in vars.targets:
            f.write(vic)
            f.write("\n")

def sessionparse(i, load=True):
    victims = []
    modules = {}
    oneline = ""
    with open("core/sessioncache/{}".format(i), "r") as file:
        for line in file:
            oneline += line
    vicblocks = oneline.split("<victim ")[1:]
    for block in vicblocks:
        block = block.split("</victim>")[0]
        victim = block.split(">")[0].strip()
        victims.append(victim)
        if load:
            vars.targets.append(victim)
        inter = block.replace(victim+">","")
        modblocks = inter.split("<module ")[1:]
        for modblock in modblocks:
            properties = {}
            module = modblock.split(">")[0].strip()
            modblock = modblock.split("</module>")[0]
            if ">" in modblock:
                modblock = modblock.split(">")[1]
            proplist = modblock.split(";")
            for proptuple in proplist:
                if ":" in proptuple:
                    prop = proptuple.split(":")[0].strip()
                    val = proptuple.split(":")[1].strip()
                    properties.update({prop : val})
            modules.update({module : properties})
    return (victims, modules)

def createVal(victims, modules, name):
    with open ("core/sessioncache/{}".format(name), "w") as file:
        for victim in victims:
            file.write("<victim "+victim+">\n")
            for module in modules:
                file.write("  <module "+module+">\n")
                if "modules" in module:
                    j = importlib.import_module(module)
                else:
                    p = bareimport(module)
                    md = p[1]
                    j = importlib.import_module(md)
                properties = j.properties
                for key, value in properties.items():
                    if value[1].strip() != "":
                        file.write("    {}:{};\n".format(key, value[1]))
                file.write("  </module>\n")
            file.write("</victim>\n")