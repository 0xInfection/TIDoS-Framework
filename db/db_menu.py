from database_module import get_info, retrieve_data
import sys

menu_dict = {
    'ReconANDOSINT' : 'Reconnaissance & OSINT', 
    'ScanANDEnum' : 'Scanning & Enumeration',
    'VulnAnalysis' : 'Vulnerability Analysis',
    'Exploitation' : 'Exploitation',
    'AuxModules' : 'Auxiliary Modules'
    }
db_name = "sessionresults.db"
query_list = [db_name]
error_message = "Sorry, please enter one of the choices listed."
menu_message = "Please make your selection: "
input_cursor = "Input > "
main_exit_message = "E) Exit."
higher_menu_exit_message = "0) Exit to higher menu."
exit_message = "Now exiting. Goodbye."

def query_db(query_list):
    db, module, lvl1 = query_list[0], query_list[1], query_list[2]
    if len(query_list) == 4:
        lvl2, lvl3, num = "", "", query_list[3]
    elif len(query_list) == 5:
        lvl2, lvl3, num = query_list[3], "", query_list[4]
    else:
        lvl2, lvl3, num = query_list[3], query_list[4], query_list[5]
    print(retrieve_data(db, module, lvl1, lvl2, lvl3, num))

def build_db_menu(a_list, b_list, selection):
    print(menu_message)
    while True:
        ctr = 0
        while ctr < len(a_list):
            if selection == "Data":
                print("{}) Scan {}".format(str(ctr + 1), a_list[ctr]))
            elif b_list != "None":
                print("{}) {}".format(str(ctr + 1), b_list[ctr]))
            else:
                print("{}) {}".format(str(ctr + 1), a_list[ctr]))
            ctr += 1
        if selection != "None":
            print(higher_menu_exit_message)
        print(main_exit_message)
        cmd = input(input_cursor)
        if cmd == "e" or cmd == "E" or cmd == "exit" or cmd == "Exit" or cmd == "EXIT":
            print(exit_message)
            sys.exit()
        elif cmd == "0":
            del query_list[-1]
            return cmd
        elif int(cmd) <= len(a_list):
            query_list.append(a_list[int(cmd) - 1])
            if selection == "None":
                return a_list[int(cmd) - 1]
            elif selection[a_list[int(cmd) - 1]] == "Data":
                print(selection[a_list[int(cmd) - 1]])
                query_db(query_list)
                del query_list[-1]
            else:
                return a_list[int(cmd) - 1]
        else:
            print(error_message)

def level_five_menu(choice1, choice2, choice3, choice4, menu_data):
    a_list = list(menu_data[choice1][choice2][choice3][choice4].keys())
    selection = menu_data[choice1][choice2][choice3][choice4]
    result = build_db_menu(a_list, "None", selection)
    if result == "0":
        level_four_menu(choice1, choice2, choice3, menu_data)

def level_four_menu(choice1, choice2, choice3, menu_data):
    a_list = list(menu_data[choice1][choice2][choice3].keys())
    selection = menu_data[choice1][choice2][choice3]
    result = build_db_menu(a_list, "None", selection)
    if result == "0":
        level_three_menu(choice1, choice2, menu_data)
    else:
        level_five_menu(choice1, choice2, choice3, result, menu_data)

def level_three_menu(choice1, choice2, menu_data):
    a_list = list(menu_data[choice1][choice2].keys())
    selection = menu_data[choice1][choice2]
    result = build_db_menu(a_list, "None", selection)
    if result == "0":
        level_two_menu(choice1, menu_data)
    else:
        level_four_menu(choice1, choice2, result, menu_data)
    
def level_two_menu(choice, menu_data):
    a_list = list(menu_data[choice].keys())
    selection = menu_data[choice]
    result = build_db_menu(a_list, "None", selection)
    if result == "0":
        menu(menu_data)
    else:
        level_three_menu(choice, result, menu_data)

def menu(menu_data):
    a_list = list(menu_data.keys())
    b_list = []
    for item in a_list:
        b_list.append(menu_dict[item])
    result = build_db_menu(a_list, b_list, "None")
    level_two_menu(result, menu_data)
    
menu_data = get_info(db_name)
menu(menu_data)