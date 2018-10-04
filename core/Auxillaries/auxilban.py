#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

from __future__ import print_function
from colors import *
import time
import os

def auxilban():

    os.system('clear')
    print(" [!] Module Selected : Auxillary Modules\n")
    time.sleep(0.4)
    print(C+'''
\033[1;37m
      '      .      +          .    .       '       +           '         .       .
          .                    '               +          .         *          .
                +            '                                       .        +
        .             *        .     .       .          *        .        *
             .    \033[1;33m _\033[1;37m     .     .            .       .
      .    .  \033[1;33m _  / | \033[1;37m     .        .  *        \033[1;33m _ \033[1;37m .     .    + 
              \033[1;33m| \_| | \033[1;37m           +          .   \033[1;33m| | __
           \033[1;33m _ |     |\033[1;37m       .           _       \033[1;33m| |/  |
       +   \033[1;33m| \      |     \033[1;36m _/\_        \033[1;33m| |     /  |    \  \033[1;37m +      /
           \033[1;33m|  |     \    \033[1;36m+/_\/_\+      \033[1;33m| |    /   |     \  \033[1;37m   .  |\033[1;34m
      ____\033[1;33m/____\--...\___ \033[1;36m\_||_/\033[1;34m ___...\033[1;33m|__\_\033[1;34m..\033[1;33m|____\____/\033[1;34m_______/_\033[1;34m
            .     .      \033[1;36m|_|__|_| \033[1;34m        .       .  .
         .    . .       \033[1;36m_/ /__\ \_\033[1;34m .          .            .   .
      	      .       .    .           .    .    .
         .      '                         '                    '      '
             '     \033[1;33m-=[\033[1;31m A U X I L L A R I E S \033[1;33m]=-\033[1;34m     .     '      .
       .             '       .          .       '       .
''')
    time.sleep(0.3)
    print('')
    print(B+'     [1]'+C+' Generate Hashes from Strings'+W+'(4 Types) ')
    time.sleep(0.1)
    print(B+'     [2]'+C+' Encode Payload or Strings'+W+' (7 Types)')
    time.sleep(0.1)
    print(B+'     [3]'+C+' Extract Metadata from Images'+W+' (EXIF Data)')
    time.sleep(0.1)
    print(B+'     [4]'+C+' HoneyPot Probability'+W+' (ShodanLabs HoneyScore)\n')
    time.sleep(0.1)
    print(B+'     [99]'+C+' Back\n') 

