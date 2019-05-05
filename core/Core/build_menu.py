#!/usr/bin/env python
from __future__ import print_function
from collections import OrderedDict
from core.Core.colors import *
import sys
from random import randint
from core.Exploitation.exploits import exploits
from core.Footprinting.footprint import footprint
from core.Enumeration.scanenum import scanenum
from core.Vulnlysis.vuln import vuln
from core.Auxillaries.auxil import auxil
from tidos import web
from core.Footprinting.Info_Disc.infodisc import *
from core.Footprinting.Active_Recon.activeo import *
from core.Footprinting.Passive_Recon.passiveo import *

main_functions = {
    'footprint':footprint,
    'scanenum':scanenum,
    'vuln':vuln,
    'exploits':exploits,
    'auxil':auxil
}

footprint_functions = {
    'infodisc':infodisc,
    'activeo':activeo,
    'passiveo':passiveo
}

scanenum_functions = {

}

vuln_functions = {

}

exploits_functions = {

}

auxil_functions = {

}

def buildmenu(menu,dict):
    dictionary = OrderedDict(sorted(dict.items(), key=lambda x: int(x[0]))) 
    i=1
    print(ORANGE+'\n Choose from the options below :\n')
    for key, value in dictionary.items():
        print(BLUE+' ['+str(i)+'] \033[1;36m'+ '{} - '.format(value[0]) +WHITE+'{}'.format(value[1]))
        i+=1
    print('\n')
    if menu == 'main':
        print(BLUE+' [0] \033[1;36mSay "alvida"! (Exit TIDoS)\n')
    else:
        print(BLUE+'[A] \033[1;36mAutomate all one by one on target\n')
        print(BLUE+'[99] \033[1;36mBack')

    input_dirty = raw_input(''+GRAY+' [#] \033[1;4mChoose Option\033[0m'+GRAY+' :> ' + color.END)
    choice = input_dirty.strip()
    found = False
    if choice == '0': # exit
        print(RED+'\n [-] Exiting...')
        sys.exit(0)
        

    for key, value in dictionary.items():
        if str(choice) == str(key): # select option
            if menu=='main':
                results = main_functions[value[2]](web)
            elif menu =='footprint':
                results=footprint_functions[value[2]](web)
            found = True
            break

    if found == False:
        dope = ['You high dude?', 'Sorry fam! You just typed shit']
        print(RED+' [-] ' + dope[randint(0,1)])
        pass