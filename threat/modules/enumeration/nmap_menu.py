import re
from core.colors import color
from modules.enumeration.nmap_builder import nmap_target_sorter

test_target = [{
    "ip": "10.10.10.1",
    "nmap": {
        "-sV": True,
        "-sC": True,
        "-p": "80-125",
        "-oA": False
    }
}]

menu = {
    "1": "Run NMAP Command",
    "2": "Port Range",
    "3": "Edit Target",
    "4": "[ ] Scan for Services ON/OFF",
    "e": "Exit"
}

def create_nmap_menu(menu):
    nmap_obj = test_target[0]["nmap"]
    if(nmap_obj["-sV"] == True):
        print('\nService Scan has been set\n')
        menu["4"] = "[@] Scan for Services ON/OFF"
    else:
        print('\nService Scan has been deactivated\n')
        menu["4"] = "[ ] Scan for Services ON/OFF"
    for keys in menu:
        print(color.green(keys), ' ', color.blue(menu[keys]))

def nmap_menu(target):
    user_input = ''
    nmap_obj = test_target[0]
    nmap_params = nmap_obj["nmap"]
    exit_condition = False
    while(exit_condition == False):

        # Display Menu
     create_nmap_menu(menu)
        nmap_command = str(nmap_target_sorter(nmap_obj)[0])
        print('\n')
        print('-'*40)
        print(color.green('Current nmap Command:  '))
        print(color.blue(nmap_command))
        print('-'*40)

        user_input = input('\n[#] Choose Option:> ')
        if(user_input.lower() == 'exit' or user_input.lower() == 'e'):
            exit_condition = True
        
        # Set Port Range
        if(user_input == '2'):
            port_range = input('Enter Desired Port Range (ie: 80, 5-100, \'ALL\')\n')
            if(port_range.lower() == 'all' or port_range == '-p-'):
                nmap_params['-p'] = False
                nmap_params['-p-'] = True
            elif(re.match(r'^\d{1,5}(-?\d{1,5})?$', port_range)):
                nmap_params['-p'] = port_range
            else:
                print(color.red('INVALID PORT RANGE'))
        elif(user_input == '4'):
            value = not nmap_params['-sV']
            nmap_params['-sV'] = value
            