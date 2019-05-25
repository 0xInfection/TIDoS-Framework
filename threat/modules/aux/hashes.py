#!/usr/bin/env python
from core.colors import color
import hashlib
import inspect
import os
from database.database_module import save_data

def hashes(target):
    from core.build_menu import buildmenu
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3='' 
    try:
        message = input('\n [#] Enter the string to hash:> ')
        print(color.green(' [+] Generating hashes...'))
        md5 = hashlib.md5()
        md5.update(message.encode('utf-8'))
        
        sha1 = hashlib.sha1()
        sha1.update(message.encode('utf-8'))
        
        sha224 = hashlib.sha224()
        sha224.update(message.encode('utf-8'))       

        sha256 = hashlib.sha256()
        sha256.update(message.encode('utf-8'))
        
        sha384 = hashlib.sha384()
        sha384.update(message.encode('utf-8'))
    
        sha512 = hashlib.sha512()
        sha512.update(message.encode('utf-8'))
        
        print(color.green(" [+] MD5 Hash : ")+color.yellow(md5.hexdigest()))
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(md5.hexdigest()))
        print(color.green(" [+] SHA1 Hash : ")+color.yellow(sha1.hexdigest()))
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(sha1.hexdigest()))
        print(color.green(" [+] SHA224 Hash : ")+color.yellow(sha224.hexdigest()))
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(sha224.hexdigest()))
        print(color.green(" [+] SHA256 Hash : ")+color.yellow(sha256.hexdigest()))
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(sha256.hexdigest()))
        print(color.green(" [+] SHA384 Hash : ")+color.yellow(sha384.hexdigest()))
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(sha384.hexdigest()))
        print(color.green(" [+] SHA512 Hash : ")+color.yellow(sha512.hexdigest()))
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(sha512.hexdigest()))

    except EOFError as e:
        #os.system('clear')
        print(e)
    st = input(color.blue(' [#] Press')+color.red(' Enter ')+color.blue('to continue... '))
    buildmenu(target,target[0].main_menu,'Main Menu','')