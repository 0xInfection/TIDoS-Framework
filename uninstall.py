import os
import sys
import shutil
import time
from time import sleep
####################################
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
   ENDC = '\033[0m'
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[1;36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan
M = '\033[1;35;32m' # magenta
#####################################
print ''
print ''
print "               \033[1;36m......................................................................................."
time.sleep(0.2)
print "               \033[1;36m......................................................................................."
time.sleep(0.2)
print "                        \033[1;36m.%%..%%..%%..%%..%%%%%%..%%..%%...%%%%...%%%%%%...%%%%...%%......%%....."
time.sleep(0.2)
print "                        \033[1;36m.%%..%%..%%%.%%....%%....%%%.%%..%%........%%....%%..%%..%%......%%....."
time.sleep(0.2)
print "                        \033[1;36m.%%..%%..%%.%%%....%%....%%.%%%...%%%%.....%%....%%%%%%..%%......%%....."
time.sleep(0.2)
print "                        \033[1;36m.%%..%%..%%..%%....%%....%%..%%......%%....%%....%%..%%..%%......%%....."
time.sleep(0.2)
print "                        \033[1;36m..%%%%...%%..%%..%%%%%%..%%..%%...%%%%.....%%....%%..%%..%%%%%%..%%%%%%."
time.sleep(0.2)
print "                \033[1;36m......................................................................................"
time.sleep(0.2)
print "                \033[1;36m......................................................................................"
time.sleep(0.2)
print ''
main = raw_input (''+T+color.BOLD+'		            Is there something wrong with me? (yes/no)  :( >  ' +color.END)
if main == "no":
    of = raw_input(''+R+color.BOLD+'               Is it that you ran into errors during installation or something? (yes/no) :> ')
    if of == 'no':
	print ''
        print (''+O+ color.BOLD+'		   Then why do you wanna uninstall me? :( Contact my developer if u require help...' +color.END)
	time.sleep(1)
        ohno = raw_input (''+T+ color.BOLD+'	        	Do you still want to get rid of me? (yes/no) :( > ' + color.END)
	time.sleep(0.2)
        if ohno == "yes":
	     print ''
             print (""+B+color.BOLD+"             [!] Gathering info...")
	     time.sleep(0.5)
             print (""+GR+color.BOLD+"             [*] Uninstalling...")
             time.sleep(3)
             try:
                shutil.rmtree('/opt/tidos')
                os.remove('/usr/bin/tidos')
		print ''
                print (''+R+ color.BOLD+'		     Okay I am gone :) No more to trouble you :)' + color.END)
             except:
		print ''
	   	print ""+R+color.BOLD+"                                [!] ERROR [!]  "
                print (""+G + color.BOLD+'	 TIDoS is already uninstalled or not yet installed! LOL!!! What u gonna uninstall? Dumbhead :p ' + color.END)
                sys.exit()
        else:
	     print (''+G+ color.BOLD+'			Okay! Relax I am is still there' + color.END)
	     sys.exit()
    elif of == 'yes':
	print (""+GR+"            Okay, so now this will uninstall automatically..."+color.END)
	print (""+C+"               Run the setup.py installation file and install the dependencies again from scratch"+color.END)
	time.sleep(0.8)
	print ''
	print ''
	print (""+B+color.BOLD+"             [!] Gathering info...")
	time.sleep(0.5)
	print (""+GR+color.BOLD+"             [*] Uninstalling...")
	time.sleep(3)
	print ''
	try:
           shutil.rmtree('/opt/tidos')
           os.remove('/usr/bin/tidos')
	   print ''
	   print ''+G+color.BOLD+'             [!] Installation successfully completed'
           print (''+R+ color.BOLD+'		     Goodbye, I am gone :) ' + color.END)
        except:
	   print ''
	   print ""+R+color.BOLD+"                                [!] ERROR [!]  "
           print (""+G + color.BOLD+'	 TIDoS is already uninstalled or not yet installed! LOL!!! What u gonna uninstall? Dumbhead :p ' + color.END)
           sys.exit()
elif main == "yes":
    print ''
    print (''+G+ color.BOLD+'		         Please contact my developer to report the faults :)' + color.END)
    print ''
    print ''
    time.sleep(0.6)
    print (""+B+color.BOLD+"             [!] Gathering info...")
    time.sleep(0.5)
    print (""+GR+color.BOLD+"             [*] Uninstalling...")
    time.sleep (3)
    try:
         shutil.rmtree('/opt/tidos')
         os.remove('/usr/bin/tidos')
	 print ''
         print (''+T+ color.BOLD+'		         	Goodbye, I am gone :) No more to trouble you :D' + color.END)
    except:
	 print ''
         print (color.FAIL + color.BOLD+'	     TIDoS is already uninstalled or not yet installed! LoL!!! What u gonna uninstall ? Dumbhead :p ' + color.END)
         sys.exit()
else:
    print ''
    print ""+R+color.BOLD+"                                [!] ERROR [!]  "
    print (''+T+color.BOLD+'		Your machine ran into ERRORS !!! Hence contact DarK ErroR team :)  ')
    sys.exit()
