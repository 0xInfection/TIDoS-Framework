from modules.database.database_module import get_info, retrieve_data
from core.colors import color
import sys

menu_dict = {
    'ReconANDOSINT' : 'Reconnaissance & OSINT', 
    'ScanANDEnum' : 'Scanning & Enumeration',
    'VulnAnalysis' : 'Vulnerability Analysis',
    'Exploitation' : 'Exploitation',
    'AuxModules' : 'Auxiliary Modules'
    }
db_name = "modules/database/tidos.db"
query_list = [db_name]
error_message = "Sorry, please enter one of the choices listed."
menu_message = "Please make your selection: "
input_cursor = "[#] Choose Option:> "
main_exit_message = color.green('\n [M] ') + color.yellow('Main Menu\n')
higher_menu_exit_message = color.green('\n [0] ') + color.yellow('Exit to higher menu')
exit_message = "Now exiting. Goodbye."

def build_banner(banner):
    size = len(banner)*2 + 4
    padding = "".join("=" for i in range(size))
    letters = "| "
    for letter in banner:
        letters = letters + color.yellow(letter.upper()) + " "
    letters = letters + color.blue(" |")
    print("\n")
    print(color.blue(padding))
    print(color.blue(letters))
    print(color.blue(padding))
    print("\n")

def query_db(query_list):
    db, module, lvl1 = query_list[0], query_list[1], query_list[2]
    if len(query_list) == 4:
        lvl2, lvl3, num = "", "", query_list[3]
    elif len(query_list) == 5:
        lvl2, lvl3, num = query_list[3], "", query_list[4]
    else:
        lvl2, lvl3, num = query_list[3], query_list[4], query_list[5]
    retrieved_data = retrieve_data(db, module, lvl1, lvl2, lvl3, num)
    print("Target: " + str(retrieved_data[0][0]))
    print("Data  : " + str(retrieved_data[0][1]))

def build_db_menu(a_list, b_list, selection, target):
    from core.build_menu import buildmenu
    if selection == "None":
        build_banner("Access Data")
    else:
        build_banner(query_list[-1])
    while True:
        ctr = 0
        while ctr < len(a_list):
            if "Data" in selection.values():
                print(color.green(' ['+str(ctr + 1)+'] ') + color.blue(str(a_list[ctr])))
            elif b_list != "None":
                print(color.green(' ['+str(ctr + 1)+'] ') + color.blue(b_list[ctr]))
            else:
                print(color.green(' ['+str(ctr + 1)+'] ') + color.blue(a_list[ctr]))
            ctr += 1
        if selection != "None":
            print(higher_menu_exit_message)
        print(main_exit_message)
        cmd = input(input_cursor)
        if cmd.lower() == "m":
            found = True
            buildmenu(target,target[0].main_menu,'Main Menu','')
        elif cmd == "0":
            del query_list[-1]
            return cmd
        elif int(cmd) <= len(a_list):
            query_list.append(a_list[int(cmd) - 1])
            if selection == "None":
                return a_list[int(cmd) - 1]
            elif selection[a_list[int(cmd) - 1]] == "Data":
                query_db(query_list)
                del query_list[-1]
            else:
                return a_list[int(cmd) - 1]
        else:
            print(error_message)
                
def level_five_menu(choice1, choice2, choice3, choice4, menu_data, target):
    a_list = list(menu_data[choice1][choice2][choice3][choice4].keys())
    selection = menu_data[choice1][choice2][choice3][choice4]
    result = build_db_menu(a_list, "None", selection, target)
    if result == "0":
        level_four_menu(choice1, choice2, choice3, menu_data, target)

def level_four_menu(choice1, choice2, choice3, menu_data, target):
    a_list = list(menu_data[choice1][choice2][choice3].keys())
    selection = menu_data[choice1][choice2][choice3]
    result = build_db_menu(a_list, "None", selection, target)
    if result == "0":
        level_three_menu(choice1, choice2, menu_data, target)
    else:
        level_five_menu(choice1, choice2, choice3, result, menu_data, target)

def level_three_menu(choice1, choice2, menu_data, target):
    a_list = list(menu_data[choice1][choice2].keys())
    selection = menu_data[choice1][choice2]
    result = build_db_menu(a_list, "None", selection, target)
    if result == "0":
        level_two_menu(choice1, menu_data, target)
    else:
        level_four_menu(choice1, choice2, result, menu_data, target)

def level_two_menu(choice, menu_data, target):
    a_list = list(menu_data[choice].keys())
    selection = menu_data[choice]
    result = build_db_menu(a_list, "None", selection, target)
    if result == "0":
        db_menu(target)
    else:
        level_three_menu(choice, result, menu_data, target)

def db_menu(target):
    menu_data = get_info(db_name)
    a_list = list(menu_data.keys())
    b_list = []
    for item in a_list:
        b_list.append(menu_dict[item])
    result = build_db_menu(a_list, b_list, menu_data, target)
    level_two_menu(result, menu_data, target)