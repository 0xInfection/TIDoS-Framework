#!/usr/bin/env python

target_name = "cmd_options"
# Function determines if incoming target is entire LIST or sub-object within LIST
def nmap_target_sorter(target):

    # Function takes a single dictionary object and processes it into a nmap string
    def nmap_string_builder(target):
        nmap_key_list = []
        nmap_command_list = []

        for key in target[target_name]:     # Extract all keys from nmap obj within TARGET
            nmap_key_list.append(key)
        for key in nmap_key_list:      # Associate all values from nmap obj into keys
            nmap_command_list.append([key, target[target_name][key]])

        # Create string
        string_list = ["nmap"]
        for command in nmap_command_list:
            if (command[1] == True):  # If value is True, only include the key into nmap string
                string_list.append(command[0])
            elif(command[1] != False): # If value is NOT False, include both key and value into string
                string_list.append(command[0])
                string_list.append(command[1])
        string_list.append(target["name"])
        return " ".join(string_list)

    # Same function as above, but receives Class Object
    def class_obj_string_builder(target):
        nmap_key_list = []
        nmap_command_list = []
        for key in target.cmd_options:
            nmap_key_list.append(key)
        for key in nmap_key_list:      # Associate all values from nmap obj into keys
            nmap_command_list.append([key, target.cmd_options[key]])

        # Create string
        string_list = ["nmap"]
        for command in nmap_command_list:
            if (command[1] == True):  # If value is True, only include the key into nmap string
                string_list.append(command[0])
            elif(command[1] != False): # If value is NOT False, include both key and value into string
                string_list.append(command[0])
                string_list.append(command[1])
        string_list.append(target.name)
        return " ".join(string_list)

    # Start of sorter function code
    result_list = []
    if (isinstance(target, list)): # If LIST, process all objects individually
        for each_obj in target:
            if("name" in each_obj):
                result_list.append(nmap_string_builder(each_obj))
    elif (isinstance(target, dict) & ("name" in target)): # If Dict, only process this
            result_list.append(nmap_string_builder(target))
    elif (isinstance(target, object)):
            result_list.append(class_obj_string_builder(target))
    return result_list[0]