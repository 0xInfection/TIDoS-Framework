#!/usr/bin/env python

import re
import json
from core.colors import color
from modules.enumeration.nmap_menu import nmap_menu
from modules.enumeration.nmap_builder import nmap_target_sorter
from modules.enumeration.nmap_support.nmap_helper_functions import list_create_and_dedupe
from modules.enumeration.nmap_support.nmap_helper_functions import tag_manager
from modules.enumeration.nmap_support.nmap_helper_functions import retrieve_module_index

### -- THIS IS THE PATH OF THE DEFAULT TARGET ACCESSED INITIALLY IN THE EDITOR -- ###
with open('modules/enumeration/nmap_support/sample_target.json') as the_json:
    default_target = json.load(the_json)
#####################################################################################


with open('modules/enumeration/nmap_support/nmap_menu.json') as the_json:
    menu_objects = json.load(the_json)

# Final Display Menu is built into this dict object
menu = {}

# Determines order of Menu Items. Must have matching header value in {nmap_menu.json} to appear in menu
start_menu_order = ['Run NMAP', 'Edit Target', 'Set Port Range']
menu_toggle_items = []
list_create_and_dedupe("header_template", menu_objects, menu_toggle_items, start_menu_order, menu_objects)

# Creates a list of all the unique tags (limit to Toggle Tags only by using ignore list)
ignore_list = ['-p']
cmd_list = []
list_create_and_dedupe("tag", menu_objects, cmd_list, ignore_list, menu_objects)

# Master menu list is combination of ALL "header_templates" in {nmap_menu.json} 
preferred_order = start_menu_order + menu_toggle_items

# Variables (LETTERS) for Menu buttons (If like to customize, only need to change here)
the_all_off_button = "F"
the_all_on_button = "O"
exit_button = "0"
description_button = "D"
description_boolean = False

# --------------------- Helper Functions -----------------------------
cmd2num = {}
def cmd2num_associator(arg, menu_obj):
    for each_tag in arg:
        for menu_number in menu_obj:
            if("tag" in menu_obj[menu_number] and menu_obj[menu_number]["tag"] == each_tag):
                cmd2num[each_tag] = menu_number

def create_edit_menu(menu, passed_target):
    global description_boolean
    index = 0
    for index, order_header in enumerate(preferred_order):
        for each_menu in menu_objects:
            if (each_menu["header"].find(order_header) != -1):
                string_index = str(index + 1)
                menu[string_index] = each_menu

    # --------------------- Lower Menu -----------------------------
    menu[" "] = {"header" : False} 
    menu[the_all_off_button.upper()] = {"header" : "Turn off all options"}
    menu[the_all_on_button.upper()] = {"header" : "Turn on all options"}
    menu[description_button.upper()] = {"header" : "Description Toggle"}
    menu[exit_button.upper()] = {"header" : ">>> Exit"}
    cmd2num_associator(cmd_list, menu)


    ### --- Shortcut variable to avoid repeated typing of ~[0]["nmap"] --- ###
    # nmap_obj = default_target[0]["nmap"]
    nmap_obj = passed_target[0].cmd_options
    ##########################################################################


    # DYNAMIC TOGGLE UPDATING OF MENU ICONS using {cmd2num} as template to access {menu} values
    for key in cmd2num:
        node = menu[cmd2num[key]]
        header = color.blue(node["header_template"])
        # If target obj has a relevant param set to true, show in menu as on. Otherwise show as turned off
        if(key in nmap_obj and nmap_obj[key] == True):
            nmap_obj[key] = True
            node["header"] = color.yellow(node["on"]) + header
        elif(key in nmap_obj and nmap_obj[key] == True):
            nmap_obj[key] = False
            node["header"] = color.red(node["off"]) + header
        else:
            nmap_obj[key] = False
            node["header"] = color.red(node["off"]) + header

    # Display Menu on screen
    for menu_number in menu:
        each_menu = menu[menu_number]
        single_digit_buffer = ''
        if(menu_number.isdigit() and int(menu_number) < 10):
            single_digit_buffer = ' '
        else:
            single_digit_buffer = ''
        if(each_menu["header"] == False):
            print(' ')
        elif(description_boolean and "description" in each_menu):
            print(color.green(" [") +color.green(menu_number)+color.green("]"), single_digit_buffer, color.blue(each_menu["header"]), color.dark_grey(each_menu["description"]))
        else:
            print(color.green(" [") +color.green(menu_number)+color.green("]"), single_digit_buffer, color.blue(each_menu["header"]))


# ------------------ This is the start of the NMAP MENU function -------------------------------
# After {create_edit_menu} is ran in {nmap_menu} function, menu items are displayed and user_input determines next steps
def nmap_editor(passed_target):
    from core.build_menu import buildmenu

    global description_boolean
    user_input = ''
    nmap_obj = passed_target[0]
    nmap_params = passed_target[0].cmd_options
    exit_condition = False

    while(exit_condition == False):
        # Invoke Create Menu Function
        create_edit_menu(menu, passed_target)
        nmap_command = str(nmap_target_sorter(passed_target[0]))
        nmap_obj.nmap = nmap_command
        print('\n' + '-'*55)
        print(color.green('Current nmap Command:  \n') + color.red(nmap_command) + '\n' + '-'*55)

        # [E] :  ----------- Graceful Exit  --------------------
        user_input = input('\n[#] Choose Option:> ')
        lowered = user_input.lower()
        if(lowered == exit_button or lowered == 'exit' or lowered == 'e' or lowered == 0):
            exit_condition = True

        # Clean user input
        if (list(user_input.strip())[0].isalpha()):
            user_input = list(user_input.strip())[0].lower()
        else:
            user_input = str(user_input.strip())
        tag_arg_set = [preferred_order, nmap_params, menu]

        # [D] : --------- Description toggle -------------------------
        if(user_input.lower() == 'd'):
            reversed = not description_boolean # Reverse Boolean
            description_boolean = reversed

        # [O] or [F] : --------- Turn ON/OFF ALL NMAP tag toggles -------------------------
        elif(user_input.upper() == the_all_on_button):
            tag_manager(menu_toggle_items, True, tag_arg_set)
        elif(user_input.upper() == the_all_off_button):
            tag_manager(menu_toggle_items, False, tag_arg_set)

        # [1] :  --------------------- 2. Run NMAP  -----------------------------------------
        elif(user_input == '1'):
            exit_condition = True

        # [2] :  -------- 2. Adjust IP Address (Target Address)  -----------------------------
        elif(user_input == retrieve_module_index('Edit Target', preferred_order)):
            address = input(menu[user_input]["start_msg"])
            reg_string = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
            if(address == 'exit'):
                print('Exiting')
            elif(re.match(reg_string, address)):
                nmap_obj.name = address
            else:
                print(color.red(menu[user_input]["error"]))

        # [3] : -------------------- 3. Set Port Range ---------------------------------------
        elif(user_input == retrieve_module_index('Set Port Range', preferred_order)):
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
        
        # -------------------- All other toggle options --------------------------------------- 
        else:
            for each_toggle in menu_toggle_items:
                tag_manager(each_toggle, user_input, tag_arg_set)
    nmap_menu(passed_target)
