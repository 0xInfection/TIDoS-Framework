#!/usr/bin/env python
from __future__ import print_function
from collections import OrderedDict
from core.Core.colors import *

def buildmenu(dictionary):
    i=1
    print(ORANGE+'\n Choose from the options below :\n')
    for key, value in dictionary.items():
        print(BLUE+' ['+str(i)+'] \033[1;36m'+ '{} - {}'.format(key, value))
        i+=1
    print(BLUE+' [99] \033[1;36mSay "alvida"! (Exit TIDoS)\n')

def menu_art(menu):

    if menu == 'main':
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
    elif menu == 'this': # add any additional menu art here
        print('this')