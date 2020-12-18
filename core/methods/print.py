#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_____, ___
   '+ .;.    
    , ;.    
     . :,  
     ;'.    
      ..    
     .;.    
      .;  
       :  
       ,   
       

┌─[TIDoS]─[]
└──╼ VainlyStrain
"""

import os, re
import time
import random
from time import sleep
from datetime import datetime
from random import uniform as rflt
import threading

from core import variables as vars
#from core.methods.select import modulecount
from core.methods.fetch import fetchinit
from core.Core.colors import *


def loadstyle():
    success = False
    thread = threading.Thread(target=fetchinit, args=(1,))
    thread.start()
    os.system(vars.CMD_CLEAR)
    red_bold = R
    cursive = color.END + "\033[3m"
    reset = cursive
    loading = "Loading console.."
    swappy = "Loading console.."
    display = """





____, __{}
   + ;    
   .:,    
     '    
    .     {}<>{}  {}T I D : 2{}  {}<>{}
    + ;   {}{}{}
    ;.    
     ;
     ;
     '   
    """.format(color.END, R, color.END, RB, color.END, R, C, cursive, swappy, color.END)
    
    action = 0
    #while action < 2:
    while thread.is_alive():
        for i, char in enumerate(loading):
            if i == 0:
                swappy = "%s%s%s%s" % (red_bold, char.swapcase(), reset, loading[1:])
                #print("%s%s%s%s" % (red_bold, char.swapcase(), reset, loading[1:]))
            elif i == 1:
                old_loading = loading[0].swapcase()
                swappy = "%s%s%s%s%s" % (old_loading, red_bold, char.swapcase(), reset, loading[2:])
                #print("%s%s%s%s%s" % (old_loading, red_bold, char.swapcase(), reset, loading[2:]))
            elif i == i:
                old_loading = loading[-0:i]
                swappy = "%s%s%s%s%s" % (old_loading, red_bold, char.swapcase(), reset, loading[i + 1:])
                #print("%s%s%s%s%s" % (old_loading, red_bold, char.swapcase(), reset, loading[i + 1:]))
            display = """





