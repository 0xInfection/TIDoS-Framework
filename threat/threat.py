#!/usr/bin/env python
import sys
import requests
from multiprocessing import Process, Queue, current_process
from core.build_menu import buildmenu

# menu = { # '#' : ['module', 'description', 'function']
#         '1':['Reconnaissance & OSINT','Description','recon'],\
#         '2':['Scanning & Enumeration','Description','scanenum'],\
#         '3':['Vulnerability Analysis','Description','vulnysis'],\
#         '4':['Exploitation','Description','exploitation'],\
#         '5':['Post Analysis','Description','post']\
#     }

# target=[]

menu_options = [
    '1. Add a domain name\n'
    '2. Start processing queue\n',
    '3. Stop processing queue\n',
    '4. Display logs\n',
    '5. Exit'
]

domain_list = [
    'https://devleague.com'
]

NUM_WORKERS = 4

done_queue = Queue()  # This is messages from the child processes for parent
process_queue = Queue()  # This is the domains to process


def scraper(process_queue, done_queue):
  done_queue.put("{} starting".format(current_process().name))
  for domain in iter(process_queue.get, 'STOP'):
    print('\nScraping Domain: ', domain)
    result = requests.get(domain)
    done_queue.put("{}: Domain {} retrieved with {} bytes".format(current_process().name, domain, len(result.text)))
    print("{}: Domain {} retrieved with {} bytes".format(current_process().name, domain, len(result.text)))

# class Target:
#     def __init__(self,name,current_menu,last_menu,main_menu):
#         self.name = name
#         self.current_menu = current_menu
#         self.last_menu = last_menu
#         self.main_menu = main_menu

# def threat():
#     while True:
#         try:
#             host = 'www.example.com'# DEBUG: temp value
#             current_menu = menu
#             last_menu = menu
#             target.append(Target(host,current_menu,last_menu,menu))
#             buildmenu(target,menu,'Main Menu','')
#         except KeyboardInterrupt:
#             print("Keyboard interrupted")
#         finally:
#             sys.exit()


def main(prompt):
  options_str = '\n'

  for options in menu_options:
    options_str += options
  print(options_str)

  while True:
    try:
      value = int(input(prompt))

      if value == 1:
        print('\nInput domain info below\n')

        domain_str = 'https://' + input('Domain Name: ')

        domain_list.append(domain_str)
        print('Domains: ', domain_list)

        main('Please select a process from the menu\n')

      if value == 2:
        print('\nStarting queue...\n')

        for domain in domain_list:
          process_queue.put(domain)
          print(domain, 'has been queued...')

        for i in range(NUM_WORKERS):
          Process(target=scraper, args=(process_queue, done_queue)).start()

        for message in iter(done_queue.get, 'STOP'):
          print(message)

      if value == 3:
        print('Stopping queue...')

        return value

      if value == 4:
        print('Logs below...')
        return value

      if value == 5:
        print('Exiting...')
        return value

    except ValueError:
      print('Please enter an integar')
      continue

    # if value not in (0, 6):
    #   print('Please select an option from the menu')
    #   continue
    # else:
    #   break

  print('VALUE', value)
  pass

# if __name__=='__main__':
#     try:
#         threat()
#     except KeyboardInterrupt:
#         print("Keyboard interrupted")
#     finally:
#         sys.exit()


if __name__ == "__main__":
  main('\nPlease select a process from the menu\n')
