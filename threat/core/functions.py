#!/usr/bin/env python
import os
import sys

sys.path.append(os.path.abspath('.'))

# main menus
from modules.recon.recon import recon
from modules.enumeration.scanenum import scanenum
from modules.exploitation.exploitation import exploitation
from modules.vulnysis.vulnysis import vulnysis

# passive recon
from modules.recon.passive_recon import passive_recon
from modules.recon.passive.dig import dig
from modules.recon.passive.whois import whois
from modules.recon.passive.nping import nping
from modules.recon.passive.getgeoip import getgeoip
from modules.recon.passive.iphistory import iphistory
from modules.recon.passive.revdns import revdns
from modules.recon.passive.revip import revip
from modules.recon.passive.subnet import subnet
from modules.recon.passive.linkedin import linkedin
from modules.recon.passive.gsearch import gsearch
from modules.recon.passive.censysdom import censysdom
from modules.recon.passive.checkuser import checkuser
from modules.recon.passive.getconinfo import getconinfo
from modules.recon.passive.googledorker import googledorker
from modules.recon.passive.googlegroups import googlegroups
from modules.recon.passive.googlenum import googlenum
from modules.recon.passive.googleSearch import googleSearch
from modules.recon.passive.hackedmail import hackedmail
from modules.recon.passive.links import links
from modules.recon.passive.mailtodom import mailtodom
from modules.recon.passive.pastebin import pastebin
from modules.recon.passive.piweb import piweb
from modules.recon.passive.threatintel import threatintel
from modules.recon.passive.webarchive import webarchive

# active recon
from modules.recon.active_recon import active_recon
from modules.recon.active.piwebenum import piwebenum
from modules.recon.active.grabhead import grabhead
from modules.recon.active.httpmethods import httpmethods
from modules.recon.active.robot import robot
from modules.recon.active.apachestat import apachestat
from modules.recon.active.dav import dav
from modules.recon.active.sharedns import sharedns
from modules.recon.active.commentssrc import commentssrc
from modules.recon.active.sslcert import sslcert
from modules.recon.active.filebrute import filebrute
from modules.recon.active.traceroute import traceroute
from modules.recon.active.phpinfo import phpinfo
from modules.recon.active.cms import cms
from modules.recon.active.serverdetect import serverdetect
from modules.recon.active.altsites import altsites

#info disclosure
from modules.recon.infodisc import info_disclosure
from modules.recon.info.creditcards import creditcards
from modules.recon.info.emailtext import emailtext
from modules.recon.info.errors import errors
from modules.recon.info.internalip import internalip
from modules.recon.info.phone import phone
from modules.recon.info.ssn import ssn

functions = {
    'recon':recon,
    'scanenum':scanenum,
    'exploitation':exploitation,
    'vulnysis':vulnysis,
    #'post':post

    # recon related
    'passive_recon':passive_recon,
    'active_recon':active_recon,
    'info_disclosure':info_disclosure,

    #'dig':dig,
    #''
}

multiprocess_functions = {
    # passive recon
    'dig':dig,
    'whois':whois,
    'nping':nping,
    'getgeoip':getgeoip,
    'iphistory':iphistory,
    'revdns':revdns,
    'revip':revip,
    'subnet':subnet,
    'linkedin':linkedin,
    'gsearch':gsearch,
    'censysdom':censysdom,
    'checkuser':checkuser,
    'getconinfo':getconinfo,
    'googledorker':googledorker,
    'googlegroups':googlegroups,
    'googlenum':googlenum,
    'googleSearch':googleSearch,
    'hackedmail':hackedmail,
    'links':links,
    'mailtodom':mailtodom,
    'pastebin':pastebin,
    'piweb':piweb,
    'threatintel':threatintel,
    'webarchive':webarchive,

    # active recon
    'piwebenum':piwebenum,
    'grabhead':grabhead,
    'httpmethods':httpmethods,
    'robot':robot,
    'apachestat':apachestat,
    'dav':dav,
    'sharedns':sharedns,
    'commentssrc':commentssrc,
    'sslcert':sslcert,
    'filebrute':filebrute,
    'traceroute':traceroute,
    'phpinfo':phpinfo,
    'cms':cms,
    'serverdetect':serverdetect,
    'altsites':altsites,
    #information disclosure
    'creditcards':creditcards,
    'emailtext':emailtext,
    'errors':errors,
    'internalip':internalip,
    'phone':phone,
    'ssn':ssn,

}