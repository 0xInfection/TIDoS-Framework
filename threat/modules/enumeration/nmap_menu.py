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

# These variables represent menu display names which tie the entire nmap menu together
edit_target_module = 'Edit Target'
set_port_module = 'Set Port Range'

# This Array determines the order of Menu Items and can be adjusted freely. 
# Must have matching header value in {menu_objects} to appear in menu
preferred_order = [
'Run NMAP',
edit_target_module,
set_port_module,
"Run Default Scripts",
"Scan Service Versions"
]

# Display Menu is built into this dict object
menu = {}

# List of menu item dicts and their various attributes
menu_objects = [
    {
        "header": "Run NMAP",
        "description": "x"
    },
    {
        "header": edit_target_module ,
        "start_msg" : "Enter New Target Address\n",
        "error": '\nINVALID ADDRESS FORMAT\n',
        "description": "x"
    },
    {
        "start_msg" : "Enter Desired Port Range (ie: 80, 5-100, \'ALL\')\n",
        "header": set_port_module,
        "tag": "-p",
        "error": '\nINVALID PORT RANGE\n',
        "description": "x"
    },
    {
        "header": "[ ] Run Default Scripts",
        "tag": "-sC",
        "on": "[!]",
        "off": "[ ]",
        "on_msg": '\n *** Run Default Scripts has been turned on\n',
        "off_msg": '\n *** Run Default Scripts has been turned off\n',
        "header_template": " Run Default Scripts",
        "description": " (-sC) nmap.org/nsedoc/categories/default"
    },
    {
        "header": "\n [ ] Scan Service Versions\n",
        "tag": "-sV",
        "on": "[!]",
        "off": "[ ]",
        "on_msg": '\n *** Service Version Scan has been turned on\n',
        "off_msg": '\n *** Service Version Scan has been turned off\n',
        "header_template": " Scan Service Versions",
        "description": "x"
    },
]

# This dict associates nmap tags with their order (needs to be dynamic but is not yet)
cmd2num = {
    "-sC": "4",
    "-sV": "5",
}

def retrieve_module_index(invoked_module):
    return str(preferred_order.index(invoked_module) + 1)

def create_nmap_menu(menu):
    # Dynamically create enumerated list of Menu Commands based off "preferred_order" object
    for index, order_header in enumerate(preferred_order):
        for each_menu in menu_objects:
            if (each_menu["header"].find(order_header) != -1):
                string_index = str(index + 1)
                menu[string_index] = each_menu

    nmap_obj = test_target[0]["nmap"]

    # DYNAMIC UPDATING OF MENU ICONS using {cmd2num} as template to access {menu} values
    for key in cmd2num:
        if(nmap_obj[key] == True): # If target obj has a relevant param set to true, reflect it in menu as yellow & turned on
            node = menu[cmd2num[key]]
            on_icon = color.yellow(node["on"])
            header = color.blue(node["header_template"])
            node["header"] = on_icon + header
        else:
            node = menu[cmd2num[key]] # Otherwise, reflect it in meny as turned off (no icon, color red)
            off_icon = color.red(node["off"])
            header = color.blue(node["header_template"])
            node["header"] = off_icon + header

    # Display Menu on screen
    for menu_number in menu:
        print(color.green(" [") +color.green(menu_number)+color.green("]"), color.blue(menu[menu_number]["header"]))


def nmap_menu(target):
    user_input = ''
    nmap_obj = test_target[0]
    nmap_params = nmap_obj["nmap"]
    exit_condition = False
    while(exit_condition == False):
        # Invoke Create Menu Function
        create_nmap_menu(menu)
        nmap_command = str(nmap_target_sorter(nmap_obj)[0])
        print('\n')
        print('-'*40)
        print(color.green('Current nmap Command:  '))
        print(color.red(nmap_command))
        print('-'*40)

        # User Choices
        user_input = input('\n[#] Choose Option:> ')

        # Consider Exit
        if(user_input.lower() == 'exit' or user_input.lower() == 'e'):
            exit_condition = True

        # 2 :  Adjust IP Address (Target Address)
        target_edit_index = retrieve_module_index(edit_target_module)

        if(user_input == target_edit_index):
            address = input(menu[user_input]["start_msg"])
            reg_string = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
            if(address == 'exit'):
                print('Exiting')
            elif(re.match(reg_string, address)):
                nmap_obj["ip"] = address
            else:
                print(color.red(menu[user_input]["error"]))

        # 3: Set Port Range
        target_edit_index = retrieve_module_index(set_port_module)
        if(user_input == target_edit_index):
            port_range = input(menu[user_input]["start_msg"])
            if(port_range == 'exit'):
                print('Exiting')
            elif(port_range.lower() == 'all' or port_range == '-p-'):
                nmap_params['-p'] = False
                nmap_params['-p-'] = True
            elif(re.match(r'^\d{1,5}(-?\d{1,5})?$', port_range)):
                nmap_params['-p'] = port_range
            else:
                print(color.red(menu[user_input]["error"]))

        # 4. Run Default Script
        target_edit_index = retrieve_module_index('Run Default Scripts')
        if(user_input == target_edit_index):
            order_header = not nmap_params[menu[user_input]["tag"]]
            nmap_params['-sC'] = order_header
            if(order_header == True):
                print(menu[user_input]["on_msg"])
            elif(order_header == False):
                print(menu[user_input]["off_msg"])
        
        # 5. Set Service Scan
        target_edit_index = retrieve_module_index('Scan Service Versions')
        if(user_input == target_edit_index):
            order_header = not nmap_params[menu[user_input]["tag"]]
            nmap_params['-sV'] = order_header
            if(order_header == True):
                print(menu[user_input]["on_msg"])
            elif(order_header == False):
                print(menu[user_input]["off_msg"])
        