# Which index number is each module?
def retrieve_module_index(invoked_module, orders):
    return str(orders.index(invoked_module) + 1)

# Tag manager can be used to create as many menu options pertaining to nmap tags that toggle on/off
def tag_manager(module_type, choice, set):
    order = set[0]
    params = set[1]
    menu = set[2]
    if (type(module_type) is list):
        for each_toggle in module_type:
            target_edit_index = retrieve_module_index(each_toggle, order)
            params[menu[target_edit_index]["tag"]] = choice
        if (choice):
            print('**** All toggle tags ON')
        else:
            print('**** All toggle tags OFF')     
        return True
    target_edit_index = retrieve_module_index(module_type, order)
    if(choice == target_edit_index):
        order_header = not params[menu[choice]["tag"]] # Reverse Boolean
        params[menu[choice]["tag"]] = order_header
        if(order_header == True):
            print(menu[choice]["on_msg"])
            return True
        elif(order_header == False):
            print(menu[choice]["off_msg"])
            return True
    else:
        return False

def list_create_and_dedupe(obj_key, obj, base_list, remove_these_list, full_menu):
    for each_menu_item in full_menu:
        if(obj_key in each_menu_item):
            base_list.append(each_menu_item[obj_key])
    for poss_dupes in base_list:
        if poss_dupes in remove_these_list:
            base_list.remove(poss_dupes)