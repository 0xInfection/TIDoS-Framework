#!/usr/bin/env python

import re
import json
from core.colors import color
from modules.enumeration.nmap_builder import nmap_target_sorter
from modules.enumeration.nmap_support.nmap_helper_functions import *
with open('modules/enumeration/nmap_support/sample_target.json') as the_json:
    test_target = json.load(the_json)
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
exit_button = "E"


# --------------------- Helper Functions -----------------------------
cmd2num = {}
def cmd2num_associator(arg, menu_obj):
    for each_tag in arg:
        for menu_number in menu_obj:
            if("tag" in menu_obj[menu_number] and menu_obj[menu_number]["tag"] == each_tag):
                cmd2num[each_tag] = menu_number

def create_nmap_menu(menu):
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
    menu[exit_button.upper()] = {"header" : "Exit"}
    cmd2num_associator(cmd_list, menu)

    # Access target object nmap KEY object in List to avoid repeated typing of ~[0]["nmap"]
    nmap_obj = test_target[0]["nmap"]

    # DYNAMIC TOGGLE UPDATING OF MENU ICONS using {cmd2num} as template to access {menu} values
    for key in cmd2num:
        node = menu[cmd2num[key]]
        header = color.blue(node["header_template"])
        # If target obj has a relevant param set to true, show in menu as on. Otherwise show as turned off
        if(key in nmap_obj and nmap_obj[key] == True):
            node["header"] = color.yellow(node["on"]) + header
        else:
            nmap_obj[key] = False
            node["header"] = color.red(node["off"]) + header

    # Display Menu on screen
    for menu_number in menu:
        if(menu[menu_number]["header"] == False):
            print(' ')
        else:
            print(color.green(" [") +color.green(menu_number)+color.green("]"), color.blue(menu[menu_number]["header"]))


# ------------------ This is the start of the NMAP MENU function -------------------------------
# After {create_nmap_menu} is ran in {nmap_menu}, menu items are displayed and user_input determines next steps
def nmap_menu(target):
    user_input = ''
    nmap_obj = test_target[0]
    nmap_params = nmap_obj["nmap"]
    exit_condition = False

    while(exit_condition == False):
        # Invoke Create Menu Function
        create_nmap_menu(menu)
        nmap_command = str(nmap_target_sorter(nmap_obj)[0])
        print('\n' + '-'*55)
        print(color.green('Current nmap Command:  \n') + color.red(nmap_command) + '\n' + '-'*55)

        # [E] :  ----------- Graceful Exit  --------------------
        user_input = input('\n[#] Choose Option:> ')
        if(user_input.lower() == 'exit' or user_input.lower() == 'e'):
            exit_condition = True

        # Clean user input hardcore-ly
        user_input = list(user_input.strip())[0].lower()
        tag_arg_set = [preferred_order, nmap_params, menu]


        # [O] or [F] : --------- Turn ON/OFF ALL toggles -------------------------
        if(user_input.upper() == the_all_on_button):
            tag_manager(menu_toggle_items, True, tag_arg_set)
        elif(user_input.upper() == the_all_off_button):
            tag_manager(menu_toggle_items, False, tag_arg_set)

        # [2] :  -------- 2. Adjust IP Address (Target Address)  -----------------------------
        elif(user_input == retrieve_module_index('Edit Target', preferred_order)):
            address = input(menu[user_input]["start_msg"])
            reg_string = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
            if(address == 'exit'):
                print('Exiting')
            elif(re.match(reg_string, address)):
                nmap_obj["ip"] = address
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