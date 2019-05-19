#!/usr/bin/env python
import os
import sys
from multiprocessing import Lock, Process, Queue, current_process
import time
import queue # imported for using queue.Empty exception
from threat import processes, tasks_that_are_done, tasks_to_accomplish
from .colors import color


NUM_WORKERS = 4#multiprocessing.cpu_count()

sys.path.append(os.path.abspath('.'))

# main menus
from modules.recon.recon import recon
from modules.enumeration.scanenum import scanenum
from modules.exploitation.exploitation import exploitation
from modules.vulnysis.vulnysis import vulnysis
from modules.database.db_menu import db_menu
from modules.post.post_exploitation import post_exploitation

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

# enumeration
from modules.enumeration.nikto import nikto
from modules.enumeration.windows_enum import windows_enum
from modules.enumeration.windows.enum4linux import enum4linux
from modules.enumeration.nmap_menu import nmap_menu

# database
from modules.database.database_module import get_info
# post / aux modules
# critical bugs
from modules.vulnysis.critical_bugs import critical
from modules.vulnysis.critical.lfi import lfi
from modules.vulnysis.critical.rfi import rfi
from modules.vulnysis.critical.ldap import ldap
from modules.vulnysis.critical.rce import rce
from modules.vulnysis.critical.csrf import csrf
from modules.vulnysis.critical.sqli import sqli
from modules.vulnysis.critical.crlf import crlf
from modules.vulnysis.critical.subdomover import subdomover
from modules.vulnysis.critical.strutsshock import strutsshock
from modules.vulnysis.critical.phpi import phpi
from modules.vulnysis.critical.htmli import htmli
from modules.vulnysis.critical.xpathi import xpathi
from modules.vulnysis.critical.shellshock import shellshock
from modules.vulnysis.critical.xss import xss
from modules.vulnysis.critical.openredirect import openredirect
from modules.vulnysis.critical.pathtrav import pathtrav

# misconfiguration
from modules.vulnysis.misconfig_bugs import misconfig
from modules.vulnysis.misconfig.icors import icors
from modules.vulnysis.misconfig.ssscript import ssscript
from modules.vulnysis.misconfig.clickjack import clickjack
from modules.vulnysis.misconfig.zone import zone
from modules.vulnysis.misconfig.hhi import hhi
from modules.vulnysis.misconfig.netmisc import netmisc
from modules.vulnysis.misconfig.cloudflaremisc import cloudflaremisc
from modules.vulnysis.misconfig.hsts import hsts
from modules.vulnysis.misconfig.sessionfix import sessionfix
from modules.vulnysis.misconfig.headers import headers
from modules.vulnysis.misconfig.xsstrace import xsstrace
from modules.vulnysis.misconfig.cookiecheck import cookiecheck
from modules.vulnysis.misconfig.mailspoof import mailspoof

# vuln others
from modules.vulnysis.other_bugs import other
from modules.vulnysis.other.popbrute import popbrute
from modules.vulnysis.other.ftpbrute import ftpbrute
from modules.vulnysis.other.sqlbrute import sqlbrute
from modules.vulnysis.other.sshbrute import sshbrute
from modules.vulnysis.other.smtpbrute import smtpbrute
from modules.vulnysis.other.xmppbrute import xmppbrute
from modules.vulnysis.other.telnetbrute import telnetbrute

# post
from modules.post.encodeall import encodeall
from modules.post.hashes import hashes
from modules.post.honeypot import honeypot
from modules.post.imgext import imgext

functions = {
    'recon':recon,
    'scanenum':scanenum,
    'exploitation':exploitation,
    'vulnysis':vulnysis,
    'db_menu':db_menu,
    #'post':post
    'post_exploitation':post_exploitation,

    # recon related
    'passive_recon':passive_recon,
    'active_recon':active_recon,
    'info_disclosure':info_disclosure,
    'nmap_menu':nmap_menu,
    #'dig':dig,
    #''

    # enumeration
    'windows_enum':windows_enum,

    # databased
    'get_info':get_info,
    #vuln
    'critical':critical,
    'misconfig':misconfig,
    'other':other,
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

    # enumeration
    'nikto':nikto,
    'enum4linux':enum4linux,

    #critical bugs
    'lfi':lfi,
    'rfi':rfi,
    'ldap':ldap,
    'rce':rce,
    'csrf':csrf,
    'sqli':sqli,
    'crlf':crlf,
    'subdomover':subdomover,
    'strutsshock':strutsshock,
    'phpi':phpi,
    'htmli':htmli,
    'xpathi':xpathi,
    #'shellshock':shellshock,
    'xss':xss,
    'openredirect':openredirect,
    'pathtrav':pathtrav,

    # misconfigurations
    'icors':icors,
    'ssscript':ssscript,
    'clickjack':clickjack,
    'zone':zone,
    'hhi':hhi,
    'netmisc':netmisc,
    'cloudflaremisc':cloudflaremisc,
    'hsts':hsts,
    'sessionfix':sessionfix,
    'headers':headers,
    'xsstrace':xsstrace,
    'cookiecheck':cookiecheck,
    'mailspoof':mailspoof,

    # other
    'popbrute':popbrute,
    'ftpbrute':ftpbrute,
    'sqlbrute':sqlbrute,
    'sshbrute':sshbrute,
    'smtpbrute':smtpbrute,
    'xmppbrute':xmppbrute,
    'telnetbrute':telnetbrute,

    # post
    'encodeall':encodeall,
    'hashes':hashes,
    'honeypot':honeypot,
    'imgext':imgext,

}


def do_job(func,tgt):#,tasks_to_accomplish, tasks_that_are_done):
    from core.build_menu import buildmenu
    '''
    TODO:
        1. buildmenu callback after multiprocess runs
    '''

    print('DO JOB')
    while True:
        try:
            '''
                try to get task from the queue. get_nowait() function will
                raise queue.Empty exception if the queue is empty.
                queue(False) function would do the same task also.
            '''
            #global processes
            #global tasks_to_accomplish

            menu = { # '#' : ['module', 'description', 'function']
                '1':['Reconnaissance & OSINT','Description','recon'],\
                '2':['Scanning & Enumeration','Description','scanenum'],\
                '3':['Vulnerability Analysis','Description','vulnysis'],\
                '4':['Exploitation','Description','exploitation'],\
                '5':['Post Analysis','Description','post'],\
                '6':['Access Data', 'Description', 'db_menu']
            }

            task = tasks_to_accomplish.get_nowait()
            p = Process(target=func, args=(tgt,))
            processes.append(p)
            print('PROCESSES', processes)
            print('PPPP', p)
            p.start()
            print('STARTED')
            buildmenu(tgt,menu,'Scanning and Enumeration','')          # build menu
        except queue.Empty:

            break
        else:
            '''
                if no exception has been raised, add the task completion
                message to task_that_are_done queue
            '''
            #global tasks_that_are_done
            tasks_that_are_done.put(task + ' is done by ' + current_process().name)
            time.sleep(.5)
    return True


def multi(func,tgt):
    print('MULTI')
    tasks_to_accomplish.put(str(func))

    # creating processes
    #for w in range(NUM_WORKERS):
        #p = Process(target=do_job, args=(func,tgt,tasks_to_accomplish, tasks_that_are_done))
    p = Process(target=do_job, args=(func,tgt))
    processes.append(p)
    print(color.green('INFO: Starting '+tgt[0].option))
    p.start()

    # completing process
    for p in processes:
        p.join()

    # print the output
    # while not tasks_that_are_done.empty():
    #     print(tasks_that_are_done.get())

    return True