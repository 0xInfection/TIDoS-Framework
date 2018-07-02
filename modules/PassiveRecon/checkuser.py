#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework

# WARNING : may return false positives

import requests
import json
import time
import urllib
from colors import *		

def check0x00(alias):
	
	print GR+" [*] Searching alias "+O+alias+GR+" on 160 websites...\n"
	print GR+' [¬] Result : \n'
	headers = {'X-Requested-With':'XMLHttpRequest'}
	for service in services:  
		try:
			url = 'http://checkusernames.com/usercheckv2.php?target=' + service + '&username=' + alias
			req = requests.get(url, headers = headers)
			if 'notavailable' in req.text: 
			#if req.content.split('|')[0] == '2': #found
				print G+' [+] Found '+O+alias+G+' : '+GR+service 
		except Exception as e:
			print R+' [-] Incurred Exception : '+str(e) 


def checkuser(web):

	print GR+' [*] Loading module...'
	time.sleep(0.6)
	print R+'\n    ======================='
	print R+'     C H E C K   A L I A S'
	print R+'    =======================\n'

	print GR+' [*] Parsing Url...'
	web = web.replace('https://','')
	web = web.replace('http://','')
	web = web.split('.')[0]
	print G+' [+] Alias Set : '+web
	print O+' [*] Setting services...'
	time.sleep(0.7)
	global services
	services = ['YouTube', 'Hypemachine', 'Yahoo', 'Linkagogo', 'Coolspotters', 'Wikipedia', 'Twitter', 'gdgt', 'BlogMarks', 'LinkedIn', 'Ebay', 'Tumblr', 'Pinterest','yotify', 'Blogger', 'Flickr', 'FortyThreeMarks,Moof', 'HuffingtonPost', 'Wordpress', 'DailyMotion', 'LiveJournal', 'vimeo', 'DeviantArt', 'reddit','StumbleUpon', 'Answers', 'Sourceforge', 'Wikia', 'ArmChairGM', 'Photobucket', 'MySpace', 'Etsy,SlideShare', 'Fiverr', 'scribd', 'Squidoo', 'ImageShack','ThemeForest', 'SoundCloud', 'Tagged', 'Hulu', 'Typepad', 'Hubpages', 'weebly', 'Zimbio', 'github', 'TMZ', 'WikiHow', 'Delicious', 'zillow', 'Jimdo', 'goodreads','Segnalo', 'Netlog', 'Issuu', 'ForumNokia', 'UStream', 'Gamespot', 'MetaCafe', 'askfm', 'hi5', 'JustinTV', 'Blekko', 'Skyrock', 'Cracked', 'foursquare', 'LastFM','posterous', 'steam', 'Opera', 'Dreamstime', 'Fixya', 'UltimateGuitar', 'docstoc', 'FanPop', 'Break', 'tinyurl', 'Kongregate', 'Disqus', 'Armorgames', 'Behance','ChaCha', 'CafeMom', 'Liveleak', 'Topix', 'lonelyplanet', 'Stardoll', 'Instructables', 'Polyvore', 'Proboards', 'Weheartit', 'Diigo', 'Gawker', 'FriendFeed','Videobash', 'Technorati', 'Gravatar', 'Dribbble', 'formspringme', 'myfitnesspal', '500px', 'Newgrounds', 'GrindTV', 'smugmug', 'ibibo', 'ReverbNation', 'Netvibes','Slashdot', 'Fool', 'Plurk', 'zedge', 'Discogs', 'YardBarker', 'Ebaumsworld', 'sparkpeople', 'Sharethis', 'Xmarks', 'Crunchbase', 'FunnyOrDie,Suite101', 'OVGuide','Veoh', 'Yuku', 'Experienceproject', 'Fotolog', 'Hotklix', 'Epinions', 'Hyves', 'Sodahead', 'Stylebistro', 'fark', 'AboutMe', 'Metacritic', 'Toluna', 'Mobypicture','Gather', 'Datpiff', 'mouthshut', 'blogtalkradio', 'Dzone', 'APSense', 'Bigstockphoto', 'n4g', 'Newsvine', 'ColourLovers', 'Icanhazcheezburger', 'Xanga','InsaneJournal', 'redbubble', 'Kaboodle', 'Folkd', 'Bebo', 'Getsatisfaction', 'WebShots', 'threadless', 'Active', 'GetGlue', 'Shockwave', 'Pbase']
	print O+' [!] Loaded '+GR+str(len(services))+O+' services...'
	check0x00(web)	