____, __{}
   + ;    
   .:,    
     '    
    .     {}<>{}  {}T I D : 2{}  {}<>{}
    + ;   {}{}{}
    ;.    
     ;
     ;
     '   
            """.format(color.END, R, color.END, RB, color.END, R, C, cursive, swappy, color.END)
            print(display)
            time.sleep(0.1)
            os.system(vars.CMD_CLEAR)
        action += 1



vaile = '''{0}                      |
                      :   
                      |   
                      .   
                      .   
                      .   
____, __             .|   
   + ;               .|   
   .{1}:,                       
     '                      
    .              /      
    + ;           :,      
    ;.           /,       
   {0}  ;          /;' ;    
     ;         /;{2}|{0}  : ^  
     '      / {2}:{0}  ;.'  *   
          '/; \\           
         ./ '. \\      {2}|{0}
          '.  '-    __\\,_
         {1}   '.      {0}\\{1}`{2};{0}{1} 
              \\      {0}\\ {1}
              .\\.     {0}V{1}   
                \\.               
                 .,.      
                   .'.    
                  ''.;:     
                    .|.   
                     | .  
                     .    
                     
'''.format(color.END, color.BOLD, color.CURSIVE)

metasploit_hakcers = '''                                                 ,˛
                                              .:oDFo:.                            
                                           ./ymM0dayMmy/.                          
                                        -+dHJ5aGFyZGVyIQ==+-                    
                                    .:sm⏣~~Destroy.No.Data~~s:`                
                                 -+h2~~Maintain.No.Persistence~~h+-              
                             .:odNo2~~Above.All.Else.Do.No.Harm~~Ndo:`          
                          ./etc/shadow.0days-Data'%20OR%201=1--.No.0MN8'/.      
                       -++SecKCoin++e.AMd`       `.-://///+hbove.913.ElsMNh+-    
                      -~/.ssh/id_rsa.Des-                  `htN01UserWroteMe!-  
                      :dopeAW.No<nano>o                     :is:TЯiKC.sudo-.A:  
                      :we're.all.alike'`                     The.PFYroy.No.D7:  
                      :PLACEDRINKHERE!:                      yxp_cmdshell.Ab0:    
                      :msf>exploit -j.                       :Ns.BOB&ALICEes7:    
                      :---srwxrwx:-.`                        `MS146.52.No.Per:    
                      :<script>.Ac816/                        sENbove3101.404:    
                      :NT_AUTHORITY.Do                        `T:/shSYSTEM-.N:    
                      :09.14.2011.raid                       /STFU|wall.No.Pr:    
                      :hevnsntSurb025N.                      dNVRGOING2GIVUUP:    
                      :#OUTHOUSE-  -s:                       /corykennedyData:    
                      :$nmap -oS                              SSo.6178306Ence:    
                      :Awsm.da:                            /shMTl#beats3o.No.:    
                      :Ring0:                             `dDestRoyREXKC3ta/M:    
                      :23d:                               sSETEC.ASTRONOMYist:    
                       /-                        /yo-    .ence.N:(){ :|: & };:    
                                                 `:Shall.We.Play.A.Game?tron/    
                                                 ```-ooy.if1ghtf0r+ehUser5`    
                                               ..th3.H1V3.U2VjRFNN.jMh+.`          
                                              `MjM~~WE.ARE.se~~MMjMs              
                                               +~KANSAS.CITY's~-`                  
                                                J~HAKCERS~./.`                    
                                                .esc:wq!:`                        
                                                 +++ATH`                            '''



tidos1 = color.BOLD + """

   T H E

         ███      ▄█  ████████▄   ▄██████▄     ▄████████
     ▀█████████▄ ███  ███   ▀███ ███    ███   ███    ███ 
        ▀███▀▀██ ███▌ ███    ███ ███    ███   ███    █▀
         ███   ▀ ███▌ ███    ███ ███    ███   ███
         ███     ███▌ ███    ███ ███    ███ ▀███████████
         ███     ███  ███    ███ ███    ███          ███ 
         ███     ███  ███   ▄███ ███    ███    ▄█    ███
        ▄████▀   █▀   ████████▀   ▀██████▀   ▄████████▀

                                                 F R A M E W O R K
""" + color.END

tidos2 = """

   T H E

    _________ ___ ______        _______  
     |       |   |   _  \.--.--|       | 
     |.|   | |.  |.  |   |  |  |___|   | 
     `-|.  |-|.  |.  |    \___/ /  ___/  
       |:  | |:  |:  1    /    |:  1  \  
       |::.| |::.|::.. . /     |::.. . | 
       `---' `---`------'      `-------' 
       
                                  F R A M E W O R K
"""


tidos3 = """

____, - 
   + ;  {0}T H E{1}      ____        _______
   .:,          |   _  \.--.--|       | 
     '      |.  |.  {2}|   |  |  |___|   |
    .  `-|. |.  |.  |    \___/ /  ___/    
    + ;  |: |{1}:  |:  1    /    |:  1  \\
    ;.      |::.|::.. . /     |::{2}.. . |{1} 
     ;      `---`------'      `-------' 
     ;                           
     '                           {0}F R A M E W O R K{1}
