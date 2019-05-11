
#!/usr/bin/env python
from core.colors import color
def checkuser(target):
    print('This module is not yet available.')
    pass
    # #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author: @_tID
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# # WARNING : may return false positives

# from __future__ import print_function
# import os
# import tld
# import requests
# import json
# import time
# import urllib
# from core.Core.colors import *
# serv = []

# def check0x00(alias,web):

#     print(GR+" [*] Searching alias "+O+alias+GR+" on 160 websites...\n")
#     print(GR+' [¬] Result : \n')
#     headers = {'X-Requested-With':'XMLHttpRequest'}

#     for service in services:
#         try:
#             url = 'http://checkusernames.com/usercheckv2.php?target=' + service + '&username=' + alias
#             req = requests.get(url, headers = headers)
#             if 'notavailable' in req.text:
#             #if req.content.split('|')[0] == '2': #found
#                 print(GR+' [+] Found '+O+alias+G+' : '+C+service)
#                 serv.append(service)

#         except Exception as e:
#             print(R+' [-] Incurred Exception : '+str(e))

#     if 'http://' in web.strip():
#         po = web.replace('http://','')
#     elif 'https://' in web.strip():
#         po = web.replace('https://','')
#     p = 'tmp/logs/'+po+'-logs/'+str(po)+'-usernames.lst'
#     open(p,'w+')
#     print(B+' [!] Saving links...')
#     time.sleep(1)
#     for m in serv:
#         m = 'Social Network : ' + m + '\n'
#         ile = open(p,"a")
#         ile.write(m)
#         ile.close()
#     pa = os.getcwd()
#     print(G+' [+] Links saved under '+pa+'/'+p+'!')
#     print('')

# def checkuser(web):

#     print(GR+' [*] Loading module...')
#     time.sleep(0.6)
#     print(R+'\n    =======================')
#     print(R+'     C H E C K   A L I A S')
#     print(R+'    =======================\n')

#     print(GR+' [*] Parsing Url...')
#     web0 = tld.get_fld(web).split('.', 1)[0]
#     print(G+' [+] Alias Set : '+web0)
#     print(O+' [*] Setting services...')
#     time.sleep(0.7)
#     global services
#     services = ['YouTube', 'Hypemachine', 'Yahoo', 'Linkagogo', 'Coolspotters', 'Wikipedia', 'Twitter', 'gdgt', 'BlogMarks', 'LinkedIn', 'Ebay', 'Tumblr', 'Pinterest','yotify', 'Blogger', 'Flickr', 'FortyThreeMarks,Moof', 'HuffingtonPost', 'Wordpress', 'DailyMotion', 'LiveJournal', 'vimeo', 'DeviantArt', 'reddit','StumbleUpon', 'Answers', 'Sourceforge', 'Wikia', 'ArmChairGM', 'Photobucket', 'MySpace', 'Etsy,SlideShare', 'Fiverr', 'scribd', 'Squidoo', 'ImageShack','ThemeForest', 'SoundCloud', 'Tagged', 'Hulu', 'Typepad', 'Hubpages', 'weebly', 'Zimbio', 'github', 'TMZ', 'WikiHow', 'Delicious', 'zillow', 'Jimdo', 'goodreads','Segnalo', 'Netlog', 'Issuu', 'ForumNokia', 'UStream', 'Gamespot', 'MetaCafe', 'askfm', 'hi5', 'JustinTV', 'Blekko', 'Skyrock', 'Cracked', 'foursquare', 'LastFM','posterous', 'steam', 'Opera', 'Dreamstime', 'Fixya', 'UltimateGuitar', 'docstoc', 'FanPop', 'Break', 'tinyurl', 'Kongregate', 'Disqus', 'Armorgames', 'Behance','ChaCha', 'CafeMom', 'Liveleak', 'Topix', 'lonelyplanet', 'Stardoll', 'Instructables', 'Polyvore', 'Proboards', 'Weheartit', 'Diigo', 'Gawker', 'FriendFeed','Videobash', 'Technorati', 'Gravatar', 'Dribbble', 'formspringme', 'myfitnesspal', '500px', 'Newgrounds', 'GrindTV', 'smugmug', 'ibibo', 'ReverbNation', 'Netvibes','Slashdot', 'Fool', 'Plurk', 'zedge', 'Discogs', 'YardBarker', 'Ebaumsworld', 'sparkpeople', 'Sharethis', 'Xmarks', 'Crunchbase', 'FunnyOrDie,Suite101', 'OVGuide','Veoh', 'Yuku', 'Experienceproject', 'Fotolog', 'Hotklix', 'Epinions', 'Hyves', 'Sodahead', 'Stylebistro', 'fark', 'AboutMe', 'Metacritic', 'Toluna', 'Mobypicture','Gather', 'Datpiff', 'mouthshut', 'blogtalkradio', 'Dzone', 'APSense', 'Bigstockphoto', 'n4g', 'Newsvine', 'ColourLovers', 'Icanhazcheezburger', 'Xanga','InsaneJournal', 'redbubble', 'Kaboodle', 'Folkd', 'Bebo', 'Getsatisfaction', 'WebShots', 'threadless', 'Active', 'GetGlue', 'Shockwave', 'Pbase']
#     print(O+' [!] Loaded '+GR+str(len(services))+O+' services...')
#     check0x00(web0,web)
