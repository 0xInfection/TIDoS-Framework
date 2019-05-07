#!/usr/bin/env python
from __future__ import print_function
from collections import OrderedDict
from core.Core.colors import *
from core.Core.arts import *
import sys
import os
from random import randint
from core.Exploitation.exploits import exploits
from core.Footprinting.footprint import footprint
from core.Enumeration.scanenum import scanenum
from core.Vulnlysis.vuln import vuln
from core.Auxillaries.auxil import auxil

### Footprinting imports
sys.path.append('modules/0x01-OSINT+Footprinting/')
from core.Footprinting.Info_Disc.infodisc import *
from core.Footprinting.Active_Recon.activeo import *
from core.Footprinting.Passive_Recon.passiveo import *

sys.path.append('modules/0x01-OSINT+Footprinting/0x01-PassiveReconnaissance/')
from dnschk import *
from piweb import *
from getgeoip import *
from revip import *
from revdns import *
from getconinfo import *
from subdom import *
from googlenum import *
from links import *
from censysdom import *
from subnet import *
from hackedmail import *
from iphistory import *
from mailtodom import *
from checkuser import *
from googlegroups import *
from threatintel import *
from webarchive import *
from googledorker import *
from googleSearch import *
from whoischeckup import *
from pastebin import *
from linkedin import *

sys.path.append('modules/0x01-OSINT+Footprinting/0x02-ActiveReconnaissance/')
from piwebenum import *
from grabhead import *
from httpmethods import *
from robot import *
from apachestat import *
from dav import *
from sharedns import *
from commentssrc import *
from sslcert import *
from filebrute import *
from traceroute import *
from phpinfo import *
from cms import *
from serverdetect import *
from altsites import *

sys.path.append('modules/0x01-OSINT+Footprinting/0x03-InformationDisclosure/')
from creditcards import *
from emailext import *
from errors import *
from phone import *
from ssn import *
from internalip import *

### Scanning/Enumeration imports
sys.path.append('modules/0x02-Scanning+Enumeration/')
from nmapmain import *
from webscan import *
from bannergrab import *
from osdetect import *
from webtech import *
from waf import *
from ssltlsscan import *
from core.Core.colors import *
from core.Enumeration.scanenumban import *
from core.Enumeration.Crawling.crawlers import *
from core.Enumeration.PortScans.portscan import *

sys.path.append('modules/0x02-Scanning+Enumeration/0x01-PortScanning/')
from finscan import *
from servicedetect import *
#from nullscan import *
#from tcpack import *
from simpleport import *
from tcpconnectscan import *
from tcpstealthscan import *
#from tcpwindows import *
#from udpscan import *
from xmasscan import *

sys.path.append('modules/0x02-Scanning+Enumeration/0x02-WebCrawling/')
from crawler1 import *
from crawler2 import *
from crawler3 import *

# Vulnerability imports
from core.Vulnlysis.Misc_Bugs.webbugs import *
from core.Vulnlysis.Oth_Bugs.othbugs import *
from core.Vulnlysis.Serio_Bugs.serbugs import *
# Exploitation imports
sys.path.append('modules/0x04-Exploitation+Loot/')
from core.Exploitation.exploitsban import *
from shellshock_exp import *
# Auxillary imports
sys.path.append('modules/0x05-Auxillaries+PF6/')
from encodeall import *
from honeypot import *
from hashes import *
from imgext import *

