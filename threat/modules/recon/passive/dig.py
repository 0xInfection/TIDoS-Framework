import subprocess
from database.database_module import save_data
import inspect

def dig(target):
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        DIGSCAN = "dig "+host.name
        results_dig = subprocess.check_output(DIGSCAN, shell=True)
        data=results_dig.decode().replace("<<","").replace(">>","")
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
    return