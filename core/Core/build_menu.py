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
from tidos import web
# Footprinting imports
from core.Footprinting.Info_Disc.infodisc import *
from core.Footprinting.Active_Recon.activeo import *
from core.Footprinting.Passive_Recon.passiveo import *

# Scanning/Enumeration imports
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
    'footprint':footprint,
    'scanenum':scanenum,
    'vuln':vuln,
    'exploits':exploits,
    'auxil':auxil,
    'infodisc':infodisc,
    'activeo':activeo,
    'passiveo':passiveo,
    'waf':waf,
    'portscan':portscan,
    'nmapmain':nmapmain,
    'webtech':webtech,
    'ssltlsscan':ssltlsscan,
    'osdetect':osdetect,
    'bannergrab':bannergrab,
    'webscan':webscan,
    'crawlers':crawlers,
    'webbugs':webbugs,
    'serbugs':serbugs,
    'othbugs':othbugs,
    'shellshock_exp':shellshock_exp,
    'hashes':hashes,
    'encodeall':encodeall,
    'imgext':imgext,
    'honeypot':honeypot
}

def buildmenu(dict,banner,art):
    os.system('clear')
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
            results=all_functions[value[2]](web)
        found = True
    else:
        for key, value in dictionary.items():
            if str(choice) == str(key): # select option
                if 'Aux' in banner:
                    results=all_functions[value[2]]
                else:
                    results=all_functions[value[2]](web)
                found = True
                break

    if found == False:
        dope = ['You high dude?', 'Sorry fam! You just typed shit']
        print(RED+' [-] ' + dope[randint(0,1)])
        pass