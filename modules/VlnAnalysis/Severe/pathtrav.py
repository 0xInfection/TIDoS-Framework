#!/usr/bin/env python3
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import sys, os, re, inspect, subprocess, time
from core.database.database_module import save_data
from core.variables import database, vailyndir, tor, username
from core.methods.cache import targetname
from core.methods.print import summary
from core.Core.colors import O, GR, R, G, B, C, W, color, RD

info = "This module tries to find path traversal vulnerabilities on the target webpage. It is capable of in-path, as well as query attacks, and features two modes: a simple mode, recovering all possible paths, and a powerful evasion engine, attacking a specific path. Also, the user can provide cookies and his own dictionary."
searchinfo = "Advanced Path Traversal Scanning"
properties = {"DIRECTORY":["Sensitive directory. Attack target will be http://site.com/sensitive", " "], 
              "ATTACK":["Attack vector to be used (1: Query; 2: Path; 3: Cookie; 4: POST; 5: crawler-all", " "],
              "COOKIE":["File containing Authentication Cookie to be used", " "], 
              "PARAM":["Parameter to be used with QUERY", " "], 
              "POST":["POST Data to be used with POST (mark injection point with INJECT)", " "], 
              "FILE":["File to be searched for", " "], 
              "DEPTH":["Depth of lookup for the scan (int)", " "],
              "TIMEOUT":["Timeout to be used for requests (int)", " "]}

def pathtrav(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = inspect.stack()[0][3]
    global module
    module = "VulnAnalysis"
    global lvl1
    lvl1 = "Critical Vulnerabilities"
    global lvl3
    lvl3 = ""
    #global gotcha
    time.sleep(0.5)
    #print(R+'\n     ================================================')
    #print(R+'\n      P A T H   T R A V E R S A L  (Sensitive Paths)')
    #print(R+'     ---<>----<>----<>----<>----<>----<>----<>----<>-\n')

    from core.methods.print import pvln
    pvln("path traversal") 
                  
    try:
        if vailyndir == "":
            raise ValueError("Vailyn Installation directory not set (in core/doc/vailyn)")
        target = web.strip()
        attack = ""

        command = ["sudo", "-u", username, "./Vailyn"]

        if properties["DIRECTORY"][1] == " ":
            print(GR+' [!] Input the directory to be used... Final Url will be like '+O+'"http://site.com/sensitive"'+GR)
            param = input(C+' [!] Enter directory asssociated (eg. /sensitive) [Enter for None] :> ')
        elif properties["DIRECTORY"][1].lower() == "none":
            param = ""
        else:
            param = properties["DIRECTORY"][1]

        target += param.strip()
        command += ["-v", target]

        if properties["ATTACK"][1] == " ":
            attack = input("\n [!] Select Attack vector (1: Query; 2: Path; 3: Cookie; 4: POST; 5: crawler-all :> ")
        else:
            attack = properties["PARALLEL"][1]
        
        attack = attack.strip()
        if attack not in ["1", "2", "3", "4", "5"]:
            raise ValueError("Not a valid attack vector: {}".format(attack))
        command += ["-a", attack]
        
        if properties["COOKIE"][1] == " ":
            input_cookie = input("\n [§] Path to Authentication cookie file [Enter if none] :> ")
        elif properties["COOKIE"][1].lower() == "none":
            input_cookie = ""
        else:
            input_cookie = properties["COOKIE"][1]

        if input_cookie != "":
            command += ["-c", input_cookie]

        if attack == "1":
            if properties["PARAM"][1] == " ":
                param = input("\n [+] Select Query Paramter :> ")
            else:
                param = properties["PARAM"][1]

            command += ["-p", param]
        elif attack == "4":
            if properties["POST"][1] == " ":
                post = input("\n [+] Select POST Data (mark injection point with INJECT) :> ")
            else:
                post = properties["POST"][1]

            command += ["-s", post]

        if properties["FILE"][1] == " ":
            file = input(" [+] Select file to be looked for (e.g. /etc/passwd) :> ")
        else:
            file = properties["FILE"][1]
        
        command += ["-i", file]

        if properties["DEPTH"][1] == " ":
            depth = input(" [!] Set Attack depth (int) :> ")
        else:
            depth = properties["DEPTH"][1]

        command += ["-d", depth, "1", "1"]
        command += ["--nosploit"]

        if properties["TIMEOUT"][1] == " ":
            timeout = input(" [~] Set Request Timeout (enter if none) :> ")
        elif properties["TIMEOUT"][1].strip().lower() == "none":
            timeout = ""
        else:
            timeout = properties["TIMEOUT"][1]

        if timeout != "":
            command += ["-k", timeout]

        if tor:
            command += ["-t"]

        #output = ""
        #p = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, cwd=vailyndir)
        #while p.poll() is None:          
        #    out = p.stdout.readline().decode("utf-8")
        #    output += out
        subprocess.run(command, cwd=vailyndir)

        #save_data(database, module, lvl1, lvl2, lvl3, name, output)

    except KeyboardInterrupt:
        print(R+' [-] User Interruption!')
        return

    except Exception as e:
        print(R+' [-] Exception encountered during processing...')
        print(R+' [-] Error : '+str(e))

def attack(web):
    web = web.fullurl
    pathtrav(web)
