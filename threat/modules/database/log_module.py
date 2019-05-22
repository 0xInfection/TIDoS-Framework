import os
import subprocess

def log(module_name, target, body):
    module_name = "{}/{}.txt".format(target, module_name.replace('/', '-'))
    if not os.path.isdir(target):
        subprocess.check_output(["mkdir", "{}".format(target)])
    file = open(module_name, 'a')
    file.write(target + ':' + '\n' + body + '\n' + '\n')
    file.close()