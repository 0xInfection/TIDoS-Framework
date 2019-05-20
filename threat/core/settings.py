from threat import Target, target, menu
from core.colors import color

def add_host(target):
    host = input('[#] Input new host:> ')
    target.append(Target(host,menu,menu,menu,host))
    print(color.yellow(host+' added'))
    settings(target)

def add_email(target):
    email = input('[#] Input email address:> ')
    target[0].emails.append(email)
    print(color.yellow(email+' added'))
    settings(target)

def add_username(target):
    username = input('[#] Input username:> ')
    target[0].usernames.append(username)
    print(color.yellow(username+' added'))
    settings(target)

def settings(target):
    from core.build_menu import buildmenu
    hosts = []
    emails = []
    usernames = []
    for host in target:
        hosts.append(host.name)
        for email in host.emails:
            emails.append(email)
        for user in host.usernames:
            usernames.append(user)
    
    settings_menu = { # '#' : ['module', 'description', 'function']
        '1':['Add host',str(hosts),'add_host'],\
        '2':['Add email',str(emails),'add_email'],\
        '3':['Add username',str(usernames),'add_username'],\
        '4':['xxxx','xxx','xxx'],\
        '5':['xxxx','xxx','xxx'],\
        '6':['xxxx','xxx','xxx'],\
        '7':['xxxx','xxx','xxx'],\
        '8':['xxxx','xxx','xxx'],\
        '9':['xxxx','xxx','xxx'],\
        '10':['xxxx','xxx','xxx'],\
        '11':['xxxx','xxx','xxx'],\
        '12':['xxxx','xxx','xxx'],\
        '13':['xxxx','xxx','xxx'],\
        '14':['xxxx','xxx','xxx'],\
        '15':['xxxx','xxx','xxx'],\
    }
    target[0].settings_menu = settings_menu
    buildmenu(target,settings_menu,'Settings','')          # build menu