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

import importlib as imp
import os
import re
from pathlib import Path
from socket import gaierror

import texttable as table

import core.variables as vars
import core.methods.print as prnt

from core.Core.colors import R, B, C, color, O, G
from core.methods.creds import attackdrop

info = "Core methods for module handling."
searchinfo = ""
properties = {}

catlist = """
  all
  -----
  aid
  infdisc
  osint-active
  osint-passive
  post
  scan
  sploit
  vlnysis  
"""


def attack(target):
    try:
        j = imp.import_module(vars.module)
        j.attack(target)
    except ImportError:
        print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Invalid module: {}".format(vars.module))
    except KeyboardInterrupt:
        print("^C")
    except SystemExit:
        pass
    except gaierror:
        delcred = input(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Socket Error received. This may be caused by credentials. \n" +"\033[0m"+ color.CURSIVE + "Temporarily remove creds from {}?".format(target.fullurl) + C + " (enter for not) :> ")
        if delcred != "":
            newtarget = attackdrop(target)
            try:
                j.attack(newtarget)
            except KeyboardInterrupt:
                print("^C")
            except Exception as e:
                mod = vars.module.split(".")[-1]
                print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Module {} failed on target {}:".format(mod,target.fullurl)+"\033[0m"+ color.CURSIVE +"\n{}".format(e) + C)
    except Exception as e:
        mod = vars.module.split(".")[-1]
        print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Module {} failed on target {}:".format(mod,target.fullurl)+"\033[0m"+ color.CURSIVE +"\n{}".format(e) + C)


def set(mod, param, value):
    try:
        try:
            j = imp.import_module(vars.module)
            j.properties[param][1] = value
            #print("{} > {}".format(param, value))
            print(O+param+C+color.TR3+C+G+value+C+color.TR2+C)
        except ImportError:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Incorrect module: 'properties' dictionary missing.")
    except KeyError:
        print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Module {} has no property {}".format(mod, param))


def display(i, names: list, descriptions: list, values: list):
    for k in i:
        names.append(k)
        descriptions.append(i[k][0])
        values.append(i[k][1])

    t = table.Texttable()
    headings = ["Name", "Desc.", "Val"]
    t.header(headings)
    #t.set_chars(["-"," ","+","~"])
    t.set_deco(table.Texttable.BORDER)
    for row in zip(names, descriptions, values):
        t.add_row(row)
    s = t.draw()
    print(s + "\n")
    return names, descriptions, values

def listdisplay(names, descs):
    t = table.Texttable()
    headings = ["Modvle", "Desc."]
    t.header(headings)
    t.set_chars(["-","|","+","-"])
    t.set_deco(table.Texttable.HEADER)
    for row in zip(names, descs):
        t.add_row(row)
    s = t.draw()
    print("\n" + s + "\n")

def information(mod):
    names = []
    descs = []
    vals = []
    try:
        j = imp.import_module(vars.module)
        i = j.info
        print("\n\033[4m{}\033[0m\n".format(vars.module))
        print(i + "\n\n\033[4mOptions\033[0m\n")
        i = j.properties
        names, descs, vals = display(i, names, descs, vals)
        return (j.info, j.properties)
    except ImportError:
        print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Incorrect module: 'info' string missing.")


def opts(mod):
    names = []
    descs = []
    vals = []
    try:
        j = imp.import_module(vars.module)
        i = j.properties
        print("\n\033[4m{}\033[0m\n".format(vars.module))
        names, descs, vals = display(i, names, descs, vals)
    except ImportError:
        print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Incorrect module: 'properties' dictionary missing.")


def mlist(arg,display):
    return list(arg,display,single=False)

def modulecount(a):
    lst = list("all", False)
    vars.count = len(lst)

def list(arg,display,single=True):
    names = []
    descs = []
    dir = ""

    passivenames = []
    passivedescs = []
    activenames = []
    activedescs = []
    discnames = []
    discdescs = []
    scannames = []
    scandescs = []
    portnames = []
    portdescs = []
    crawlnames = []
    crawldescs = []
    misnames = []
    misdescs = []
    brutenames = []
    brutedescs = []
    severenames = []
    severedescs = []
    sploitnames = []
    sploitdescs = []
    aidnames = []
    aiddescs = []
    postnames = []
    postdescs = []

    if arg == "all":
        dir = vars.modir
    elif arg == "aid":
        dir = vars.aidir
    elif arg == "osint-passive":
        dir = vars.pasdir
    elif arg == "osint-active":
        dir = vars.acdir
    elif arg == "scan":
        dir = vars.scadir
    elif arg == "sploit":
        dir = vars.sploidir
    elif arg == "vlnysis":
        dir = vars.vlndir
    elif arg == "infdisc":
        dir = vars.infdir
    elif arg == "post":
        dir = vars.postdir
    else:
        print(catlist)
        return

    for filen in sorted(Path(dir).glob("**/*.py")):
        module1 = str(filen).split(".py")[0]
        if os.name == 'nt':
            module2 = module1.split("modules/")[-1]
        else:
            module2 = module1.split("modules/")[-1]
        module2 = module2.replace("/", ".")
        module2 = module2.replace("\\", ".")
        module2 = "modules." + module2
        try:
            if (
                    "__init__" not in module2 and "colors" not in module2 and "wafimpo" not in module2 and "DNSDumpsterAPI" not in module2 and "Form" not in module2 and "uri" not in module2 and "Crawler" not in module2 and "subdom0x00" not in module2 and "errorsql" not in module2 and "blindsql" not in module2 and "files.subdom" not in module2 and "fileo.subdom" not in module2 and "signatures" not in module2):
                j = imp.import_module(module2)
                i = j.searchinfo
                #names.append(module2.split(".")[-1])
                names.append(module2)
                descs.append(i)
                if "ActiveRecon" in module2:
                    activenames.append(module2.split(".")[-1])
                    activedescs.append(i)
                elif "PassiveRecon" in module2:
                    passivenames.append(module2.split(".")[-1])
                    passivedescs.append(i)
                elif "InfoDisclose" in module2:
                    discnames.append(module2.split(".")[-1])
                    discdescs.append(i)
                elif "ScanningEnumeration" in module2 and "0x01-PortScanning" not in module2 and "0x02-WebCrawling" not in module2:
                    scannames.append(module2.split(".")[-1])
                    scandescs.append(i)
                elif "ScanningEnumeration" in module2 and "0x01-PortScanning" in module2:
                    portnames.append(module2.split(".")[-1])
                    portdescs.append(i)
                elif "ScanningEnumeration" in module2 and "0x02-WebCrawling" in module2:
                    crawlnames.append(module2.split(".")[-1])
                    crawldescs.append(i)
                elif "PassiveRecon" in module2:
                    names.append(module2.split(".")[-1])
                    descs.append(i)
                elif "SploitLoot" in module2:
                    sploitnames.append(module2.split(".")[-1])
                    sploitdescs.append(i)
                elif "Aid" in module2:
                    aidnames.append(module2.split(".")[-1])
                    aiddescs.append(i)
                elif "VlnAnalysis.Severe" in module2:
                    severenames.append(module2.split(".")[-1])
                    severedescs.append(i)
                elif "VlnAnalysis.Other" in module2:
                    brutenames.append(module2.split(".")[-1])
                    brutedescs.append(i)
                elif "VlnAnalysis.Misconfig" in module2:
                    misnames.append(module2.split(".")[-1])
                    misdescs.append(i)
                elif "PostSploit" in module2:
                    postnames.append(module2.split(".")[-1])
                    postdescs.append(i)

        except ImportError:
            pass
    if display:
        from core.methods.print import cprint
        if len(passivenames) > 0 or len(activenames) > 0 or len(discdescs) > 0:
            prnt.posint("Phase 1")
            if len(passivenames) > 0:
                cprint("OSINT/Footprinting: ","Passive Recon")
                listdisplay(passivenames, passivedescs)
            if len(activenames) > 0:
                cprint("OSINT/Footprinting: ","Active Recon")
                listdisplay(activenames, activedescs)
            if len(discnames) > 0:
                cprint("OSINT/Footprinting: ","Information Disclosure")
                listdisplay(discnames, discdescs)
        if len(scannames) > 0 or len(portnames) > 0 or len(crawldescs) > 0:
            prnt.pscan("Phase 2")
            if len(scannames) > 0:
                cprint("Scanning/Enumeration: ","General Scanning")
                listdisplay(scannames, scandescs)
            if len(portnames) > 0:
                cprint("Scanning/Enumeration: ","Port Scanners")
                listdisplay(portnames, portdescs)
            if len(crawldescs) > 0:
                cprint("Scanning/Enumeration: ","Web Crawlers")
                listdisplay(crawlnames, crawldescs)
        if len(severenames) > 0 or len(misnames) > 0 or len(brutedescs) > 0:
            prnt.pvln("Phase 3")
            if len(misnames) > 0:
                cprint("Vulnerability Analysis: ","Misconfiguration")
                listdisplay(misnames, misdescs)
            if len(severenames) > 0:
                cprint("Vulnerability Analysis: ","Severe Issues")
                listdisplay(severenames, severedescs)
            if len(brutedescs) > 0:
                cprint("Vulnerability Analysis: ","Weak Credentials")
                listdisplay(brutenames, brutedescs)
        if len(sploitdescs) > 0:
            prnt.psploit("Phase 4")
            cprint("Exploitation: ","Exploits")
            listdisplay(sploitnames, sploitdescs)
        if len(postdescs) > 0:
            prnt.ppost("Phase 5")
            cprint("Post Exploitation: ","All")
            listdisplay(postnames, postdescs)
        if len(aidnames) > 0:
            print("\nAdditional Modules")
            listdisplay(aidnames, aiddescs)
    if single:
        return names
    else:
        return (passivenames, activenames, discnames, scannames, portnames, crawlnames, misnames, severenames, brutenames, sploitnames, aidnames, postnames)


def search(inp):
    from core.methods.print import cprint
    names = []
    descs = []

    passivenames = []
    passivedescs = []
    activenames = []
    activedescs = []
    discnames = []
    discdescs = []
    scannames = []
    scandescs = []
    portnames = []
    portdescs = []
    crawlnames = []
    crawldescs = []
    misnames = []
    misdescs = []
    brutenames = []
    brutedescs = []
    severenames = []
    severedescs = []
    sploitnames = []
    sploitdescs = []
    aidnames = []
    aiddescs = []
    postnames = []
    postdescs = []

    def filematch(id, filenames):
        patt = '.*{}.*'.format(id)
        found = []
        for filename in filenames:
            if (re.match(patt, os.path.basename(filename))):
                found.append(filename)
        return found

    filenames = []
    foundfiles = []

    idlist = inp.split(" ")
    for filen in Path(vars.modir).glob("**/*.py"):
        filenames.append(str(filen))
    for id in idlist:
        foundfiles += filematch(id, filenames)
    for filen in filenames:
        module1 = filen.split(".py")[0]
        if os.name == 'nt':
            module2 = module1.split("modules/")[-1]
        else:
            module2 = module1.split("modules/")[-1]
        module2 = module2.replace("/", ".")
        module2 = module2.replace("\\", ".")
        module2 = "modules." + module2
        # print(module2)
        try:
            if (
                    "__init__" not in module2 and "colors" not in module2 and "wafimpo" not in module2 and "DNSDumpsterAPI" not in module2 and "Form" not in module2 and "uri" not in module2 and "Crawler" not in module2 and "subdom0x00" not in module2 and "errorsql" not in module2 and "blindsql" not in module2 and "files.subdom" not in module2 and "fileo.subdom" not in module2 and "signatures" not in module2):
                module = imp.import_module(module2)
                j = module.info
                for id in idlist:
                    if id.lower() in str(j).lower():
                        if filen not in foundfiles:
                            foundfiles.append(str(filen))
        except ImportError:
            pass
    for file in foundfiles:
        if os.name == 'nt':
            list1 = file.split("\\modules\\")
        else:
            list1 = file.split("/modules/")
        if len(list1) != 2:
            print("[-] PathError. Length: {}, expected: 2".format(len(list1)))
        else:
            parsedfile = list1[1].split(".py")[0]
            parsedfile = "modules." + parsedfile
            parsedfile = parsedfile.replace("/", ".")
            parsedfile = parsedfile.replace("\\", ".")
            try:
                if (
                        "__init__" not in parsedfile and "colors" not in parsedfile and "wafimpo" not in parsedfile and "DNSDumpsterAPI" not in parsedfile and "Form" not in parsedfile and "uri" not in parsedfile and "Crawler" not in parsedfile and "subdom0x00" not in parsedfile and "errorsql" not in parsedfile and "blindsql" not in parsedfile and "files.subdom" not in parsedfile and "fileo.subdom" not in parsedfile and "signatures" not in parsedfile):
                    j = imp.import_module(parsedfile)
                    i = j.searchinfo
                    names.append(parsedfile.split(".")[-1])
                    descs.append(i)
                    if "ActiveRecon" in parsedfile:
                        activenames.append(parsedfile.split(".")[-1])
                        activedescs.append(i)
                    elif "PassiveRecon" in parsedfile:
                        passivenames.append(parsedfile.split(".")[-1])
                        passivedescs.append(i)
                    elif "InfoDisclose" in parsedfile:
                        discnames.append(parsedfile.split(".")[-1])
                        discdescs.append(i)
                    elif "ScanningEnumeration" in parsedfile and "0x01-PortScanning" not in parsedfile and "0x02-WebCrawling" not in parsedfile:
                        scannames.append(parsedfile.split(".")[-1])
                        scandescs.append(i)
                    elif "ScanningEnumeration" in parsedfile and "0x01-PortScanning" in parsedfile:
                        portnames.append(parsedfile.split(".")[-1])
                        portdescs.append(i)
                    elif "ScanningEnumeration" in parsedfile and "0x02-WebCrawling" in parsedfile:
                        crawlnames.append(parsedfile.split(".")[-1])
                        crawldescs.append(i)
                    elif "PassiveRecon" in parsedfile:
                        names.append(parsedfile.split(".")[-1])
                        descs.append(i)
                    elif "SploitLoot" in parsedfile:
                        sploitnames.append(parsedfile.split(".")[-1])
                        sploitdescs.append(i)
                    elif "Aid" in parsedfile:
                        aidnames.append(parsedfile.split(".")[-1])
                        aiddescs.append(i)
                    elif "VlnAnalysis.Severe" in parsedfile:
                        severenames.append(parsedfile.split(".")[-1])
                        severedescs.append(i)
                    elif "VlnAnalysis.Other" in parsedfile:
                        brutenames.append(parsedfile.split(".")[-1])
                        brutedescs.append(i)
                    elif "VlnAnalysis.Misconfig" in parsedfile:
                        misnames.append(parsedfile.split(".")[-1])
                        misdescs.append(i)
                    elif "PostSploit" in parsedfile:
                        postnames.append(parsedfile.split(".")[-1])
                        postdescs.append(i)
            except ImportError:
                pass

    if len(passivenames) > 0 or len(activenames) > 0 or len(discdescs) > 0:
        prnt.posint("Phase 1")
        if len(passivenames) > 0:
            cprint("OSINT/Footprinting: ","Passive Recon")
            listdisplay(passivenames, passivedescs)
        if len(activenames) > 0:
            cprint("OSINT/Footprinting: ","Active Recon")
            listdisplay(activenames, activedescs)
        if len(discnames) > 0:
            cprint("OSINT/Footprinting: ","Information Disclosure")
            listdisplay(discnames, discdescs)
    if len(scannames) > 0 or len(portnames) > 0 or len(crawldescs) > 0:
        prnt.pscan("Phase 2")
        if len(scannames) > 0:
            cprint("Scanning/Enumeration: ","General Scanning")
            listdisplay(scannames, scandescs)
        if len(portnames) > 0:
            cprint("Scanning/Enumeration: ","Port Scanners")
            listdisplay(portnames, portdescs)
        if len(crawldescs) > 0:
            cprint("Scanning/Enumeration: ","Web Crawlers")
            listdisplay(crawlnames, crawldescs)
    if len(severenames) > 0 or len(misnames) > 0 or len(brutedescs) > 0:
        prnt.pvln("Phase 3")
        if len(misnames) > 0:
            cprint("Vulnerability Analysis: ","Misconfiguration")
            listdisplay(misnames, misdescs)
        if len(severenames) > 0:
            cprint("Vulnerability Analysis: ","Severe Issues")
            listdisplay(severenames, severedescs)
        if len(brutedescs) > 0:
            cprint("Vulnerability Analysis: ","Weak Credentials")
            listdisplay(brutenames, brutedescs)
    if len(sploitdescs) > 0:
        prnt.psploit("Phase 4")
        cprint("Exploitation: ","Exploits")
        listdisplay(sploitnames, sploitdescs)
    if len(postdescs) > 0:
            prnt.ppost("Phase 5")
            cprint("Post Exploitation: ","All")
            listdisplay(postnames, postdescs)
    if len(aidnames) > 0:
        print("\nAdditional Modules")
        listdisplay(aidnames, aiddescs)

def bareimport(inp):
    success = False
    for i in vars.dlist:
        try:
            mod = imp.import_module(i+inp)
            #print(i+inp)
            success = True
            break
        except ImportError:
            pass
    return [success, i+inp]