all_functions = {
    # main functions
    'footprint':footprint,
    'scanenum':scanenum,
    'vuln':vuln,
    'exploits':exploits,
    'auxil':auxil,
    # Footprinting
    'infodisc':infodisc,
    'activeo':activeo,
    'passiveo':passiveo,
    # Scanning and enumeration
    'waf':waf,
    'portscan':portscan,
    'nmapmain':nmapmain,
    'webtech':webtech,
    'ssltlsscan':ssltlsscan,
    'osdetect':osdetect,
    'bannergrab':bannergrab,
    'webscan':webscan,
    'crawlers':crawlers,
    
    'finscan':finscan,
    'servicedetect':servicedetect,
    'simpleport':simpleport,
    'tcpconnectscan':tcpconnectscan,
    'tcpstealthscan':tcpstealthscan,
    'xmasscan':xmasscan,

    # Vulnerability
    'webbugs':webbugs,
    'serbugs':serbugs,
    'othbugs':othbugs,
    # Exploitation
    'shellshock_exp':shellshock_exp,
    # Auxillaries
    'hashes':hashes,
    'encodeall':encodeall,
    'imgext':imgext,
    'honeypot':honeypot,
    'dnschk':dnschk,
    # Footprinting sub functions
    'piweb':piweb,
    'getgeoip':getgeoip,
    'revip':revip,
    'revdns':revdns,
    'getconinfo':getconinfo,
    'subdom':subdom,
    'googlenum':googlenum,
    'links':links,
    'censysdom':censysdom,
    'subnet':subnet,
    'hackedmail':hackedmail,
    'iphistory':iphistory,
    'mailtodom':mailtodom,
    'checkuser':checkuser,
    'googlegroups':googlegroups,
    'threatintel':threatintel,
    'webarchive':webarchive,
    'googledorker':googledorker,
    'googleSearch':googleSearch,
    'whoischeckup':whoischeckup,
    'pastebin':pastebin,
    'linkedin':linkedin,
    'piwebenum':piwebenum,
    'grabhead':grabhead,
    'httpmethods':httpmethods,
    'robot':robot,
    'apachestat':apachestat,
    'dav':dav,
    'sharedns':sharedns,
    'commentssrc':commentssrc,
    'sslcert':sslcert,
    'filebrute':filebrute,
    'traceroute':traceroute,
    'phpinfo':phpinfo,
    'cms':cms,
    'serverdetect':serverdetect,
    'altsites':altsites,
    'creditcards':creditcards,
    'emailext':emailext,
    'errors':errors,
    'phone':phone,
    'ssn':ssn,
    'internalip':internalip

}

def buildmenu(target,dict,banner,art):
    #os.system('clear')
    dictionary = OrderedDict(sorted(dict.items(), key=lambda x: int(x[0]))) 
    i=1
    if len(banner)>0:
        print(BLUE+' [+] Module Selected : '+CYAN+'{}'.format(banner))
    if len(art)>0:
        print(art)
    print(ORANGE+'\n Choose from the options below :\n')
    for key, value in dictionary.items():
        print(BLUE+' ['+str(i)+'] \033[1;36m'+ '{} - '.format(value[0]) +WHITE+'{}'.format(value[1]))
        i+=1
    print('\n')
    if 'Main Menu' in banner:
        print(BLUE+' [0] \033[1;36mSay "alvida"! (Exit TIDoS)\n')
    else:
        if not 'Aux' in banner:
            print(BLUE+' [A] \033[1;36mAutomate all one by one on target\n')
        print(BLUE+' [99] \033[1;36mBack')

    input_dirty = raw_input(''+GRAY+' [#] \033[1;4mChoose Option\033[0m'+GRAY+' :> ' + color.END)
    choice = input_dirty.strip()
    found = False
    if choice == '0': # exit
        print(RED+'\n [-] Exiting...')
        sys.exit(0)
    elif choice == '99':
        os.system('clear')
    elif choice == 'A' and not 'Aux' in banner:
        for key, value in dictionary.items():
            results=all_functions[value[2]](target)
        found = True
    else:
        for key, value in dictionary.items():
            if str(choice) == str(key): # select option
                if 'Aux' in banner:
                    results=all_functions[value[2]]
                else:
                    results=all_functions[value[2]](target)
                found = True
                break

    if found == False:
        dope = ['You high dude?', 'Sorry fam! You just typed shit']
        print(RED+' [-] ' + dope[randint(0,1)])
        pass