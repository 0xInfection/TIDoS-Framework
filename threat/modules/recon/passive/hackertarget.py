import requests
import socket
import time
from core.colors import color
from database.database_module import save_data
import inspect

# YOU ONLY GET 100 QUERIES PER DAY PER IP. (You get 10 queries total per host you send if you use them all)
def hackertarget(target):
    from core.build_menu import buildmenu
    site = 'https://api.hackertarget.com/'
    options = ['mtr','nping','dnslookup','reversedns','whois','geoip','reverseiplookup',\
        'httpheaders','pagelinks','aslookup']
    description=['Access to the MTR Traceroute API','Access to the on-line Test Ping API',\
    'Access to the DNS Lookup API','Access to the Reverse DNS Lookup API',\
    'Access to the Whois Lookup API','Access to the GeoIP Lookup API',\
    'Access to the Reverse IP Lookup API','Access to the HTTP Headers API',\
    'Access to the Page Links API','Access to the AS Lookup API']
    print(color.green(" [*] Finding HackerTarget.com information. This will take approximately 20 seconds ...\n"))
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        i=0
        for option in options:
            try:
                print(color.green(' [#] Checking: ')+color.yellow(description[i]))
                url = site + option + '/?q='+host.ip.replace('http://','').replace('https://','')
                check = requests.get(url)
                time.sleep(.5) # max query is 3 per second or you get blocked
                if check.status_code == 200:
                        data = check.text
                        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(data))
                else:
                    print(color.red(' [-] Did not find any info about domain ')+color.yellow(host.name))
                    print(color.red(' [+] Try with another one...'))
            except Exception as e:
                pass
                print(color.red(' [-] Encountered Exception : '+str(e)))
            i=i+1
    # return to main menu
    buildmenu(target,target[0].main_menu,'Main Menu','')




