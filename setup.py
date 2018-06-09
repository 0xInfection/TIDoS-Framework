import os, sys, time
from time import sleep

if not os.geteuid() == 0:
    sys.exit("\033[1;31m    [!] Please run this script as root!\033[0m")

header = """
       ---------------------------------
              < \033[1;36mTIDoS Installer!!\033[1;36m >
       ---------------------------------
                      _nnnn_                      
                     dGGGGMMb     
                    @p~qp~~qMb     TIDoS Rules!!! 
                    M|@||@) M|   _;
                    @,----.JM| -'
                   JS^\__/  qKL
                  dZP        qKRb
                 dZP          qKKb
                fZP            SMMb
                HZM            MMMM
                FqM            MMMM
              __| ".        |\dS"qML
              |    `.       | `' \Zq
             _)      \.___.,|     .'
             \____   )MMMMMM|   .'
                  `-'       `--' 
"""

print header
print "\033[1;36m         Operating Systems Available:\033[1;36m "
print "\n          -------------------------------------"
print "            (1) Kali Linux / Ubuntu / Raspbian"
print "           ------------------------------------\n"

option = raw_input("\033[0m          [>] Select Operating System :> \033[0m")

if option == "1":
    print "\033[1;33m[*] Loading...\033[0m"
    os.system('apt-get install python-pip')
    os.system('easy_install pip')
    import pip
    os.system('pip install google')
    os.system('pip install requests')
    print "\033[1;33m[*] Installing...\033[0m"
    install = os.system("apt-get update && apt-get install -y build-essential libncurses5")
    install2 = os.system("cp -R tidos/ /opt/ && cp tidos.py /opt/tidos && cp runon.sh /opt/tidos && cp runon.sh /usr/bin/tidos && chmod +x /usr/bin/tidos")
    print '\033[1;33m[*] Giving permissions...\033[0m'
    os.system('chmod +x /opt/tidos/* && chmod +x /usr/bin/tidos')
    print "\033[1;32m[!] Finished Installing! Run 'tidos' to run program [!]\033[0m"
    sys.exit()
else:
    print "Whoops! Something went wrong!"