""".format(color.CURSIVE, color.END, color.BOLD)

bannerlist = [vaile]

sp00k70b3r = """
      ___
     /   \\
    / O O \\       _ __         
   |   O   |     /// / _   _   _ _ __ 
 , |       | ,  / ` /,'o| /o| /o|\\V / 
  \\/(     )\\/  /_n_/ |_,7/_,'/_,' )/  
   | )   ( |            //  //   //    
   |(     )|      ___
   ||   | |'    ,' _/ _   _   _   /7  /7  _   /7  __ _ 
   `|   | |    _\\ `. /o|,'o|,'o| //_7/_7,'o| /o\\,'o///7
    |   | |   /___,'/_,'|_,'|_,'//\\\\//  |_,'/_,'|_(//  
    |   /-'        //        
    |_.'    
""" 

christmas = """\033[1m
               ,--.
              (:.. )
           ,--.`--'
          (:.. )'""`.
           `--/`.__,'
             f f                      .-.   .-..----..----. .----..-.  .-. 
            ,'.`.                     |  `.'  || {_  | {}  }| {}  }\\ \\/ / 
        _,-'  :  `-._                 | |\\ /| || {__ | .-. \\| .-. \\ }  {  
        `-._ .:. _,-'                 `-' ` `-'`----'`-' `-'`-' `-' `--' 
            ) :.(          .---. .-. .-..----. .-. .----..---. .-.   .-.  .--.   .----.
        _,-' .:  `-._     /  ___}| {_} || {}  }| |{ {__ {_   _}|  `.'  | / {} \\ { {__  
       '-._  .:.  _,-`    \\     }| { } || .-. \\| |.-._} } | |  | |\\ /| |/  /\\  \\.-._} }
           )  :  (         `---' `-' `-'`-' `-'`-'`----'  `-'  `-' ` `-'`-'  `-'`----' 
       _,-'..::.  `-._
       `-._  .:   _,-'
           `. : ,'
         _,-' : `-._
         `-. .:. ,-'
            \\ . /
             `v' 

"""

currentMonth = datetime.now().month
currentDay = datetime.now().day

def f00l():
    import signal
    def handler(signum, frame):
        pass
    signal.signal(signal.SIGINT, handler) 
    #add some stuff here when time has come ;)
    time.sleep(1.5)
    print("Initialising...")
    time.sleep(3)
    print("\n [*] Checking for problems...")
    time.sleep(1.7)
    print(" [+] All problems fixed. Initialising fetch phase...")
    time.sleep(1.7)
    print("\n [*] Downloading VA1NLy Rootkit:")
    time.sleep(0.1)
    items = list(range(0, 35))
    l = len(items)
    progressbar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, item in enumerate(items):
        time.sleep(0.075)
        progressbar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50, fill="=")
    
    time.sleep(0.3)
    print("\n [*] Fetching payloads (1/3):")
    time.sleep(0.1)
    items = list(range(0, 20))
    l = len(items)
    progressbar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, item in enumerate(items):
        time.sleep(0.05)
        progressbar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50, fill="=")
    
    time.sleep(0.3)
    print("\n [*] Fetching payloads (2/3):")
    time.sleep(0.1)
    items = list(range(0, 30))
    l = len(items)
    progressbar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, item in enumerate(items):
        time.sleep(0.03)
        progressbar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50, fill="=")

    time.sleep(0.3)
    print("\n [*] Fetching payloads (3/3):")
    time.sleep(0.1)
    items = list(range(0, 15))
    l = len(items)
    progressbar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, item in enumerate(items):
        time.sleep(0.05)
        progressbar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50, fill="=")

    time.sleep(0.8)
    print("\n [*] Unpacking payloads...")
    time.sleep(1.2)
    print(" [+] Done!")
    time.sleep(0.4)
    print("\n [*] Infecting /bin/bash...")
    items = list(range(0, 25))
    l = len(items)
    progressbar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, item in enumerate(items):
        time.sleep(0.025)
        progressbar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50, fill="=")
    
    print("\n [*] Infecting package managers...")
    items = list(range(0, 45))
    l = len(items)
    progressbar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, item in enumerate(items):
        time.sleep(0.05)
        progressbar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50, fill="=")
    print("\n [*] Infecting security measures...")
    items = list(range(0, 25))
    l = len(items)
    progressbar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, item in enumerate(items):
        time.sleep(0.05)
        progressbar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50, fill="=")

    time.sleep(0.5)
    print("\n [!] Congratulations! You have been pwnd. There is nothing you can do, just cry. Enjoy your stay on my new computer.\n")
    time.sleep(0.3)
    loop = True
    
    def handler(signum, frame):
        print()
        raise KeyboardInterrupt
    signal.signal(signal.SIGINT, handler)
    
    while loop:
        try:
            inp = input("ur fucked $")
        except KeyboardInterrupt:
            continue
        if inp == "exit":
            loop = False
        elif "apt" in inp or "pacman" in inp or "yum" in inp or "dnf" in inp:
            print("I fear that this won't be very useful...")
        elif "rkhunter" in inp or "rootkit" in inp or "clamav" in inp or "tripwire" in inp or "aide" in inp:
            print("{}: Error: you can't do anything, just cry.".format(inp.split(" ")[0]))
        elif "sudo" in inp or "su " in inp or inp == "su":
            print("{}: Permission denied.".format(inp.split(" ")[0]))
        else:
            os.system(inp)
            
    time.sleep(2)
    troll = """
                         lOkxxxxdddddxOO00OOkxxxxxxxxxdl:;..                         
                      .x0;      .......................;;:cokOd,                     
                     ;N;     ..'...';'.....  ................ .c0x.                  
                    cX.   .....;...       ..       ..........    .Ko                 
                   lN.      ..'   ...'..   .       ..       ..    ;W                 
                 .00.         .xXMMMMMlokOl.         .;clll;       OO.               
               'O0xc,.    .,..N0O0OO0Kkx:.lM:    ,:dNMMMWKK0d ......,O0.             
              k0c. 'kOxxxOx:'    .l0.  .;dO:     .oMo..        ....,,,cN             
             kd , dK.  co .,ldxdxo,                M;    ,o;oXx::ok ; :M.            
             K. '.M. ,dMk0kc.          ''od;       .d0l.  .',. 0    ; lM.            
             Od ; Xl',:W:  'oX0d:....   Nl coo:      OWN:..   :MX  '.;0O             
             .Xo.'';   oM0l. .M;,lxOOdc,cx .     l:oKc     .,xWXW: . OO              
               oXd..    'NKo00MN:.    oMxkkkxdlc;:ol,,;:lxKOdM'NMd  cX               
                 xK.      kO..W00WWKd:0O     .Nx.';xW:,..xX  Mo0Mx  xd               
                  ;W'      ,KxN.  .:dXMMWKOxooNKoooOMxddxKM0NMMMMd  xo               
                   ,N;       ;0x'    x0 .;okXMMMMMMMMMMMMMMMMMMXM:  xd               
                    .kO'       .oKd,lN.      M'..',WOcc0WlcMoxXO0   xd               
                      .k0;....... .ckKxl;'. .M.   .M. .Nc KK:xXl    dx               
                        .c0k:'...'...  .';codxxoodkOddxxdoc;'       oO               
                            ;x0d;'...',....                 .'.  .  :K               
                               .;dOkc. ....';;;,'...........   ''.  'W               
                                    'lOOl'       ..............     0x               
                                        .ckOOxo:,.               .lXc                
                                              .';lxkxxdoollllloxOd,     
    """
    print(troll)
    time.sleep(0.3)
    print("Happy April Fools Day! And thank you for using TIDoS. ~Vainly")

def banner():
    os.system(vars.CMD_CLEAR)
    if currentMonth == 10:
        print(sp00k70b3r)
    elif currentDay == 1 and currentMonth == 4:
        if 'no' in open('core/doc/mystery').read():
            FILE = open("core/doc/mystery", "w")
            FILE.write('yes')
            FILE.close()
            f00l()
        else:
            print(random.choice(bannerlist))
    elif currentDay in [24,25,26] and currentMonth == 12:
        print(christmas)
    else:
        print(random.choice(bannerlist))

def randomsg():
    with open("files/ms.lst","r") as msg_list:
        return random.choice(msg_list.readlines()).strip()

def bannerbelownew():
    #print("   {}tidos{}{}{}{}{}{}{}{}{}{}".format(color.END, color.END, color.TR6, color.END, RB, vars.e_version.split("#")[0],C,color.TR3,G,vars.e_version.split("#")[1],color.TR2) + C)
    #print("   {}tidconsole{}{}{}{}{}{}{}{}{}{}".format(color.END, color.END, color.TR6, color.END, RB, vars.version,C,color.TR3,G,vars.e_version.split("#")[1],color.TR2) + C)
    print("   {}tidconsole{}{}{}{}{}{}{}{}{}{}".format(color.END, color.END, color.TR6, color.END, RB, vars.version,C,color.TR3,G,vars.count,color.TR2) + C)
    print("  {}{}{}".format(RC, randomsg(), color.END))


def info():
  print('''{}  {}                                                    {}  {}
 !  attack    Attack specified target(s)              M
 :  clear     Clear terminal.                         :
 V  creds     Handle target credentials.              
 :  fetch     Check for and install updates.          :
 :  find      Search a module.                        :
    help      Show help message.                      :
    info      Show description of current module.     M
 :  intro     Display Intro.                          :
 :  leave     Leave module.                           M
    list      List all modules of a category.         :
 :  load      Load module.                            :
 :  netinfo   Show network information.               :
 :  opts      Show options of current module.         M
    phpsploit Load the phpsploit framework.           :
              (needs to be downloaded externally)
 :  processes Set number of processes in parallelis.  :
    q         Terminate TIDoS session.                :
 :  sessions  Interact with cached sessions.          :
 :  set       Set option value of module.             M
 :  tor       Pipe Attacks through the Tor Network.   :
    vicadd    Add Target to list.                     :
    vicdel    Delete Target from list.                :
    viclist   List all targets.                       :

  {}Avail. Cmds{}
    {}M{} needs loaded modvle
    {}V [! potentially]{} need loaded target(s)
'''.format(color.UNDERLINE, color.END, color.UNDERLINE, color.END, color.UNDERLINE, color.END, color.BOLD, color.END, color.BOLD, color.END,))


def disclaimer():
    print("""
DISCLAIMER
----------

TIDoS Attack was provided as an open-source, royalty-free penetration testing toolkit. It has capable modules in various phases which can unveil potential dangerous flaws in various web-applications which can further be exploited maliciously. Therefore the author as well as the contrbutors assume no liability for misuseof this toolkit. Usage of TIDoS Attack for testing or exploiting websites without prior mutual consent can be considered as an illegal activity. It is the final user's responsibility to obey all applicable local, state and federal laws.  
            """)

def title(mod):
    return " ".join(mod[i].upper() for i in range(0, len(mod)))

def posintpas(mod):
    print("""
   ,_       
 ,'  `\\,_   
 |_,-'_)    
 /##c '\\  (   {}O S I N T   P A S S I V E{}
' |'  -{{.  )
  /\\__-' \\[]        {}{}{}
 /`-_`\\     
 '     \\    
""".format(color.END, C, RC, title(mod), C))

def posint(mod):
    print("""
   ,_       
 ,'  `\\,_   
 |_,-'_)    
 /##c '\\  (   {}O S I N T{}
' |'  -{{.  )
  /\\__-' \\[]        {}{}{}
 /`-_`\\     
 '     \\    
""".format(color.END, C, RC, title(mod), C))

def posintact(mod):
    print("""
   ,_       
 ,'  `\\,_   
 |_,-'_)    
 /##c '\\  (   {}O S I N T   A C T I V E{}
' |'  -{{.  )
  /\\__-' \\[]        {}{}{}
 /`-_`\\     
 '     \\    
""".format(color.END, C, RC, title(mod), C))

def psploit(mod):
    print("""
      ,--.!,
   __/   -*-    {}S P L O I T{}
 ,d08b.  '|`
 0088MM     {}{}{}
 `9MMP'  
""".format(color.END, C, RC, title(mod), C))

def ppost(mod):
    print("""
       /\\
      /  \\
     /    \\   {}P O S T{}
    /      \\
   /        \\   {}S P L O I T {}
  /          \\
 / /\\/\\  /\\/\\ \\   {}{}{}
/ /    \\/    \\ \\
\\/            \\/
""".format(color.END, C, color.END, C, RC, title(mod), C))

def pvln(mod):
    print("""
   (
   '\\
  '  )       {}V L N Y S I S{}
##-------->     
  .  )       {}{}{}
   ./
   (
""".format(color.END, C, RC, title(mod), C))

def pscan(mod):
    print("""
       /\\
      /  \\
     /    \\   {}S C A N N I N G   &{}
    /      \\
   /        \\   {}E N U M E R A T I O N{}
  /          \\
 / /\\/\\  /\\/\\ \\   {}{}{}
/ /    \\/    \\ \\
\\/            \\/
""".format(color.END, C, color.END, C, RC, title(mod), C))

def pbrute(mod):
    print("""
 .--.
/.-. '----------.   {}B R U T E F O R C E{}
\\'-' .--"--""-"-'       {}{}{}
 '--'
""".format(color.END, C, RC, title(mod), C))

def pleak(mod):
    print("""
   ,_       
 ,'  `\\,_   
 |_,-'_)    
 /##c '\\  (   {}I N F D I S C{}
' |'  -{{.  )
  /\\__-' \\[]        {}{}{}
 /`-_`\\     
 '     \\ 
""".format(color.END, C, RC, title(mod), C))

def cprint(text1, text2):
    print(RC + text1 + color.END + RB + text2 + color.END)


def progressbar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "{}༛{}".format(RD, color.END) * (length - filledLength)
    #print('\r%s [%s] %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    print('\r%s ---->%s>---- %s%% %s' % (prefix, bar, C+percent+color.END, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def summary(module, msg):
    display = """





{}____, __
   + ;    
   .:,    
     '    
    .     {}<>{}  {}{}{}  {}<>{}
    + ;   {}{}{}
    ;.    
     ;
     ;
     '   
    """.format(color.END, R, color.END, RB, title(module), color.END, R, C, color.CURSIVE, msg, color.END)
    print(display)

def loadstyle2():
    for i in range(0, 31):
        rnd = rflt(0.08, 0.15)
        time.sleep(rnd) #0.055
        #base = "TIDoS {}".format(vars.r_version)
        base = "vailyn"
        if i%4 == 0:
            splitted = re.findall(".", base)
            for j in range(0, len(splitted)):
                #if j%4 == 0:
                if j == i%len(splitted):
                    splitted[j] = splitted[j].swapcase()
            disp = "".join(c for c in splitted)
            #progressbar(i, 30, fill="{}༛{}".format(color.END, color.END), length=20, suffix=" {} \\".format(disp))
            progressbar(i, 30, fill="{}༛{}".format(color.END, color.END), length=20, suffix="\\", prefix=disp+" ୰")
        elif i%4 == 1:
            splitted = re.findall(".", base)
            for j in range(0, len(splitted)):
                #if j%4 == 1:
                if j == i%len(splitted):
                    splitted[j] = splitted[j].swapcase()
            disp = "".join(c for c in splitted)
            #progressbar(i, 30, fill="{}༛{}".format(color.END, color.END), length=20, suffix=" {} |".format(disp))
            progressbar(i, 30, fill="{}༛{}".format(color.END, color.END), length=20, suffix="|", prefix=disp+" ୰")
        elif i%4 == 2:
            splitted = re.findall(".", base)
            for j in range(0, len(splitted)):
                #if j%4 == 2:
                if j == i%len(splitted):
                    splitted[j] = splitted[j].swapcase()
            disp = "".join(c for c in splitted)
            #progressbar(i, 30, fill="{}༛{}".format(color.END, color.END), length=20, suffix=" {} /".format(disp))
            progressbar(i, 30, fill="{}༛{}".format(color.END, color.END), length=20, suffix="/", prefix=disp+" ୰")
        else:
            splitted = re.findall(".", base)
            for j in range(0, len(splitted)):
                #if j%4 == 3:
                if j == i%len(splitted):
                    splitted[j] = splitted[j].swapcase()
            disp = "".join(c for c in splitted)
            #progressbar(i, 30, fill="{}༛{}".format(color.END, color.END), length=20, suffix=" {} -".format(disp))
            progressbar(i, 30, fill="{}༛{}".format(color.END, color.END), length=20, suffix="-", prefix=disp+" ୰")
    time.sleep(0.75)
    os.system("clear")

def upinfo():
    if vars.upd:
        print(" ! A new version of TIDoS is available.")

def ogprint(s1, s2):
    print(O + s1 + C + color.TR3 + C + G + s2 + C + color.TR2 + C)

def gprint(s):
    print(G+s+C+color.TR2+C)
