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
       

┌─[TIDoS]─[%
└──╼ VainlyStrain
"""

import importlib as imp
import os
import platform
import sys
import time
from cmd import Cmd
import argparse

import core.methods.inputin as addtarget
import core.methods.print as prnt
import core.methods.select as select
import core.variables as varis
from core.Core.colors import R, B, C, color, O, G, RD, RC
from core.methods.cache import load, save, sessionparse, createVal, targetparse
from core.methods.creds import creds
from core.methods.tor import torpipe, initcheck, session
from core.methods.parser import build_parser

"""The metasploit-like shell, binding the framework together"""
class TIDcon(Cmd):
    #design stuff
    intro = ""
    prompt = '{} tid2 > {}'.format(C, color.END)
    ruler = "--"
    doc_header = "Docvmented:"
    misc_header = "Misc.:"
    undoc_header = "NoDocs:"

    """override the default cmdloop to handle ctrl+c"""
    def cmdloop(self, intro=None):
        while True:
            try:
                super(TIDcon, self).cmdloop(intro=None)
                break
            except KeyboardInterrupt:
                if varis.module == "":
                    print("^C\n" + R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Command 'q' to end session.")
                else:
                    print("^C")

    """override the default help function to point to our help menu"""
    def do_help(self, arg):
        """List available commands with "help" or detailed help with "help cmd"."""
        if arg:
            # XXX check arg syntax
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc = getattr(self, 'do_' + arg).__doc__
                    if doc:
                        self.stdout.write("%s\n" % str(doc))
                        return
                except AttributeError:
                    pass
                self.stdout.write("%s\n" % str(self.nohelp % (arg,)))
                return
            func()
        else:
            prnt.info()

    def help_help(self):
        print("""
  help [?]
  ----------

  TIDoS help menu.
  Syntax: ? [CMD]

    CMD: command for which more detailed help should be shown.

  If CMD is omitted, a list of all commands with its function will be shown.
""")

    def do_q(self, inp) -> bool:
        return True

    def help_q(self):
        print("""
  q
  ---

  Terminate current session and quit the program.
  [!] The session is not cached, use command 'sessions' for this.
""")

    """
    help loading VAL sessions by setting options, providing terminal output 
    and the target list to the GUI if in use
    """
    def sessionhelper(self, inp, gui):
        print()
        if gui:
            victims, options = sessionparse(inp, load=False)
        else:
            victims, options = sessionparse(inp)
        for module, props in options.items():
            self.do_load(module)
            print("{}{}{}{}\n".format(C, color.UNDERLINE, module, C))
            for opt, val in props.items():
                self.do_set("{} {}".format(opt, val))
            self.do_leave("")
            print()
        if gui:
            return victims

    """
    fully automate the framework providing a VAL file with the -c argument
    supports different options for different targets, however not while using GUI (TODO)
    """
    def automator(self, inp):
        print()
        victims, options = sessionparse(inp, load=False)
        for victim in victims:
            target = targetparse(victim)
            varis.targets.append(target)
            for module, props in options.items():
                self.do_load(module)
                print("{}{}{}{}\n".format(C, color.UNDERLINE, module, C))
                for opt, val in props.items():
                    self.do_set("{} {}".format(opt, val))
                self.do_attack("")
                self.do_leave("")
                print()

    def do_sessions(self, inp, gui=False):
        if "load" in inp:
            b = varis.targets
            om = varis.module
            varis.targets = []
            victims = []
            #for i in varis.targets:
            #    varis.targets.remove(i)
            session = inp.split("load")[1].strip()
            if session == "":
                print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Syntax: sessions [load|save <SESS_ID>] [list]")
                varis.targets = b
            else:
                try:
                    if ".val" in session or "--val" in session:
                        session = session.replace("--val","").strip()
                        #print(session)
                        victims = self.sessionhelper(session, gui)
                        print(G+" [+] Restored VAL session: {}".format(session)+C+color.TR2+C)
                        if om != "":
                            self.do_load(om)
                    else:
                        load(session)
                        print(G+" [+] Restored session: {}.".format(session)+C+color.TR2+C)
                except FileNotFoundError:
                    print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "{}: no such session file.".format(session))
                    varis.targets = b
        elif "save" in inp:
            session = inp.split("save")[1].strip()
            if session == "":
                print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Syntax: sessions [load|save <SESS_ID>] [list]")
            else:
                if ".val" in session or "--val" in inp:
                    session = session.replace("--val","").strip()
                    modlist = select.list("all", False)
                    createVal(varis.targets, modlist, session)
                else:
                    save(session)
        elif "list" in inp:
            os.system("{} core/sessioncache".format(varis.CMD_LS))
        else:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Syntax: sessions [load|save <SESS_ID>] [list]")
        if gui:
            return victims


    def help_sessions(self):
        print("""
  sessions
  ----------

  Interact with cached sessions.
  Available commands:

    list     list all available sessions to load.
    load ID  restore session ID
    save ID  save current session as ID.

  Using the --val flag or .val file ending will save configured module options too.
""")

    def do_clear(self, inp):
        os.system(varis.CMD_CLEAR)

    def help_clear(self):
        print("""
  clear
  -------

  Clear the terminal using the native 'clear' or 'cls' command.
""")

    def do_tor(self, inp, shell=True):
        try:
            initv = varis.initip == ""
            acc = False
            if initv:
                try:
                    """
                    check the initial IP - will be used later to verify that Tor
                    works
                    """
                    initcheck()
                    acc = True
                except:
                    acc = False
            if "on" in inp.lower():
                #check if Tor service is running; if not, prompt user to start it
                if acc or not initv:
                    p = torpipe(True)
                    if p:
                        print(O+" [+] Tor"+C+color.TR3+C+G+"ON"+C+color.TR2+C)
                    else:
                        varis.tor = False
                        if shell:
                            start = input(color.END+" [?] Do you want to start the Tor service? (enter if not) :> ")
                        else:
                            start = "yes"
                        if start != "":
                            try:
                                os.system("systemctl start tor")
                                print(G+" [+] Tor service successfully started."+C+color.TR2+C)
                                self.do_tor("on")
                            except Exception as e:
                                print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Starting Tor service failed:"+"\033[0m"+ color.CURSIVE +"\n{}".format(e) + C)
                else:
                    print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Starting Tor service failed: Initial IP not set."+"\033[0m" + C)
            elif "off" in inp.lower():
                torpipe(False)
                if shell:
                    stop = input(color.END+" [?] Do you want to stop the Tor service? (enter if not) :> ")
                else:
                    stop = "yes"
                if stop != "":
                    try:
                        os.system("systemctl stop tor")
                        print(G+" [+] Tor service successfully stopped."+C+color.TR2+C)
                    except Exception as e:
                        print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Stopping Tor service failed:"+"\033[0m"+ color.CURSIVE +"\n{}".format(e) + C)
                print(O+" [+] Tor"+C+color.TR3+C+G+"OFF"+C+color.TR2+C)
            else:
                print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Syntax: tor on|off")
        except:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Tor connection failed: IPcheck service not available.")

    def help_tor(self):
        print("""
  tor
  -----

  Pipe attacks over the Tor Anonymity Network.
  Syntax:

    tor on|off
""")

    def do_netinfo(self, inp):
        try:
            import core.methods.netinfo as netinfo
            netinfo.info()
        except Exception as e:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Something went wrong: {}".format(e))

    def help_netinfo(self):
        print("""
  netinfo
  ---------

  Provides current network information, such as

    + your local IP
    + your public IP
    + your MAC address
""")

    def do_creds(self, inp):
        creds(inp)
        
    def help_creds(self):
        print("""
  creds
  -------

  Add or remove credentials from a specific target.
  Syntax: creds add|del target

    target: the URL which shall be operated on

  [!] the target must be formatted as in viclist.
""")

    def do_find(self, inp):
        if inp == "":
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Please enter a search term.")
        else:
            select.search(inp)

    def help_find(self):
        print("""
  find
  ------

  Search a module by providing a search term.
  The command will return any module containing the term in

    + its name
    + its description
""")

    def do_list(self, inp):
        select.list(inp,True)

    def help_list(self):
        print("""
  list
  ------

  List all modules in a specified category.
  Providing no category, list will output all availbale categories.
  Available categories:

    all           all available modules
    aid           additional tools (e.g. honeypot check)
    infdisc       information disclosure modules
    osint-active  modules for active reconnaissance
    osint-passive modules for passive reconnaissance
    post          post exploitation modules
    scan          modules for scanning and enumeration
    sploit        exploits (in progress)
    vlnysis       modules useful for vulnerability analysis
""")

    def do_attack(self, inp):
        if varis.module == "":
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "No module loaded.")
            return None
        elif "arpscan" in varis.module or "shellcraft" in varis.module or "encodeall" in varis.module or "hashes" in varis.module or "imgext" in varis.module:
            select.attack("")
        elif len(varis.targets) <= 0:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "No target(s) set.")
            return None
        else:
            for i in varis.targets:
                if len(varis.targets) > 1:
                    print( "\n"+O+" [i] Target:"+C+color.TR3+C+G+i.fullurl+C+color.TR2+C+"\n")
                select.attack(i)

    def help_attack(self):
        print("""
  attack
  --------

  unleash the loaded module on the specified target(s)
  if no options have been specified

    + configured options will be applied
    + if option not set, user will be prompted for live input.
""")

    def do_vicadd(self, inp):
        if not inp:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "No target specified.")
            return
        if "--ip" in inp:
            ip = inp.replace("--ip", "").strip()
            addtarget.inputip(ip)
        elif "--net" in inp:
            net = inp.replace("--net", "").strip()
            addtarget.inputnet(net)
        else:
            addtarget.inputin(inp)

    def help_vicadd(self):
        print("""
  vicadd
  --------

  Add the specified target to the target list.
  Syntax: viacdd [--ip] [--net] TARGET

    TARGET: the target added to the list.
    
  Options:
    --ip:  specified target is an IP, rather than an URL
    --net: load all hosts in local network as targets
           Syntax: vicadd --net NRANGE/NMASK
""")

    def do_phpsploit(self, inp):
        try:
            def filecheck():
                if not os.path.exists(varis.phpsploit):
                    print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "No phpsploit installation under {}".format(varis.phpsploit) + color.END)
                    phpsplt = input(" [§] Enter path to phpsploit script :> ")
                    varis.phpsploit = phpsplt
                    filecheck()
            filecheck()
            if inp == "":
                os.system("python3 {}".format(varis.phpsploit))
            else:
                os.system("sudo -u {} python3 {}".format(inp, varis.phpsploit))
        except SystemExit:
            pass
        except Exception:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "phpsploit crashed.")

    def help_phpsploit(self):
        print("""
  phpsploit
  -----------

  Load the phpsploit post-exploitation and control framework.
  Syntax: phpsploit [user]

    user  the user who will execute phpsploit (e.g. a non-privileged user)
  
  [!] you need to change the phpsploit path in core/variables.py to point at your installation.
""")

    def do_vicdel(self, inp):
        if inp == "all":
            varis.targets = []
            print(" [+] Cleared target list.")
        else:
            old = varis.targets
            varis.targets = list(filter(lambda a: a.fullurl != inp, varis.targets))
            found = old != varis.targets
            if found:
                print(O+" [+] Deleted Target:"+C+color.TR3+C+G+inp+C+color.TR2+C)
            else:
                print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Could not find specified target: {}".format(inp))

    def do_viclist(self, inp):
        for i in varis.targets:
            print(i.fullurl)

    def help_viclist(self):
        print("""
  viclist
  ---------

  List all targets specified for attack.
""")

    def do_intro(self, inp):
        prnt.banner()
        #prnt.bannerbelownew()
        #print()

    def help_intro(self):
        print("""
  intro
  -------

  Display the intro banner.
""")

    def help_vicdel(self):
        print("""
  vicdel
  --------

  Remove a target from the list.
  Syntax: vicdel TARGET

    TARGET  target to be removed

  To delete all targets, use TARGET = all.
""")

    def emptyline(self):
        pass

    def do_set(self, inp):
        listed = inp.split(" ")
        if len(listed) != 2:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Entry must contain exactly 1 space.")
        else:
            param = listed[0]
            value = listed[1]
            if varis.module != "":
                select.set(varis.module, param, value)
            else:
                print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "No module loaded.")

    def help_set(self):
        print("""
  set
  -----

  Set an attack option for the current module.
  Syntax: set OPT VAL

    OPT  name of the option to be modified
    VAL  value the option will take

  [!] VAL "none" for no value ("")
""")

    def do_info(self, inp, gui=False):
        if varis.module == "":
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "No module loaded.")
        else:
            info = select.information(varis.module)
            if gui:
                return info

    def help_info(self):
        print("""
  info
  ------

  Displays the description of the current module, as well as all available options.
""")

    def do_opts(self, inp):
        if varis.module == "":
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "No module loaded.")
        else:
            select.opts(varis.module)

    def help_opts(self):
        print("""
  opts
  ------

  Displays the options of the current module.
""")

    def do_load(self, inp):
        try:
            success = False
            impmod = inp
            if "modules" in impmod:
                imp.import_module(impmod)
                success = True
            else:
                p = select.bareimport(impmod)
                success = p[0]
                impmod = p[1]
                imp.import_module(impmod)
            if success:
                varis.module = impmod
                self.prompt = '{} tid2({}{}{}) > {}'.format(C, R, varis.module.split(".")[-1], C, color.END)
        except ImportError:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Not a valid module: {}".format(inp))
        except ValueError:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Please enter a module.")

    def help_load(self):
        print("""
  load
  ------

  Load a module.
  Syntax: load MODULE

    MODULE: module to be loaded

  The full path, as well as the name can be used ('.' as separator)
""")

    def do_processes(self, inp):
        try:
            p = int(inp.strip())
            assert p > 0
            print(O+" [+] Processes:"+C+color.TR3+C+G+"{} > {}".format(varis.processes, p)+C+color.TR2+C)
            varis.processes = p
        except (ValueError, AssertionError):
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Not a valid (positive) integer: {}".format(inp))

    def help_processes(self):
        print("""
  processes
  -----------

  Sets the number of processes used in parallelised mode (default=5)
  Syntax: processes INT

    INT: a strictly positive integer
""")

    def do_leave(self, inp):
        varis.module = ""
        self.prompt = '{} tid2 > {}'.format(C, color.END)

    def help_leave(self):
        print("""
  leave
  -------

  Leave the current module.
""")

    #aliases and shortcuts to exit the framework
    do_EOF = do_q
    do_quit = do_q
    do_exit = do_q
    help_quit = help_q
    help_exit = help_q

    def do_fetch(self, inp, gui=False):
        try:
            localver = varis.e_version.split("#")[0]
            s = session()
            onver = s.get("https://raw.githubusercontent.com/0xInfection/TIDoS-Framework/dev/core/doc/version").text.strip()
            localmain = localver.split("-")[0]
            localrev = localver.split("-")[1]
            locallist = localmain.split(".")
            onmain = onver.split("-")[0]
            onrev = onver.split("-")[1]
            onlist = onmain.split(".")
            uptodate = True
            matches = True
            for i in range(0, len(locallist)):
                if int(locallist[i]) < int(onlist[i]):
                    uptodate = False
            for i in range(0, len(locallist)):
                if int(locallist[i]) != int(onlist[i]):
                    matches = False
            if uptodate and matches:
                if int(localrev) < int(onrev):
                    uptodate = False
            if not uptodate:
                print(" [!] An update is available! Last version is: {}, installed version is: {}.".format(onver, localver))
                if not gui:
                    d = input(" [?] Do you want to update the framework? (enter if not) :> ")
                    if d != "":
                        path = os.path.dirname(os.path.realpath(__file__))
                        if "/home/" in path:
                            user = path.split("/")[2]
                            os.system("git stash; sudo -u {} git pull".format(user))
                        else:
                            os.system("git stash ; git pull ; cp tmp/TIDoS /bin/TIDoS ; chmod +x /bin/TIDoS")
                        print(G+" [+] Update installed successfully."+C+color.TR2+C)
            else:
                print(" [+] You are running the latest version of TIDoS-framework ({}).".format(localver))
            if gui:
                return (uptodate, localver)
        except Exception:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "An error occurred fetching...")

    def help_fetch(self):
        print("""
  fetch
  -------

  Check for and install updates of the framework.
""")

# tidos shell main function

def main():
    #parse arguments
    parser = build_parser()
    opt = vars(parser.parse_args())
    args = parser.parse_args()
    os.system(varis.CMD_CLEAR)
    #currently, only Linux is supported - TODO support other OSes as well
    if str(platform.system()) != "Linux":
        sys.exit(
            R + " [!] " + color.UNDERLINE + "\033[1m" + "You are not using a Linux Based OS! Linux is a must-have for "
                                                        "this script!" + color.END)
    #some modules require root permissions to work
    if not os.geteuid() == 0:
        sys.exit(R + " [!] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Must be run as root." + B + " :)" + color.END)
    #prompt the user with the terms&conditions if not already accepted
    if 'no' in open('core/doc/choice').read():
        prnt.disclaimer()

        a1 = input(B + ' [?] Do you agree to these terms and conditions? :> ' + C)
        if a1.lower().startswith('y'):
            print(B + ' [+] That\'s awesome! Move on...')
            time.sleep(3)
            FILE = open("core/doc/choice", "w")
            FILE.write('yes')
            FILE.close()

        else:
            print(R + ' [!] ' + "\033[0m" + color.UNDERLINE + "\033[1m" + 'You have to agree!' + color.END)
            time.sleep(1)
            sys.exit(0)

    if varis.username == "":
        user = input("Enter your (unprivileged) user name [necessary for GUI] :> ")
        with open("core/doc/local","w") as localfile:
            localfile.write(user)

    if varis.vailyndir == "":
        vailyn = input("Enter Vailyn installation directory (absolute path; required for pathtrav module) :> ")
        with open("core/doc/vailyn","w") as vailynfile:
            vailynfile.write(vailyn)

    """
    handle arguments. Note that the --app argument for the GUI is handled in
    tmp/tidos (which will be executed after global installation)
    """
    if opt["load"] and opt["victim"] and not opt["help"] and not opt["list"]:
        s = TIDcon()
        if not opt["quiet"]:
            prnt.banner()
            #prnt.bannerbelownew()
        prnt.upinfo()
        if not opt["session"]:
            s.do_vicadd(args.victim)
        else:
            s.do_sessions("load {}".format(args.victim))
        s.do_load(args.load)
        if opt["tor"]:
            s.do_tor("on")
            if varis.tor:
               s.do_attack("")
               s.do_tor("off")
        else:
            s.do_attack("")
    elif opt["file"]:
        if not opt["quiet"]:
            prnt.banner()
            #prnt.bannerbelownew()
        prnt.upinfo()
        s = TIDcon()
        if opt["tor"]:
            s.do_tor("on")
            if varis.tor:
               s.automator(args.file)
               s.do_tor("off")
        else:
            s.automator(args.file)
        print("Done.")
    elif opt["help"]:
        if not opt["quiet"]:
            prnt.banner()
            #prnt.bannerbelownew()
        prnt.upinfo()
        parser.print_help()
    elif opt["list"]:
        s = TIDcon()
        if not opt["quiet"]:
            prnt.banner()
        prnt.upinfo()
        s.do_list(args.list)
    elif opt["fetch"]:
        s = TIDcon()
        s.do_fetch("")
    elif opt["victim"] and not opt["load"] or opt["load"] and not opt["victim"]:
        parser.error("'-v' and '-l' are required for CLI attack.")
    else:
        if not opt["quiet"]:
            prnt.loadstyle()
            prnt.banner()
            #prnt.bannerbelownew()
            prnt.upinfo()
        TIDcon().cmdloop()
        print(R + "[TIDoS] " + "\033[0m" + color.END + "Alvida, my chosen")
        #print(R + "[TIDoS] "+color.END+RC+prnt.randomsg()+color.END)

if __name__ == '__main__':
    main()
