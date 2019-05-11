#!/usr/bin/env python
from core.colors import color
def threatintel(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # coding: utf-8

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author : @_tID
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import requests
# import socket
# import time
# from core.Core.colors import *
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# def usom(web,ip):

#     print(O+'\n [!] Checking on '+G+'Usom threatlist...')
#     try:
#         print(GR+' [*] Making a reverse DNS query...')
#         print(G+' [+] DNS : '+O+ip)
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://www.usom.gov.tr/url-list.txt', verify=False, timeout=10).content
#         for i in str(resp).splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' is harmful and has been reported on Usom...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per Usom...')

#     except:
#         print(R+' [-] Request to usom.gov.tr timed out!')
#         pass

# def badip(web,ip):

#     print(O+'\n [!] Checking on '+G+'Bad IPs threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get("https://www.badips.com/get/info/"+str(ip), verify=False, timeout=10).content
#         print(O+' [*] Parsing raw-data...')
#         time.sleep(0.7)
#         res = json.dumps(resp)
#         r = json.loads(res)
#         if r['Listed'] == 'True':
#             flag = True
#         else:
#             flag = False

#         if flag == True:
#             print(R+' [+] '+O+web+G+' is harmful and has been reported on badips.com...')
#             print(G+' [+] Bad IP : '+O+r['suc'])
#             print(G+" [+] Country : "+O+r['CountryCode'])
#             print(G+" [+] Report number: "+O+str(r['ReporterCount']['sum']))
#             print(G+" [+] Category: " +O+r['Categories'][0])
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per badips.com...')

#     except:
#         print(R+' [-] Request to badips.com timed out!')
#         pass

# def blocklistssh(web,ip):

#     print(O+'\n [!] Checking on '+G+'BlockLists SSH threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://lists.blocklist.de/lists/ssh.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' has been reported for attacks on SSH services...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

#     except:
#         print(R+' [-] Request to BlockLists timed out!')
#         pass

# def blocklistmail(web,ip):

#     print(O+'\n [!] Checking on '+G+'BlockLists Mail threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://lists.blocklist.de/lists/mail.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' has been reported for attacks on SMTP services...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

#     except:
#         print(R+' [-] Request to BlockLists timed out!')
#         pass

# def blocklistapache(web,ip):

#     print(O+'\n [!] Checking on '+G+'BlockLists APACHE threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://lists.blocklist.de/lists/apache.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' has been reported for attacks on Apache services...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

#     except:
#         print(R+' [-] Request to BlockLists timed out!')
#         pass

# def blocklistimap(web,ip):

#     print(O+'\n [!] Checking on '+G+'BlockLists IMAP threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://lists.blocklist.de/lists/imap.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' has been reported for attacks on IMAP services...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

#     except:
#         print(R+' [-] Request to BlockLists timed out!')
#         pass

# def blocklistpop3(web,ip):

#     print(O+'\n [!] Checking on '+G+'BlockLists POP3 threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://lists.blocklist.de/lists/pop3.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' has been reported for attacks on POP3 services...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

#     except:
#         print(R+' [-] Request to BlockLists timed out!')
#         pass

# def blocklistftp(web,ip):

#     print(O+'\n [!] Checking on '+G+'BlockLists FTP threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://lists.blocklist.de/lists/ftp.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' has been reported for attacks on FTP services...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

#     except:
#         print(R+' [-] Request to BlockLists timed out!')
#         pass

# def blocklistsip(web,ip):

#     print(O+'\n [!] Checking on '+G+'BlockLists SIP & VoIP threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://lists.blocklist.de/lists/sip.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' has been reported for attacks on SIP, VoIP services...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

#     except:
#         print(R+' [-] Request to BlockLists timed out!')
#         pass

# def blocklistbots(web,ip):

#     print(O+'\n [!] Checking on '+G+'BlockLists Bots threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://lists.blocklist.de/lists/bots.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' has been reported for attacks as HTTPD Bots, BAD Bots...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

#     except:
#         print(R+' [-] Request to BlockLists timed out!')
#         pass

# def blocklistirc(web,ip):

#     print(O+'\n [!] Checking on '+G+'BlockLists IRC threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://lists.blocklist.de/lists/ircbot.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' has been reported for attacks as IRC Bot...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

#     except:
#         print(R+' [-] Request to BlockLists timed out!')
#         pass

# def blockliststrong(web,ip):

#     print(O+'\n [!] Checking on '+G+'BlockLists Strong threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://lists.blocklist.de/lists/strongips.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' has been reported for attacks as Strong IPs...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

#     except:
#         print(R+' [-] Request to BlockLists timed out!')
#         pass

# def blocklistbrute(web,ip):

#     print(O+'\n [!] Checking on '+G+'BlockLists Bruteforce Login IPs threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://lists.blocklist.de/lists/bruteforcelogin.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' has been reported for attacks via Bruteforce on services...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

#     except:
#         print(R+' [-] Request to BlockLists timed out!')
#         pass

# def emergethreats(web,ip):

#     print(O+'\n [!] Checking on '+G+'Emerging Threats latest threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('http://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' is harmful and has been reported on Emerging Threats...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per Emerging Threats...')

#     except:
#         print(R+' [-] Request to Emerging Threats timed out!')
#         pass

# def emergecompro(web,ip):

#     print(O+'\n [!] Checking on '+G+'Emerging Threats comrpmised IPs threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('http://rules.emergingthreats.net/blockrules/compromised-ips.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' is harmful and has been reported on Emerging Threats...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per Emerging Threats...')

#     except:
#         print(R+' [-] Request to Emerging Threats timed out!')
#         pass

# def binarydefense(web,ip):

#     print(O+'\n [!] Checking on '+G+'Binary Defense threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('http://www.binarydefense.com/banlist.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' has a banned IP and has been reported on Binary Defense...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per Binary Defense...')

#     except:
#         print(R+' [-] Request to Binary Defense timed out!')
#         pass

# def openphish(web,ip):

#     print(O+'\n [!] Checking on '+G+'openphish.com threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://openphish.com/feed.txt', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#         if flag == True:
#             print(R+' [+] '+O+web+G+' is a harmful phishing site and has been reported on Open Phish...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per Open Phish...')

#     except:
#         print(R+' [-] Request to Open Phish timed out!')
#         pass

# def zeustracker(web,ip):

#     print(O+'\n [!] Checking on '+G+'zeustracker.com threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://zeustracker.abuse.ch/blocklist.php?download=badips', verify=False, timeout=10).text
#         print(C+' [!] Parsing raw data...')
#         time.sleep(0.5)
#         for i in resp.splitlines():
#             if ip in i:
#                 flag = True
#                 break
#         if flag == True:
#             print(R+' [+] '+O+web+G+' is a harmful phishing site and has been reported on Zeus Tracker...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per Zeus Tracker...')

#     except:
#         print(R+' [-] Request to zeustracker.com timed out!')
#         pass

# def projecthoneypot(web,ip):

#     print(O+'\n [!] Checking on '+G+'Project HoneyPot threatlist...')
#     try:
#         flag= False
#         print(GR+' [*] Making the request...')
#         resp = requests.get('https://www.projecthoneypot.org/list_of_ips.php', verify=False, timeout=10).text
#         if str(ip) in resp:
#             flag = True

#         if flag == True:
#             print(R+' [+] '+O+web+G+' is a harmful site and has been reported on Project HoneyPot...')
#         else:
#             print(G+' [+] '+O+web+G+' is clean as per Project HoneyPot...')

#     except:
#         print(R+' [-] Request to projecthoneypot.com timed out!')
#         pass

# def threatintel(web):

#     print(GR+' [*] Loading components...')
#     time.sleep(0.7)
#     print(R+'\n    =======================================')
#     print(R+'     T H R E A T   I N T E L L I G E N C E')
#     print(R+'    =======================================\n')
#     print(O+' [Data in these threatlists is the latest data')
#     print(O+'            not older than a week!]\n')
#     print(C+' [!] Parsing Url..')
#     time.sleep(0.7)
#     web = web.replace('https://','')
#     web = web.replace('http://','')
#     print(O+' [!] Getting host information...')
#     time.sleep(0.8)
#     ip = socket.gethostbyname(web)
#     print(G+' [+] DNS : '+O+str(ip))
#     print(C+' [!] Loading up modules...')
#     time.sleep(0.7)
#     print(GR+' [*] Starting gathering...')
#     usom(web,ip)
#     badip(web,ip)
#     blocklistssh(web,ip)
#     blocklistmail(web,ip)
#     blocklistsip(web,ip)
#     blocklistftp(web,ip)
#     blocklistpop3(web,ip)
#     blocklistirc(web,ip)
#     blocklistimap(web,ip)
#     blocklistbots(web,ip)
#     blockliststrong(web,ip)
#     blocklistapache(web,ip)
#     blocklistbrute(web,ip)
#     emergethreats(web,ip)
#     emergecompro(web,ip)
#     binarydefense(web,ip)
#     openphish(web,ip)
#     zeustracker(web,ip)
#     projecthoneypot(web,ip)
#     print(G+' [+] Done!')
