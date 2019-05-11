import subprocess

def dig(target):
    for domain in target:
        DIGSCAN = "dig "+domain.name
        
        # print(bcolors.HEADER + "INFO: Starting dig scan for " + ip_address + bcolors.ENDC)
        #DIGSCAN = "dig " + target[0].name
        # print(bcolors.HEADER + DIGSCAN + bcolors.ENDC)
        results_dig = subprocess.check_output(DIGSCAN, shell=True)
        # print(bcolors.OKGREEN + "INFO: RESULT BELOW - Finished with dig scan for " + ip_address + bcolors.ENDC)
        this=results_dig.decode().replace("<<-","")
        print(this)
        # write_to_file(ip_address, "dig", this)
        # print(bcolors.OKGREEN + "INFO: nmap scan still in progress.. " + ip_address + bcolors.ENDC)
    return
