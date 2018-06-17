<<<<<<< HEAD
#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import sys
import platform
import os
import subprocess
import logging
import time
import scapy
import atexit
from os import path
from json import dumps, loads
from scapy.all import *
from time import sleep
from subprocess import call
sys.path.append('core/')
from impo import *
from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)

try:
	agree()
	loadstyle()
	#tid()
	banner()
	banner1()
	web = inputin()
except Exception as e:
	print R+' [-] Exception encountered!'
	print R+' [-] Exception : '+str(e)
	sys.exit(1)


def tidosmain(web):

    while True:
        try:
	    dispmenu()
	    zop = raw_input(''+GR+' [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)

	    if zop == '1':

        	print G+"\n [+] Module loaded : Reconnaissance"
        	footprintban()
		footprint(web)

	    elif zop == '2':

	        print G+'\n [+] Module loaded : Scanning & Enumeration'
    		scanenumban()
		scanenum(web)

	    elif zop == '3':

	        print G+'\n [+] Module loaded : Vulnerability Analysis'
		vulnban()
		vuln(web)

	    elif zop == '4':

	        print G+'\n [+] Module loaded : Exploits Castle'
		exploitsban()
		exploits(web)
	
        except KeyboardInterrupt:
                print R+"\n [!] " + color.UNDERLINE+ "User Interruption detected!"+color.END
                print GR+' [!] Stopping jobs...'
		time.sleep(0.4)
		print C+' [!] Goodbye, see ya!\n'
		sys.exit(0)

	#except Exception as e:
		print R+' [-] Something happened! :('
		print R+' [!] Error : '+str(e)

tidosmain(web)
=======
# coding: utf-8
#!/usr/bin/env python
import sys, platform, subprocess, socket, time, os, urllib, random, string, urllib2, getpass
from urllib2 import urlopen
from time import sleep
from getpass import getpass
from subprocess import call
sys.path.append('tidos/')
from webex import *
from banner import *
from googleSearch import *
from UDoS import *
from info import *
from piweb import *

VersionNum = "1.0.0" ####### Main for all

try:
    import scapy
    import pip
    import google
    import requests
    import argparse
except ImportError as e:
    print (color.UNDERLINE + "\033[91m" + "You don't have some modules installed! \nPlease run install.py to install this tool fully! " + color.END)
    print "Error: {}".format(e)
    print "Execute: pip install (module name)"
    if (e) == "DependencyWarning":
        os.system("sudo apt-get update")
        os.system("apt-get remove python-pip")
        os.system("easy_install pip")
    elif (e) == "Unable to locate package lib32ncurses5":
        os.system("sudo apt-get update")
        os.system("sudo apt-get install lib32ncurses5 lib32bz2-1.0")
    sys.exit()
###############################
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   HEADER = '\033[95m'
   OKBLUE = '\033[94m'
   OKGREEN = '\033[92m'
   WARNING = '\033[93m'
   FAIL = '\033[91m'
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan
M = '\033[1;35;32m' # magenta
###############################
os.system('clear')
if str(platform.system()) != "Linux":
    sys.exit(""+R+"[!] " + color.UNDERLINE + "\033[91m" + "             You are not using a Linux Based OS! Linux is a must-have for this script!" + color.END)
if not os.geteuid() == 0:
    sys.exit(""+R+"[!] " + color.UNDERLINE + "\033[91m" + "                           Must be run as root. :) " + color.END)
if 'no' in open('agree.txt').read():# take out the treaty/
    print color.BOLD + """
	TIDoS is a open-source tool developed as a royalty-free website penetration testing tool.

	I was developed by Pinaxx Robinson, known by the name @_tID aka The-Infected-Drake.

	This is to make you note that I am purely developed for Penetration Testing purposes (WhiteHat in the sense). The developer is not responsible for any damage or data loss due to my misuse. If you intend to use me for any BlackHat purposes, use it at your own risk, coz I am dangerous... ;)

	Also by using this tool, you agree to be a awesome person. Try to help others, strive not being a ScriptKiD, speak fairly to everyone, offer free hugs to everyone (provided the other person agrees in a mutual hug, don't FORCE xD), and never underestimate anyone.

	You can edit these scripts within me as per your own needs, provided you use it only for yourself. If u wanna publish me again in a reformed appearance, give the developer some credits...  :)
"""
    agree = raw_input(''+G+'' + color.UNDERLINE + 'Do you agree to these terms and conditions?>' + color.END)
    if agree == "yes":
        print (''+G+ 'Awesome !!!' + color.END)
        time.sleep(3)
        FILE = open("agree.txt","w")# take out the treaty/
        FILE.write('yes')
        FILE.close()
    elif agree == "y":
        print (''+G+ 'Awesome !!!' + color.END)
        time.sleep(3)
        FILE = open("agree.txt","w")# take out the treaty/
        FILE.write('yes')
        FILE.close()
    elif agree == "Y":
        print (''+G+ 'Awesome !!!' + color.END)
        time.sleep(3)
        FILE = open("agree.txt","w")# take out the treaty/
        FILE.write('yes')
        FILE.close()
    else:
        print (''+R+'[!] You have to agree!' + color.END)
        time.sleep(1)
        sys.exit()
os.system('clear')
banner()
def banner1():
	print""
	print color.BLUE + "                             +=============================================+"
	print color.CYAN + "                             | +-----------------------------------------+ |"
	print color.DARKCYAN + "                             | |   Author: The-Infected-Drake (@_tID)    | |".format(VersionNum)
	print color.WARNING + "                             | |             Version: v0.1.2             | |" 
	print color.PURPLE + "                             | |     Basic Version of this Framework     | |"
	print color.BLUE + "                             | |         Website Pentesting Tool         | |"
	print color.YELLOW + "                             | |         Have FUN, stay LEGAL !!!        | |"
	print color.CYAN + "                             | +-----------------------------------------+ |"
	print color.BLUE + "                             +=============================================+" + color.END

print color.BLUE + "                             +=============================================+"
time.sleep(0.3)
print color.CYAN + "                             | +-----------------------------------------+ |"
time.sleep(0.5)
print color.DARKCYAN + "                             | |   Author: The-Infected-Drake (@_tID)    | |"
time.sleep(0.5)
print color.WARNING + "                             | |             Version: v0.1.2             | |"
time.sleep(0.5)
print color.PURPLE + "                             | |     Basic Version of this Framework     | |"
time.sleep(0.5)
print color.GREEN + "                             | |         Website Pentesting Tool         | |"
time.sleep(0.5)
print color.DARKCYAN + "                             | |         Have FUN, stay LEGAL !!!        | |"
time.sleep(0.5)
print color.CYAN + "                             | +-----------------------------------------+ |"
time.sleep(0.3)
print color.BLUE + "                             +=============================================+" + color.END
time.sleep(0.5)

def tidosmain():
    while True:
        try:
            main = raw_input(''+M+'                                    ' + color.BOLD + 'TID :>  ' + color.END)
            if main == "info":
                info()
            elif main == "webex":
                webex()
            elif main == "help":
                print ""+O+"                        +==============================================================+"
                print ""+C+"                                                   ╦ ╦╔═╗╦  ╔═╗"
                print ""+C+"                                                   ╠═╣║╣ ║  ╠═╝"
                print ""+C+"                                                   ╩ ╩╚═╝╩═╝╩  "
                print ""+O+"                        +==============================================================+"
                time.sleep(0.3)
                print ""+C+"                              help "+GR+"- Displays this help message"
                time.sleep(0.3)
                print ""+P+"                              banner "+GR+"- Prints a new banner"
                time.sleep(0.3)                
                print ""+G+"                              cls "+GR+"- Clears the screen"
                time.sleep(0.3)
                print ""+T+"                              info "+GR+"- Displays information about your Network"
                time.sleep(0.3)
                print ""+C+"                              piweb "+GR+"- Pings a website"
                time.sleep(0.3)                
                print ""+G+"                              webex"+GR+" - Check whether a website exists or not"
                time.sleep(0.3)
                print ""+B+"                              gsearch"+GR+" - Search Google about a Website"
                time.sleep(0.3)
                print ""+O+"                              fl00d"+GR+" - Flood a website at the UDP level dead"
                time.sleep(0.3)		
                print ""+R+"                              exit"+GR+" - Quits this tool "
                time.sleep(0.3)
                print ""+M+"                              contact"+GR+" - Contact me for queries :)"
                time.sleep(0.3)
                print ""+O+"                        +===============================================================+"
            elif main == "fl00d":
                UDoS()
            elif main == "gsearch":
                googleSearch()
            elif main == "contact":
                print(''+O+'                   =====================================================================' + color.END)
                print(''+T+'                                      ╔═╗╔═╗╔╗╔╔╦╗╔═╗╔═╗╔╦╗  ╔╦╗╔═╗')
                time.sleep(0.3)
                print(''+T+'                                      ║  ║ ║║║║ ║ ╠═╣║   ║   ║║║║╣ ')
                time.sleep(0.3)
                print(''+T+'                                      ╚═╝╚═╝╝╚╝ ╩ ╩ ╩╚═╝ ╩   ╩ ╩╚═╝')
                time.sleep(0.3)
                print(''+O+'                   =====================================================================' + color.END)
                print(''+T+'                          ' + color.UNDERLINE + 'Facebook :>'+GR+'' + color.BOLD + ' https://www.facebook.com/pinaxx.robinson' + color.END)
                time.sleep(0.3)
                print(''+T+'                          ' + color.UNDERLINE + 'Instagram :>'+GR+'' + color.BOLD + ' @tID - www.instagram.com/the_infected_drake' + color.END)
                time.sleep(0.3)
                print(''+T+'                          ' + color.UNDERLINE + 'Email me :>'+GR+'' + color.BOLD + ' robinsonpinaxx2000@gmail.com' + color.END)
                print(''+O+'                   =====================================================================' + color.END)
            elif main == "piweb":
                piweb()
            elif main == "banner":
                print (""+C+"                                   ╔╗╔╔═╗╦ ╦  ╔╗ ╔═╗╔╗╔╔╗╔╔═╗╦═╗")
                time.sleep(0.1)
                print (""+C+"                                   ║║║║╣ ║║║  ╠╩╗╠═╣║║║║║║║╣ ╠╦╝")
                time.sleep(0.1)
                print (""+C+"                                   ╝╚╝╚═╝╚╩╝  ╚═╝╩ ╩╝╚╝╝╚╝╚═╝╩╚═")
                time.sleep(0.5)
                os.system('clear')
                banner()
                banner1()
            elif main == "cls":
                time.sleep(0.1)
                print (""+C+"                                ╔═╗╦  ╔═╗╔═╗╦═╗  ╔═╗╔═╗╦═╗╔═╗╔═╗╔╗╔")
                time.sleep(0.1)
                print (""+C+"                                ║  ║  ║╣ ╠═╣╠╦╝  ╚═╗║  ╠╦╝║╣ ║╣ ║║║")
                time.sleep(0.1)
                print (""+C+"                                ╚═╝╩═╝╚═╝╩ ╩╩╚═  ╚═╝╚═╝╩╚═╚═╝╚═╝╝╚╝")
                time.sleep(0.5)
                os.system('clear')
            elif main == "exit":
                print (''+O+'                    ============================================================' + color.END)
                print (""+C+"                                          ╔═╗ ╦ ╦╦╔╦╗")
                time.sleep(0.1)
                print (""+C+"                                          ║═╬╗║ ║║ ║")
                time.sleep(0.1) 
                print (""+C+"                                          ╚═╝╚╚═╝╩ ╩" + color.END)
                time.sleep(0.1)
                print(''+O+'                     ============================================================' + color.END)
                print (""+M+"                                         [*] \033[91m" + "Exiting..." + color.END)
                time.sleep(0.3)
                print (""+O+"                                        [*] " + "GoodBye... ^_^" + color.END)
                time.sleep(0.3)
                print(''+O+'                     ============================================================' + color.END)
                sys.exit()
            elif main == "":
                print (""+R+"                                 [!] " + color.UNDERLINE + "\033[91m" + "Enter an option properly" + color.END)
            else:
                print (""+R+"                              [!] " + color.UNDERLINE + "\033[91m" + "That is not an option! Type 'help'" + color.END)
        except KeyboardInterrupt:
                print (""+R+"                             [!] " + color.UNDERLINE + "\033[91m" + " Use 'exit' to close the tool!" + color.END)
                tidosmain()
tidosmain()
>>>>>>> 536b967491752fe81f11fa1695f432cd87cb4bdc
