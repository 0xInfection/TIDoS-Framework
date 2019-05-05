#!/usr/bin/env python
from __future__ import print_function
from collections import OrderedDict
from core.Core.colors import *

def buildmenu(menu,dictionary):
    i=1
    print(ORANGE+'\n Choose from the options below :\n')
    for key, value in dictionary.items():
        print(BLUE+' ['+str(i)+'] \033[1;36m'+ '{} - '.format(key) +WHITE+'{}'.format(value[0]))
        i+=1
    if menu == 'main':
        print(BLUE+' [0] \033[1;36mSay "alvida"! (Exit TIDoS)\n')
    else:
        print(BLUE+'[A] \033[1;36mAutomate all one by one on target\n')
        print(BLUE+'[99] \033[1;36mBack')