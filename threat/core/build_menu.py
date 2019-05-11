#!/usr/bin/env python
import os
import sys
from .colors import color
from collections import OrderedDict
from .functions import functions, multiprocess_functions
from .process import multi

def exit():
    print(color.red(' [-] Exiting...'))
    sys.exit(0)

def build_banner(banner):
    size = len(banner)*2 + 4
    padding = "".join("=" for i in range(size))
    letters = "| "
    for letter in banner:
        letters = letters + color.yellow(letter.upper()) + " "
    letters = letters + color.blue(" |")
    print(color.blue(padding))
    print(color.blue(letters))
    print(color.blue(padding))

def buildmenu(target,dict,banner,art):
    #os.system('clear')
    print('TARGET', target[0].name)
    for each in target:
        each.last_menu = each.current_menu
        each.current_menu=dict
    dictionary = OrderedDict(sorted(dict.items(), key=lambda x: int(x[0])))
    i=1
    print(color.blue('[+] Module Selected : ') + color.yellow(banner))
    print(art)
    print(color.yellow(' Choose from the options below:\n'))
    for key, value in dictionary.items():
        print(color.green(' ['+str(i)+'] ') + color.blue(value[0]) + " - " + color.custom(value[1], white=True))
        i+=1
    if 'Main Menu' in banner:
        print('\n ' + color.custom('[0] Exit',bold=True,white=True,bg_red=True)+'\n')
    else:
        if not 'Temp if statement in case dont want to run all' in banner: # DEBUG: might want to not run all on a sub menu
            print('\n'+color.green(' [A] ') + color.yellow('Run all\n'))
        print(color.green(' [M] ') + color.yellow('Main Menu\n'))
        print(" " + color.custom('[B] Back',bold=True,white=True,bg_red=True)+'\n')

    choice = input('[#] Choose Option:> ')
    found = False
    if choice == '0': # exit
        exit()
    elif choice.lower() == 'b': # go back
        found = True
        buildmenu(target,target[0].last_menu,'','')
    elif choice.lower() == 'a':
        for key, value in dictionary.items():
            target[0].module = value[0]
            target[0].description = value[1]
            build_banner(value[0].replace('(','').replace(')',''))
            try:
                multi(multiprocess_functions[value[2]],target)
            except Exception as e:
                pass
            finally:
                pass
        found = True
    elif choice.lower() == 'm':
        found = True
        buildmenu(target,target[0].main_menu,'Main Menu','')
    else:
        for key, value in dictionary.items():
            if str(choice) == str(key): # select option
                target[0].module = value[0]
                target[0].description = value[1]
                if 'Temp if statement in case dont want to pass target' in banner: # DEBUG: Might use this option
                    results=functions[value[2]]
                else:
                    build_banner(value[0].replace('(','').replace(')',''))
                    mp = False
                    try:
                        multi(multiprocess_functions[value[2]],target)
                        mp = True
                    except Exception as e:
                        pass
                    finally:
                        pass
                    if mp ==False:
                        try:
                            results=functions[value[2]](target)
                        except Exception as e:
                            target[0].current_menu=target[0].last_menu
                            art=color.red('\nInvalid selection. ') + color.blue(value[0]) + color.red(' is not implemented yet.\n')
                            buildmenu(target,dict,banner,art)
                        finally:
                            pass
                found = True
                break

    if found == False:
        print(color.red('Invalid selection.'))
        pass
