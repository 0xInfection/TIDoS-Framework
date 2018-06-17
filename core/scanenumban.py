#!/usr/bin/env python2

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This script is a part of TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import os
import time

def scanenumban():

    os.system('clear')
    time.sleep(0.7)
    print """
\033[1;96m  ___   _      ___   _      ___   _      ___   _      ___   _
 [(_)] |=|    [(_)] |=|    [(_)] |=|    [(_)] |=|    [(_)] |=|
  '-`  |_|     '-`  |_|     '-`  |_|     '-`  |_|     '-`  |_|
 /mmm/  \033[94m/     \033[1;96m/mmm/  \033[94m/     \033[1;96m/mmm/  \033[94m/     \033[1;96m/mmm/  \033[94m/     \033[1;96m/mmm/  \033[94m/
\033[94m       |____________|____________|____________|____________|
                             |            |            |
       S C A N          \033[1;96m ___  \033[94m\_      \033[1;96m___  \033[94m\_      \033[1;96m___  \033[94m\_
        A N D           \033[1;96m[(_)] |=|    [(_)] |=|    [(_)] |=|
  \033[1;34mE N U M E R A T E      \033[1;96m'-`  |_|     '-`  |_|     '-`  |_|
                       /mmm/        /mmm/        /mmm/

\033[1;37m                               
                  .oo             8  o   o  
                 .P 8             8      8  
                .P  8 o    o .oPYo8 o8  o8P 
               oPooo8 8    8 8    8  8   8  
              .P    8 8    8 8    8  8   8  
             .P     8 `YooP' `YooP'  8   8  
\033[1;93m    :::::::::..:::::..:.....::.....::..::..::::::::::
    :::::::::::::::::::::::::::::::::::::::::::::::::
    :::::::::::::::::::::::::::::::::::::::::::::::::

 Choose from the following options:

\033[1;34m [1] \033[1;36mRemote Server WAF Analysis (wafw00f)
\033[1;34m [2] \033[1;36mPort Scanning and Enumeration (includes several types of scans)
\033[1;34m [3] \033[1;36mInteractive Scanning with NMap (preloaded modules)
\033[1;34m [4] \033[1;36mLet loose Crawlers on the target
 
\033[1;34m [A] \033[1;36mAutomate all one by one on target

\033[1;34m [99] \033[1;36mBack

"""
