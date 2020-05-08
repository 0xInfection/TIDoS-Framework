

import os
import platform
import socket
import time

from core.Core.colors import *
from core.methods.tor import session
from core.variables import interface


request = session()
mac_address = os.popen("cat /sys/class/net/{}/address".format(interface)).read().strip()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('google.com', 0))
localaddr = s.getsockname()[0].strip()  # local subnet
ipaddr = request.get('http://ip.42.pl/raw').text.strip()
def_gw_device = os.popen("route | grep '^default' | grep -o '[^ ]*$'").read().strip()


def info():
    print()
    #print("\n" + O + "                     +======================================================+" + color.END)
    #print("" + GR + "                             +------------------------------------+")
    time.sleep(0.1)
    print("  |:  " + O + "Mac Address:" + C + color.TR3 +C + G + mac_address + C + color.TR2 + C)
    #print("                               |:  " + O + "Mac Address:" + C + color.TR3 +C + G + mac_address + C + color.TR2 + C)
    # time.sleep (0.1)
    #print("" + GR + "                             +------------------------------------+")
    time.sleep(0.1)
    print("  |:  " + O  + "Local address:" + C + color.TR3 +C + G + localaddr + C + color.TR2 + C)
    # time.sleep (0.1)
    #print("" + GR + "                             +------------------------------------+")
    time.sleep(0.1)
    print("  |:  " + O  + "IP:" + C + color.TR3 +C + G + ipaddr + C + color.TR2 + C)
    # time.sleep (0.1)
    #print("" + GR + "                             +------------------------------------+")
    time.sleep(0.1)
    print("  |:  " + O + "Operating System:" + C + color.TR3 +C + G + platform.system() + C + color.TR2 + C)
    # time.sleep (0.1)
    #print("" + GR + "                             +------------------------------------+")
    time.sleep(0.1)
    print("  |:  " + O + "Name:" + C + color.TR3 +C + G + platform.node() + C + color.TR2 + C)
    # time.sleep (0.1)
    #print("" + GR + "                             +------------------------------------+")
    time.sleep(0.1)
    print("  |:  " + O + "Interface:" + C + color.TR3 +C + G + def_gw_device + C + color.TR2 + C)
    # time.sleep (0.1)
    #print("" + GR + "                             +------------------------------------+" + color.END)
    #print("" + O + "                     +=======================================================+\n")
    print()