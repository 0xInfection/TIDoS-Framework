#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This script is a part of TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os, sys, urllib, urllib.request, time
from time import sleep
from core.Core.colors import *

info = "TIDoS frontend to the NMap scanner."
searchinfo = "NMap Scanner"
properties = {}

def nmapmain(web):

    web = web.replace('https://','')
    web = web.replace('http://','')
    print("")
    print(""+P+"                               _______      _____                 ")
    time.sleep(0.1)
    print(""+P+"                               \      \    /     \  ____  ______  ")
    time.sleep(0.1)
    print(""+P+"                               /   |   \  /  \ /  \/__  \ \____ \ ")
    time.sleep(0.1)
    print(""+P+"                              /    |    \/    Y    \/ __ \|  |_> >")
    time.sleep(0.1)
    print(""+P+"                              \____|__  /\____|__  (____  /   __/ ")
    time.sleep(0.1)
    print(""+P+"                                      \/         \/     \/|__|    ")
    time.sleep(0.2)
    print("")
    time.sleep(0.1)
    #print(''+C+'                      +======================================================+')
    #time.sleep(0.4)
    #print(R+"                               Target set :> %s" % web)
    #print(''+GR+'                      +=====================================================+')
    def nmapsx(web):
        try:
            q=input(''+G+'                     [?] Do you want a verbose output of the Scan? (y/n) :> ')
            if q == "y":
                print('')
                print(''+R+ '                         Choose the type of scan you want to perform :-')
                time.sleep(0.3)
                print(''+GR+'                      +=====================================================+')
                print('')
                print(""+C+"                        [1] \033[94mA Basic Port Scan")
                time.sleep(0.05)
                print(""+C+"                        [2] \033[94mA Single or Range of Port Scan")
                time.sleep(0.05)
                print(""+C+"                        [3] \033[94mScan the most common range of ports")
                time.sleep(0.05)
                print(""+C+"                        [4] \033[94mScan using TCP connect")
                time.sleep(0.05)
                print(""+C+"                        [5] \033[94mScan all UDP Ports")
                time.sleep(0.05)
                print(""+C+"                        [6] \033[94mScan for OS Detection and Services")
                time.sleep(0.05)
                print(""+C+"                        [7] \033[94mScan for UDP DDoS reflectors")
                time.sleep(0.05)
                print(""+C+"                        [8] \033[94mGather page titles from HTTP Headers")
                time.sleep(0.05)
                print(""+C+"                        [9] \033[94mStandard Service Detection of web services")
                time.sleep(0.05)
                print(""+C+"                        [10] \033[94mBrute Force DNS Hostnames guessing subdomains")
                time.sleep(0.05)
                print(""+C+"                        [11] \033[94mDetect Cross-Site Scripting (XSS) Vulnerabilites")
                time.sleep(0.05)
                print(""+C+"                        [12] \033[94mDetect SQL injection vulnerabilities")
                time.sleep(0.05)
                print(""+C+"                        [13] \033[94mDetect a Heart-Bleed SSL Vulnerability")
                time.sleep(0.05)
                print(""+C+"                        [14] \033[94mEvade Firewall/IDS using Fragmented packets")
                time.sleep(0.05)
                print(""+C+"                        [15] \033[94mDiscover Web-Applications in use\n")
                time.sleep(0.05)
                print(""+C+"                        [99] \033[94mBack to the TIDoS Shell")
                time.sleep(0.05)
                print('')
                print(''+GR+'                      +=====================================================+')
                print('')
                time.sleep(0.3)
                main = input(""+O+"                         Enter the number corresponding to the scan :> ")
                if main == "1":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        time.sleep(0.3)
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" Basic Port Scan")
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v --proxies socks4://127.0.0.1:9050 ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" Basic Port Scan")
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "2":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning initiated through default configured proxy...")
                        print('')
                        print(""+ C +"                             [¬] ScanType Selected:"+GR+" Specific Port Scan")
                        print('')
                        m = input(""+G+"                        [*] Enter port no. or port range (eg. 1-100) :> ")
                        print('')
                        print(""+ GR + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v --proxies socks4://127.0.0.1:9050 -p ' + m + ' ' + dom)
                            resu = str(text)
                            print(""+ G + resu)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ C +"                             [¬] ScanType Selected:"+GR+" Specific Port Scan")
                        print('')
                        m = input(""+G+"                        Enter port no. or port range (eg. 1-100) :> ")
                        print('')
                        print(""+ GR + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v -p ' + m + ' ' + dom)
                            resu = str(text)
                            print(""+ G + resu)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "3":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" Common Ports Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v -F --proxies socks4://127.0.0.1:9050 ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" Common Ports Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v -F ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "4":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" TCP Port Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v -sT --proxies socks4://127.0.0.1:9050 ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" TCP Port Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v -sT ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "5":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" UDP Port Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v --proxies socks4://127.0.0.1:9050 -sU -p 123,161,162 ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" UDP Port Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v -sU -p 123,161,162 ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "6":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" OS Detection and Services Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v --proxies socks4://127.0.0.1:9050 -A ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" OS Detection and Services Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v -A ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "7":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" UDP DDoS Reflectors Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v -sU -A --proxies socks4://127.0.0.1:9050 -Pn -n -pU:19,53,123,161 --script=ntp-monlist,dns-recursion,snmp-sysdescr ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" UDP DDoS Reflectors Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v -sU -A -Pn -n -pU:19,53,123,161 --script=ntp-monlist,dns-recursion,snmp-sysdescr '+dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "8":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" Page Titles from HTTP Headers")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v --proxies socks4://127.0.0.1:9050 --script=http-title ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" Page Titles from HTTP Headers")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v --script=http-title ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "9":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" Standard Services Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v --proxies socks4://127.0.0.1:9050 -sV ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" Standard Services Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v -sV ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "10":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" DNS Hostname Bruteforce")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v --proxies socks4://127.0.0.1:9050 -p 80 --script dns-brute.nse ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" DNS Hostname Bruteforce")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v -p 80 --script dns-brute.nse ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "11":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" XSS Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v --proxies socks4://127.0.0.1:9050 --script=http-stored-xss,http-dombased-xss ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" XSS Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v -p 80 --script=http-stored-xss,http-dombased-xss ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "12":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" SQLi Vulnerability Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -sV -v --proxies socks4://127.0.0.1:9050 --script=http-sql-injection ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" SQLi Vulnerability Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -sV -v --script=http-sql-injection ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "13":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" HeartBleed SSL Vulnerability Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v --proxies socks4://127.0.0.1:9050 -sV -p 443 --script=ssl-heartbleed ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" HeartBleed SSL Vulnerability Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v -sV -p 443 --script=ssl-heartbleed ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "14":
                    print('')
                    print(""+ O +"                     [!] Scanning initiated through default configured proxy...")
                    print('')
                    print(""+ B +"                     [¬] ScanType Selected:"+GR+" Firewall/IDS Evasion with Fragmented Packet Scan")
                    print(''+ R +'                     [!] This scan may take a long time because it is extremely stealthy !')
                    print('')
                    nm = input(""+ O + color.BOLD + "                     [!] Enter a domain to which your IP is to be spoofed(eg. google.com) :> ")
                    print('')
                    print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                    print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                    print(""+ color.YELLOW + color.BOLD + "     ║")
                    print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                    print(""+ G + color.BOLD + "")
                    domains = [web]
                    for dom in domains:
                        text = os.system('nmap -v --proxies socks4://127.0.0.1:9050 -D ' +nm+ ' -sS -sV -T1 -f --mtu=24 --data-length=1227 ' + dom)
                        res = str(text)
                        print(""+G+ color.BOLD + res)
                    print('')
                    i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                    if i == "":
                        nmapsx(web)
                elif main == "15":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" Web-Application Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v --proxies socks4://127.0.0.1:9050 --script=http-enum ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" Web-Application Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -v --script=http-enum ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                            print('')
                elif main == "16":
                    print(""+C+"                        [!] Back to the TIDoS shell")
                    print('')
                else:
                    print(''+R+'                       [!] Python ran mad !!!')
            elif q == "n":
                print('')
                print(''+R+ '                         Choose the type of scan you want to perform :-')
                time.sleep(0.3)
                print(''+GR+'                      +=====================================================+')
                print('')
                print(""+C+"                        [1] \033[94mA Basic Port Scan")
                time.sleep(0.1)
                print(""+C+"                        [2] \033[94mA Single or Range of Port Scan")
                time.sleep(0.1)
                print(""+C+"                        [3] \033[94mScan the most common range of ports")
                time.sleep(0.1)
                print(""+C+"                        [4] \033[94mScan using TCP connect")
                time.sleep(0.1)
                print(""+C+"                        [5] \033[94mScan all UDP Ports")
                time.sleep(0.1)
                print(""+C+"                        [6] \033[94mScan for OS Detection and Services")
                time.sleep(0.1)
                print(""+C+"                        [7] \033[94mScan for UDP DDoS reflectors")
                time.sleep(0.1)
                print(""+C+"                        [8] \033[94mGather page titles from HTTP Headers")
                time.sleep(0.1)
                print(""+C+"                        [9] \033[94mStandard Service Detection of web services")
                time.sleep(0.1)
                print(""+C+"                        [10] \033[94mBrute Force DNS Hostnames guessing subdomains")
                time.sleep(0.1)
                print(""+C+"                        [11] \033[94mDetect Cross-Site Scripting (XSS) Vulnerabilites")
                time.sleep(0.1)
                print(""+C+"                        [12] \033[94mDetect SQL injection vulnerabilities")
                time.sleep(0.1)
                print(""+C+"                        [13] \033[94mDetect a Heart-Bleed SSL Vulnerability")
                time.sleep(0.1)
                print(""+C+"                        [14] \033[94mEvade Firewall/IDS using Fragmented packets")
                time.sleep(0.1)
                print(""+C+"                        [15] \033[94mDiscover Web-Applications in use")
                time.sleep(0.1)
                print(""+C+"                        [16] \033[94mBack to the TIDoS Shell")
                time.sleep(0.1)
                print('')
                print(''+GR+'                      +=====================================================+')
                time.sleep(0.2)
                print('')
                main = input(""+O+"                         Enter the number corresponding to the scan :> ")
                if main == "1":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" Basic Port Scan")
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap --proxies socks4://127.0.0.1:9050 ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" Basic Port Scan")
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "2":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning initiated through default configured proxy...")
                        print('')
                        print(""+ C +"                             [¬] ScanType Selected:"+GR+" Specific Port Scan")
                        print('')
                        m = input(""+G+"                        [*] Enter port no. or port range (eg. 1-100) :> ")
                        print('')
                        print(""+ GR + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap --proxies socks4://127.0.0.1:9050 -p ' + m + ' ' + dom)
                            resu = str(text)
                            print(""+ G + resu)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ C +"                             [¬] ScanType Selected:"+GR+" Specific Port Scan")
                        print('')
                        m = input(""+G+"                        Enter port no. or port range (eg. 1-100) :> ")
                        print('')
                        print(""+ GR + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -p ' + m + ' ' + dom)
                            resu = str(text)
                            print(""+ G + resu)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "3":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" Common Ports Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -F --proxies socks4://127.0.0.1:9050 ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" Common Ports Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -F ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "4":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" TCP Port Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -sT --proxies socks4://127.0.0.1:9050 ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" TCP Port Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -sT ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "5":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" UDP Port Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap --proxies socks4://127.0.0.1:9050 -sU -p 123,161,162 ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" UDP Port Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -sU -p 123,161,162 ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "6":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" OS Detection and Services Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap --proxies socks4://127.0.0.1:9050 -A ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" OS Detection and Services Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -A ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "7":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" UDP DDoS Reflectors Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -sU -A --proxies socks4://127.0.0.1:9050 -Pn -n -pU:19,53,123,161 --script=ntp-monlist,dns-recursion,snmp-sysdescr ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" UDP DDoS Reflectors Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -sU -A -Pn -n -pU:19,53,123,161 --script=ntp-monlist,dns-recursion,snmp-sysdescr '+dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "8":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" Page Titles from HTTP Headers")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap --proxies socks4://127.0.0.1:9050 --script=http-title ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                             [¬] ScanType Selected:"+GR+" Page Titles from HTTP Headers")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap --script=http-title ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "9":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" Standard Services Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap --proxies socks4://127.0.0.1:9050 -sV ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" Standard Services Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -sV ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "10":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" DNS Hostname Bruteforce")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap --proxies socks4://127.0.0.1:9050 -p 80 --script dns-brute.nse ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" DNS Hostname Bruteforce")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -p 80 --script dns-brute.nse ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "11":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" XSS Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap --proxies socks4://127.0.0.1:9050 --script=http-stored-xss,http-dombased-xss ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" XSS Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -p 80 --script=http-stored-xss,http-dombased-xss ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "12":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" SQLi Vulnerability Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -sV --proxies socks4://127.0.0.1:9050 --script=http-sql-injection ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" SQLi Vulnerability Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -sV --script=http-sql-injection ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "13":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" HeartBleed SSL Vulnerability Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap --proxies socks4://127.0.0.1:9050 -sV -p 443 --script=ssl-heartbleed ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" HeartBleed SSL Vulnerability Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap -sV -p 443 --script=ssl-heartbleed ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                elif main == "14":
                    print('')
                    print(""+ O +"                     [!] Scanning initiated through default configured proxy...")
                    print('')
                    print(""+ B +"                     [¬] ScanType Selected:"+GR+" Firewall/IDS Evasion with Fragmented Packet Scan")
                    print(''+ R +'                     [!] This scan may take a long time because it is extremely stealthy !')
                    print('')
                    nm = input(""+ O + color.BOLD + "                     [!] Enter a domain to which your IP is to be spoofed(eg. google.com) :> ")
                    print('')
                    print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                    print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                    print(""+ color.YELLOW + color.BOLD + "     ║")
                    print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                    print(""+ G + color.BOLD + "")
                    domains = [web]
                    for dom in domains:
                        text = os.system('nmap --proxies socks4://127.0.0.1:9050 -D ' +nm+ ' -sS -sV -T1 -f --mtu=24 --data-length=1227 ' + dom)
                        res = str(text)
                        print(""+G+ color.BOLD + res)
                    print('')
                    i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                    if i == "":
                        nmapsx(web)
                elif main == "15":
                    q = input (''+G+'                        [*] Do you want to scan through a proxy? (Y/n) :> ')
                    if q == "y":
                        print('')
                        print(""+ O +"                             [!] Scanning through default configured proxy...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" Web-Application Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap --proxies socks4://127.0.0.1:9050 --script=http-enum ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                    else:
                        print('')
                        print(""+ O +"                             [!] Scanning through direct IP (exposes your IP)...")
                        print('')
                        print(""+ B +"                          [¬] ScanType Selected:"+GR+" Web-Application Scan")
                        print('')
                        print(""+ R + color.BOLD + "                                [~] Result: "+color.YELLOW+color.BOLD+"════════════════╗" + color.END)
                        print(""+ color.YELLOW + color.BOLD + "     ╔══════════════════════════════════════════════════════╝")
                        print(""+ color.YELLOW + color.BOLD + "     ║")
                        print(""+ color.YELLOW + color.BOLD + "     ▽"+color.END)
                        print(""+ G + color.BOLD + "")
                        domains = [web]
                        for dom in domains:
                            text = os.system('nmap --script=http-enum ' + dom)
                            res = str(text)
                            print(""+G+ color.BOLD + res)
                        print('')
                        i = input(''+O+'                       [!] Scan Completed! Press ENTER to continue')
                        if i == "":
                            nmapsx(web)
                            print('')
                elif main == "16":
                    print(""+C+"                        [!] Back !")
                    print('')
                else:
                    print(''+R+'                       [!] Python ran mad !')
        except Exception as e:
            print(R+'\n                       [!] Fatal exception encountered !')
            print(R+'                       [!] Exception : '+str(e))
    nmapsx(web)

def attack(web):
    web = web.fullurl
    nmapmain(web)