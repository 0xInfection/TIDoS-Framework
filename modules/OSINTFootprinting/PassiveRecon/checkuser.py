#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

# WARNING : may return false positives


import os, time
import tld
import threading
from core.methods.tor import session
from core.Core.colors import *

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

tasks=[]
data = []
headers = {'X-Requested-With':'XMLHttpRequest'}

info = "Alias Check"
searchinfo = "Alias Check"
properties = {}


def thread(url,service,hostname):
    try:
        requests = session()
        req = requests.get(url, headers = headers)
        if 'notavailable' in req.text:
            print(' [+] Found '+hostname+' : '+service)
            data.append(service)
    except Exception as e:
        print(R+' [-] Incurred Exception : '+str(e))

def check0x00(host, lvl2):
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl3 = ""
    for user in host.usernames:
        print(GR+" [*] Searching alias "+O+user+GR+" on " + str(len(services)) + " websites...\n")
        for service in services:
            url = 'http://checkusernames.com/usercheckv2.php?target=' + service + '&username=' + user
            #check = threading.Thread(target=thread,args=(url,service,host.name))
            check = threading.Thread(target=thread,args=(url,service,user))
            tasks.append(check)
    print(GR+' [¬] Result : \n')
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()
    
        #print(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)
    save_data(database, module, lvl1, lvl2, lvl3, host.fullurl, str(data))


def checkuser(web):

    time.sleep(0.6)
    #print(R+'\n    =======================')
    #print(R+'     C H E C K   A L I A S')
    #print(R+'    =======================\n')
    from core.methods.print import posintpas
    posintpas("check alias") 
    
    if len(web.usernames) < 1:
        print(" [!] No usernames have been set for target {}".format(web.fullurl))
        a = "a"
        while a != "":
            a = input(" [§] Add username (enter if done) :> ")
            if a != "":
                web.usernames.append(a)
    
    time.sleep(0.7)
    global services
    services = ['YouTube', 'Hypemachine', 'Yahoo', 'Linkagogo', 'Coolspotters', 'Wikipedia', 'Twitter', 'gdgt', 'BlogMarks', 'LinkedIn', 'Ebay', 'Tumblr', 'Pinterest','yotify', 'Blogger', 'Flickr', 'FortyThreeMarks,Moof', 'HuffingtonPost', 'Wordpress', 'DailyMotion', 'LiveJournal', 'vimeo', 'DeviantArt', 'reddit','StumbleUpon', 'Answers', 'Sourceforge', 'Wikia', 'ArmChairGM', 'Photobucket', 'MySpace', 'Etsy,SlideShare', 'Fiverr', 'scribd', 'Squidoo', 'ImageShack','ThemeForest', 'SoundCloud', 'Tagged', 'Hulu', 'Typepad', 'Hubpages', 'weebly', 'Zimbio', 'github', 'TMZ', 'WikiHow', 'Delicious', 'zillow', 'Jimdo', 'goodreads','Segnalo', 'Netlog', 'Issuu', 'ForumNokia', 'UStream', 'Gamespot', 'MetaCafe', 'askfm', 'hi5', 'JustinTV', 'Blekko', 'Skyrock', 'Cracked', 'foursquare', 'LastFM','posterous', 'steam', 'Opera', 'Dreamstime', 'Fixya', 'UltimateGuitar', 'docstoc', 'FanPop', 'Break', 'tinyurl', 'Kongregate', 'Disqus', 'Armorgames', 'Behance','ChaCha', 'CafeMom', 'Liveleak', 'Topix', 'lonelyplanet', 'Stardoll', 'Instructables', 'Polyvore', 'Proboards', 'Weheartit', 'Diigo', 'Gawker', 'FriendFeed','Videobash', 'Technorati', 'Gravatar', 'Dribbble', 'formspringme', 'myfitnesspal', '500px', 'Newgrounds', 'GrindTV', 'smugmug', 'ibibo', 'ReverbNation', 'Netvibes','Slashdot', 'Fool', 'Plurk', 'zedge', 'Discogs', 'YardBarker', 'Ebaumsworld', 'sparkpeople', 'Sharethis', 'Xmarks', 'Crunchbase', 'FunnyOrDie,Suite101', 'OVGuide','Veoh', 'Yuku', 'Experienceproject', 'Fotolog', 'Hotklix', 'Epinions', 'Hyves', 'Sodahead', 'Stylebistro', 'fark', 'AboutMe', 'Metacritic', 'Toluna', 'Mobypicture','Gather', 'Datpiff', 'mouthshut', 'blogtalkradio', 'Dzone', 'APSense', 'Bigstockphoto', 'n4g', 'Newsvine', 'ColourLovers', 'Icanhazcheezburger', 'Xanga','InsaneJournal', 'redbubble', 'Kaboodle', 'Folkd', 'Bebo', 'Getsatisfaction', 'WebShots', 'threadless', 'Active', 'GetGlue', 'Shockwave', 'Pbase']
    print(C+' [!] Loaded '+str(len(services))+' services...')
    lvl2 = inspect.stack()[0][3]
    
    check0x00(web, lvl2)

def attack(web):
    checkuser(web)
