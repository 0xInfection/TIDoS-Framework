#!/usr/bin/env python
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import time
from core.Core.colors import *

def dispmenu():

    print('''

\033[1;37m  .    +           \033[1;34m ______                \033[1;37m         .      .
           +. \033[1;34m / ==== \ \033[1;37m     .        + .                    .
.        .  \033[1;36m ,-~--------~-. \033[1;37m                      *         +
          \033[1;36m,^\033[1;33m ___          \033[1;36m^.\033[1;37m +        *         .    .       .
*     *   \033[1;36m / \033[1;33m.^   ^.          \033[1;36m\ \033[1;37m        .  \033[1;32m    _ | _
        \033[1;36m|  \033[1;33m|  o  !           \033[1;36m|\033[1;37m  .        \033[1;32m __  \ /--.
.       \033[1;36m|\033[1;34m_ \033[1;33m'.___.'          \033[1;34m_\033[1;36m|\033[1;37m           \033[1;32mI__/_\ /  )}\033[1;36m======>   \033[1;37m      +
        \033[1;36m| \033[1;34m"'----------------"\033[1;36m|\033[1;37m       +   \033[1;32m _[ _(\033[1;33m0\033[1;32m):  ))\033[1;36m========>
+       . \033[1;36m!                    !\033[1;37m     .     \033[1;32mI__\ / \. ]}\033[1;36m======>    \033[1;37m   .
     .  \033[1;36m \   \033[1;37mTIDoS Prober   \033[1;36m/ \033[1;37m            \033[1;32m  ~^-.--'
          \033[1;36m^.              .^ \033[1;37m           .   \033[1;32m   |   \033[1;37m    +.      *
.            \033[1;36m "-..______.,-" \033[1;37m.                    .                    *
     +           .                .   +              *       .
         \033[1;33m-=[ \033[1;31mL E T S   S T A R T\033[1;33m ]=-\033[1;37m
   +        .             '                 .            +         +
*       .            +           *        .         *     .
''')
    print(O+'\n Choose from the options below :\n')
    time.sleep(0.2)
    print(B+' [1] \033[1;36mReconnaissance & OSINT'+W+' (50 modules)')
    time.sleep(0.1)
    print(B+' [2] \033[1;36mScanning & Enumeration'+W+' (16 modules)')
    time.sleep(0.1)
    print(B+' [3] \033[1;36mVulnerability Analysis'+W+' (37 modules)')
    time.sleep(0.1)
    print(B+' [4] \033[1;36mExploitation (beta)'+W+' (1 modules)')
    time.sleep(0.1)
    print(B+' [5] \033[1;36mAuxillary Modules'+W+' (4 modules)\n')
    time.sleep(0.1)
    print(B+' [99] \033[1;36mSay "alvida"! (Exit TIDoS)\n')
    time.sleep(0.1)
