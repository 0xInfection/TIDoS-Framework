#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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
                   \033[1;33m,-.        .      \033[1;37m   +           .                   +               
\033[1;37m           *     \033[1;33m / \  `. \033[1;31m __..-,O \033[1;37m           +         *        .
\033[1;37m       +         \033[1;33m:   \ \033[1;31m--''_..-'.'     
\033[1;37m                 \033[1;33m|    . \033[1;31m.-' `. '.\033[1;37m           +       .      .      +      +
\033[1;37m         .       \033[1;33m:     .     \033[1;31m.`.' \033[1;37m            
\033[1;37m                 \033[1;33m \     `.  \033[1;31m/  ..  \033[1;37m     .          +            +      .                  
\033[1;37m           +      \033[1;33m \      `.   \033[1;31m' \033[1;33m.  \033[1;37m         *            .
\033[1;37m                   \033[1;33m `,       `.   \  \033[1;37m                +           +                 
\033[1;37m           .       \033[1;36m,|,\033[1;33m`.        `-.\  \033[1;37m     *      .                                
\033[1;37m       +          \033[1;36m'.|| \033[1;33m ``-...__..-`  \033[1;37m                            '                
\033[1;37m               +   \033[1;36m|  |                      \033[1;37m  .          *           +             
\033[1;37m          *        \033[1;36m|__|         \033[1;37m          +           *         .                    
\033[1;37m     .             \033[1;36m/||\      \033[1;37m     .                
\033[1;37m               .  \033[1;36m//||\＼    \033[1;37m +    \033[1;33m-=[ \033[1;31mP R O B E  &  E N U M E R A T E \033[1;33m]=-\033[1;37m   
\033[1;37m        +        \033[1;36m// || \＼    \033[1;37m               +                                      
\033[1;37m             \033[1;36m __//__||__\＼_   \033[1;37m     .             .       *   .       +               
\033[1;33m ____________\033[1;36m'--------------'\033[1;33m____________________________________________     

 Choose from the following options:

\033[1;34m [1] \033[1;36mRemote Server WAF Enumeration \033[0m(Generic) (54 WAFs)
\033[1;34m [2] \033[1;36mPort Scanning and Analysis \033[0m(Several Types)
\033[1;34m [3] \033[1;36mInteractive Scanning with NMap \033[0m(16 Preloaded modules)
\033[1;34m [4] \033[1;36mWeb Technologies Enumeration\033[0m(FrontEnd Technologies)
\033[1;34m [5] \033[1;36mRemote Server SSL Enumeration\033[0m(Absolute)
\033[1;34m [6] \033[1;36mOperating System Enumeration \033[0m(Absolute)
\033[1;34m [7] \033[1;36mGrab Banners on Services \033[0m(via Open Ports)
\033[1;34m [8] \033[1;36mScan all IP Addresses Linked to Domain \033[0m(CENSYS)
\033[1;34m [9] \033[1;36mLet loose Crawlers on the target \033[0m(Depth 1, 2 & 3)
 
\033[1;34m [A] \033[1;36mAutomate all one by one on target

\033[1;34m [99] \033[1;36mBack
"""
