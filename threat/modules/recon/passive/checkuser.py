
#!/usr/bin/env python
from core.colors import color
from database.database_module import save_data
import inspect


# import os
import tld
import requests
import threading
# import json
# import time
# import urllib

tasks=[]
data = []
headers = {'X-Requested-With':'XMLHttpRequest'}

def thread(url,service,hostname):
    try:
        req = requests.get(url, headers = headers)
        if 'notavailable' in req.text:
            print(' [+] Found '+hostname+' : '+service)
            data.append(service)
    except Exception as e:
        print(color.red(' [-] Incurred Exception : '+str(e)))

def check0x00(host):
    for user in host.usernames:
        for service in services:
            url = 'http://checkusernames.com/usercheckv2.php?target=' + service + '&username=' + user
            check = threading.Thread(target=thread,args=(url,service,host.name))
            tasks.append(check)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()    
        #print(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
        save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(data))

def checkuser(target):
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        if len(host.usernames):
            print(' [*] Parsing Url...')
            #web0 = tld.get_fld(host.name).split('.', 1)[0]
            print(color.green(' [+] Alias Set : '+str(host.usernames)))
            print(color.yellow(' [*] Setting services...'))
            global services
            services = ['YouTube', 'Hypemachine', 'Yahoo', 'Linkagogo', 'Coolspotters', 'Wikipedia',\
                'Twitter', 'gdgt', 'BlogMarks', 'LinkedIn', 'Ebay', 'Tumblr', 'Pinterest','yotify',\
                'Blogger', 'Flickr', 'FortyThreeMarks','Moof', 'HuffingtonPost', 'Wordpress',\
                'DailyMotion', 'LiveJournal', 'vimeo', 'DeviantArt', 'reddit','StumbleUpon',\
                'Answers', 'Sourceforge', 'Wikia', 'ArmChairGM', 'Photobucket', 'MySpace',\
                'Etsy','SlideShare', 'Fiverr', 'scribd', 'Squidoo', 'ImageShack','ThemeForest',\
                'SoundCloud', 'Tagged', 'Hulu', 'Typepad', 'Hubpages', 'weebly', 'Zimbio', 'github',\
                'TMZ', 'WikiHow', 'Delicious', 'zillow', 'Jimdo', 'goodreads','Segnalo', 'Netlog',\
                'Issuu', 'ForumNokia', 'UStream', 'Gamespot', 'MetaCafe', 'askfm', 'hi5', 'JustinTV',\
                'Blekko', 'Skyrock', 'Cracked', 'foursquare', 'LastFM','posterous', 'steam', 'Opera',\
                'Dreamstime', 'Fixya', 'UltimateGuitar', 'docstoc', 'FanPop', 'Break', 'tinyurl',\
                'Kongregate', 'Disqus', 'Armorgames', 'Behance','ChaCha', 'CafeMom', 'Liveleak',\
                'Topix', 'lonelyplanet', 'Stardoll', 'Instructables', 'Polyvore', 'Proboards',\
                'Weheartit', 'Diigo', 'Gawker', 'FriendFeed','Videobash', 'Technorati', 'Gravatar',\
                'Dribbble', 'formspringme', 'myfitnesspal', '500px', 'Newgrounds', 'GrindTV',\
                'smugmug', 'ibibo', 'ReverbNation', 'Netvibes','Slashdot', 'Fool', 'Plurk',\
                'zedge', 'Discogs', 'YardBarker', 'Ebaumsworld', 'sparkpeople', 'Sharethis',\
                'Xmarks', 'Crunchbase', 'FunnyOrDie','Suite101', 'OVGuide','Veoh', 'Yuku',\
                'Experienceproject', 'Fotolog', 'Hotklix', 'Epinions', 'Hyves', 'Sodahead',\
                'Stylebistro', 'fark', 'AboutMe', 'Metacritic', 'Toluna', 'Mobypicture','Gather',\
                'Datpiff', 'mouthshut', 'blogtalkradio', 'Dzone', 'APSense', 'Bigstockphoto', 'n4g',\
                'Newsvine', 'ColourLovers', 'Icanhazcheezburger', 'Xanga','InsaneJournal', 'redbubble',\
                'Kaboodle', 'Folkd', 'Bebo', 'Getsatisfaction', 'WebShots', 'threadless', 'Active',\
                'GetGlue', 'Shockwave', 'Pbase', 'FaceBook', 'Instagram', 'Myspace']
            print(color.yellow(' [!] Loaded ')+color.green(str(len(services)))+color.yellow(' services...'))
            check0x00(host)
