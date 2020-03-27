#!/usr/bin/env python

import subprocess
from database.database_module import save_data

'''
    import subprocess
    from database.database_module import save_data

    def dig(target):
        for host in target:
            host.lvl2='dig'
            host.lvl3=''
            DIGSCAN = "dig "+host.name
            results_dig = subprocess.check_output(DIGSCAN, shell=True)
            data=results_dig.decode().replace("<<","").replace(">>","")
            save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
        return
'''

def enum4linux(target):
    print('ENUM4LINUX')

    for host in target:
        print('ENUM HOST', host.ip, host.port)
        host.lvl3 = 'enum4linux'
        ENUM4LINUXSCAN = 'enum4linux ' + host.ip
        # results_enum4linux = subprocess.run(ENUM4LINUXSCAN, shell=True)
        results_enum4linux = subprocess.check_output(ENUM4LINUXSCAN, shell=True)
        data = results_enum4linux.decode().replace("<<","").replace(">>","")
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
    return

#     target[0].ip = '10.10.10.125'       # temp value
#     target[0].port = '445'              # temp value

#     enum4linux_str = 'enum4linux ' + target[0].ip

# if __name__=='__main__':
#     try:
#         enum4linux(target)

#     except (KeyboardInterrupt, SystemExit):
#         print("\nKeyboard interrupted")
#         exit()
#         raise
