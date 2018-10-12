from __future__ import print_function
import os, io, platform, sys, socket, time
from time import sleep
from urllib2 import urlopen
#########################################
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
#########################################
mac_address = os.popen("cat /sys/class/net/eth0/address").read()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('google.com', 0))
localaddr = s.getsockname()[0] # local subnet
ipaddr = urlopen('http://ip.42.pl/raw').read()
def_gw_device = os.popen("route | grep '^default' | grep -o '[^ ]*$'").read()


def info():
    print (""+O+color.BOLD+"                          +=====================================================+")
    print (""+T+"                              _______          __    .___        _____         ")
    print (""+T+"                              \      \   _____/  |_  |   | _____/ ____\____    ")
    print (""+T+"                              /   |   \_/ __ \   __\ |   |/    \   __\/  _ \   ")
    print (""+T+"                             /    |    \  ___/|  |   |   |   |  \  | (  <_> )  ")
    print (""+T+"                             \____|__  /\___  >__|   |___|___|  /__|  \____/   ")
    print (""+T+"                                     \/     \/                \/               ")
    print (""+O+"                          +=====================================================+"+ color.END)
    print (""+GR+"                                 +------------------------------------+")
    time.sleep (0.2)
    print ("                                   |"+C+color.BOLD+"  Mac Address: " + mac_address)
    time.sleep (0.2)
    print (""+GR+"                                 +------------------------------------+")
    time.sleep (0.2)
    print ("                                   |"+R+color.BOLD+"  Local address: " + localaddr)
    time.sleep (0.2)
    print (""+GR+"                                 +------------------------------------+")
    time.sleep (0.2)
    print ("                                   |"+G+color.BOLD+"  IP: " + ipaddr)
    time.sleep (0.2)
    print (""+GR+"                                 +------------------------------------+")
    time.sleep (0.2)
    print ("                                   |"+T+color.BOLD+"  Operating System: " + platform.system())
    time.sleep (0.2)
    print (""+GR+"                                 +------------------------------------+")
    time.sleep (0.2)
    print ("                                   |"+P+color.BOLD+"  Name: " + platform.node())
    time.sleep (0.2)
    print (""+GR+"                                 +------------------------------------+")
    time.sleep (0.2)
    print ("                                   |"+O+color.BOLD+"  Interface: " + def_gw_device)
    time.sleep (0.2)
    print (""+GR+"                                 +------------------------------------+" + color.END)
    print (""+O+"                         +=======================================================+")
info()
