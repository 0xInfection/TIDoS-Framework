import subprocess
from core.database.database_module import save_data
from core.variables import database
import inspect
from core.methods.tor import session

info = "Dig DNS lookup module"
searchinfo = "Dig DNS lookup"
properties = {}

def dig(target):
    requests = session()
    name = target.name
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl2=inspect.stack()[0][3]
    lvl3=''
    DIGSCAN = "dig "+name
    results_dig = subprocess.check_output(DIGSCAN, shell=True)
    data=results_dig.decode().replace("<<","").replace(">>","")
    save_data(database, module, lvl1, lvl2, lvl3, name, data)
    return

def attack(web):
    dig(web)
