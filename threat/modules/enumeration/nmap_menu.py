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
run_nmap = 'Run NMAP'

# This Array determines the order of Menu Items and can be adjusted freely. 
# Must have matching header value in {menu_objects} to appear in menu
preferred_order = [
run_nmap,
edit_target_module,
set_port_module,
"Run Default Scripts",
"Scan Service Versions"
]

# This dict associates nmap tags with their numbered order when ran thru the associator function
# This helps find all relevant menu attributes from the nmap tag alone (ie: -sV)
cmd_list = ['-sC', '-sV']
cmd2num = {}
def cmd2num_associator(arg, menu_obj):
    for each_tag in arg:
        for menu_number in menu_obj:
            if("tag" in menu_obj[menu_number] and menu_obj[menu_number]["tag"] == each_tag):
                cmd2num[each_tag] = menu_number


# Final Display Menu is built into this dict object
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
        "error": '\n ***** INVALID ADDRESS FORMAT ***** \n',
        "description": "x"
    },
    {
        "start_msg" : "Enter Desired Port Range (ie: 80, 5-100, \'ALL\')\n",
        "header": set_port_module,
        "tag": "-p",
        "error": '\n***** INVALID PORT RANGE ***** \n',
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

# Which index number is each module?
def retrieve_module_index(invoked_module):
    return str(preferred_order.index(invoked_module) + 1)

def create_nmap_menu(menu):
    for index, order_header in enumerate(preferred_order):
        for each_menu in menu_objects:
            if (each_menu["header"].find(order_header) != -1):
                string_index = str(index + 1)
                menu[string_index] = each_menu
    cmd2num_associator(cmd_list, menu)

    nmap_obj = test_target[0]["nmap"]

    # DYNAMIC UPDATING OF MENU ICONS using {cmd2num} as template to access {menu} values
    for key in cmd2num:
        node = menu[cmd2num[key]]
        header = color.blue(node["header_template"])
        # If target obj has a relevant param set to true, show in menu as on. Otherwise show as turned off
        if(nmap_obj[key] == True):
            node["header"] = color.yellow(node["on"]) + header
        else:
            node["header"] = color.red(node["off"]) + header

    # Display Menu on screen
    for menu_number in menu:
        print(color.green(" [") +color.green(menu_number)+color.green("]"), color.blue(menu[menu_number]["header"]))


# This is the start of the function
# After {create_nmap_menu} is ran in {nmap_meny}, menu items are displayed and user_input determines next steps
def nmap_menu(target):
    user_input = ''
    nmap_obj = test_target[0]
    nmap_params = nmap_obj["nmap"]
    exit_condition = False

    # Tag manager can be used to create as many menu options pertaining to nmap tags that toggle on/off
    def tag_manager(module_type, choice):
        target_edit_index = retrieve_module_index(module_type)
        if(choice == target_edit_index):
            order_header = not nmap_params[menu[choice]["tag"]] # Reverse Boolean
            nmap_params[menu[choice]["tag"]] = order_header
            if(order_header == True):
                print(menu[choice]["on_msg"])
            elif(order_header == False):
                print(menu[choice]["off_msg"])

    while(exit_condition == False):
        # Invoke Create Menu Function
        create_nmap_menu(menu)
        nmap_command = str(nmap_target_sorter(nmap_obj)[0])
        print('\n' + '-'*55)
        print(color.green('Current nmap Command:  ') + color.red(nmap_command) + '\n' + '-'*55)

        user_input = input('\n[#] Choose Option:> ')
        if(user_input.lower() == 'exit' or user_input.lower() == 'e'):
            exit_condition = True

        target_edit_index = retrieve_module_index(edit_target_module)
        port_edit_index = retrieve_module_index(set_port_module)
        
        # 2 :  Adjust IP Address (Target Address)
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
        elif(user_input == port_edit_index):
            port_range = input(menu[user_input]["start_msg"])
            if(port_range == 'exit'):
                print('Exiting')
            elif(port_range.lower() == 'none' or port_range == 0):
                nmap_params['-p'] = False
                nmap_params['-p-'] = False   
            elif(port_range.lower() == 'all' or port_range == '-p-'):
                nmap_params['-p'] = False
                nmap_params['-p-'] = True
            elif(re.match(r'^\d{1,5}(-?\d{1,5})?$', port_range)):
                nmap_params['-p'] = port_range
            else:
                print(color.red(menu[user_input]["error"]))
        else:
            tag_manager('Run Default Scripts', user_input)
            tag_manager('Scan Service Versions', user_input)
  