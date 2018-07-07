#!/usr/bin/env python2

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This script is a part of TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import os
import time

def scanenumban():

    os.system('clear')
    time.sleep(0.7)
    print """
\033[1;37m  .    +           \033[1;34m ______                \033[1;37m         .      .
               +. \033[1;34m / ==== \ \033[1;37m     .        + .                    .
   .        .  \033[1;36m ,-~--------~-. \033[1;37m                      *         +
              \033[1;36m,^\033[1;33m ___          \033[1;36m^.\033[1;37m +        *         .    .       .
  *     *   \033[1;36m / \033[1;33m.^   ^.          \033[1;36m\ \033[1;37m        .  \033[1;32m    _ | _
            \033[1;36m|  \033[1;33m|  o  !           \033[1;36m|\033[1;37m  .        \033[1;32m __  \ /--.
    .       \033[1;36m|\033[1;34m_ \033[1;33m'.___.'          \033[1;34m_\033[1;36m|\033[1;37m           \033[1;32mI__/_\ /  )}\033[1;36m======    \033[1;37m      +
            \033[1;36m| \033[1;34m"'----------------"\033[1;36m|\033[1;37m       +   \033[1;32m _[ _(\033[1;33m0\033[1;32m):  ))\033[1;36m========
  +       . \033[1;36m!                    !\033[1;37m     .     \033[1;32mI__\ / \. ]}\033[1;36m======    \033[1;37m   .
         .  \033[1;36m \   \033[1;37mTIDoS Prober   \033[1;36m/ \033[1;37m            \033[1;32m  ~^-.--'
              \033[1;36m^.              .^ \033[1;37m           .   \033[1;32m   |   \033[1;37m    +.      *
  .            \033[1;36m "-..______.,-" \033[1;37m.                    .                    *
         +           .                .   +              *       .     
             \033[1;33m-=[ \033[1;31mP R O B E  &  E N U M E R A T E \033[1;33m]=-\033[1;37m
       +        .             '                 .            +         +
   *       .            +           *        .         *     .

 Choose from the following options:

\033[1;34m [1] \033[1;36mRemote Server WAF Enumeration
\033[1;34m [2] \033[1;36mPort Scanning and Analysis \033[0m(several types of scans)
\033[1;34m [3] \033[1;36mInteractive Scanning with NMap \033[0m(preloaded modules)
\033[1;34m [4] \033[1;36mFingerprint Web Technologies \033[0m(front-end) 
\033[1;34m [5] \033[1;36mGrab Banners on Services \033[0m(via Open Ports)
\033[1;34m [6] \033[1;36mLet loose Crawlers on the target \033[0m(Depth 1 & 2)
 
\033[1;34m [A] \033[1;36mAutomate all one by one on target

\033[1;34m [99] \033[1;36mBack

"""
