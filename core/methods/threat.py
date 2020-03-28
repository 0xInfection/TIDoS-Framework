from core.variables import database

class Target:
    #def __init__(self,name,current_menu,last_menu,main_menu,ip):
    def __init__(self,name,ip):
        self.name = name
        #self.current_menu = current_menu
        #self.last_menu = last_menu
        #self.main_menu = main_menu
        #self.settings_menu=''
        #self.lvl1 = ''
        #self.lvl2 = ''
        #self.lvl3 = ''
        #self.module = ''
        self.description = ''
        self.ip = ip
        self.port = ''
        #self.cmd_options = {}
        #self.nmap = ''
        self.lvl = 0
        self.last_lvl=0
        self.database = database
        #self.option = ''
        #self.dork=''
        #self.help = ''
        #self.options_list = ''
        #self.options_str = ''
        #self.cmd_str = ''
        self.usernames=[]
        self.emails=[]
        self.website = ''
        #self.run_file = ''
        self.urluser = ''
        self.urlpasswd = ''
        self.fullurl = ''

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value 
