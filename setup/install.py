#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import sys
import os
import time
import subprocess
from sys import stdout
from colors import *

def install():

	os.system("clear")

	time.sleep(1)
	print B+" [!] Gathering info..."
	time.sleep(1)
	print GR+" [*] Checking your resources..."
	time.sleep(1.5)

	if os.geteuid() == 0:

	    print G+" [!] No problems found."
	    print G+" [!] Checkup complete. Launching the installer..."

	else:

	    sys.exit(color.PURPLE+" [-] Run this script as ROOT !!!\033[0m")
	    sys.exit()
	time.sleep(1)

	os.system("clear")

	try:
		header = color.BOLD + """
      \033[37m---------------------------------
	     < TIDoS \033[1;36mInstaller!!\033[1;36m >
      ---------------------------------"""
		print header
		print C+"                _nnnn_"
		time.sleep(0.1)
		print C+"               dGGGGMMb"
		time.sleep(0.1)
		print C+"              @p~qp~~qMb     "+O+"TIDoS Rules!!!" 
		time.sleep(0.1)
		print C+"              M(\033[37m@\033[96m)(\033[37m@\033[96m) M|   "+GR+"_;"
		time.sleep(0.1)
		print C+"              @\033[33m,----.\033[96mJM| "+GR+"-'"
		time.sleep(0.1)
		print C+"             JS^\033[33m\__/  \033[96mqKL"
		time.sleep(0.1)
		print C+"            dZP        qKRb"
		time.sleep(0.1)
		print C+"           dZP          qKKb"
		time.sleep(0.1)
		print C+"          fZP            SMMb"
		time.sleep(0.1)
		print C+"          HZM            MMMM"
		time.sleep(0.1)
		print C+"          FqM            MMMM"
		time.sleep(0.1)
		print C+"         \033[33m_| '.        |\033[96mdS'qML'"
		time.sleep(0.1)
		print C+"        \033[33m|    `.       | `' \_\033[96mZq'"
		time.sleep(0.1)
		print C+"       \033[33m_)      \.___.,|     .'" 
		time.sleep(0.1)
		print C+"       \033[33m\________)\033[96mMMMMM\033[33m|   .' "
		time.sleep(0.1)
		print color.BOLD+"                      \033[33m`--'         "+color.END
		time.sleep(0.7)
		print O+'\nPreparing for installation...'
		time.sleep(0.5)
		print GR+'Finalising options...'
		time.sleep(0.5)
		raw_input(G+"\nPress 'Enter' to start the installation...") 
		Preinstall="rm -v -rf /opt/tidos/ && rm -v -f /usr/bin/tidos"
		print B+ '\nChecking for pre-installations...'
		time.sleep(0.5)
		print GR+'Removing any trace of pre-installations...'+O+''
		time.sleep(0.5)
		os.system(Preinstall)
		print GR+'Setting necessary permissions...'+O+''
		time.sleep(0.5)
		os.system('chmod -v +x dependencies')
		print GR+'Processing dependencies...'+O+''
		time.sleep(0.7)
		os.system('sudo bash dependencies')
		print GR+'Creating directories...'+O+''
		time.sleep(0.5)
		os.system('mkdir -v -p /opt/tidos/')
		print GR+'Copying new files...'+O+''
		time.sleep(0.5)
		os.system('cp -r -v * /opt/tidos/')
		print GR+'Creating shortcuts...'+O+''
		time.sleep(0.5)
		os.system('cp -v runon.sh /usr/bin/tidos')
		print GR+'Giving priviledges...'+O+''
		time.sleep(0.7)
		os.system('chmod -R 750 /opt/tidos/*')
		os.system('chmod -v 755 /usr/bin/tidos')
		time.sleep(1.5)

		print G+"\n [+] Setup successful!"
		print C+" [+] Execute "+B+'tidos'+C+" now to launch the tool..."
		time.sleep(0.5)

		print ''+GR+" [+] Also note that the next time you want to run this tool, just simply execute "+O+'tidos'+GR+" in terminal.\n"
		sys.exit()

	except KeyboardInterrupt:

		print R+'\n [-] Installation aborted...\n'

