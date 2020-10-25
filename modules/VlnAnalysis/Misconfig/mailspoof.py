#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import sys
import os, time
import core.lib.emailprotectionslib.dmarc as dmarclib
import core.lib.emailprotectionslib.spf as spflib
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module checks if target's mail is spoofable."
searchinfo = "Mail Spoofer"
properties = {}


def spfRedir0x00(spfrec):
    redirDom = spfrec.get_redirect_domain()

    if redirDom is not None:
        print(O+" [!] Processing an SPF redirect domain : " + str(redirDom) + '...')
        return spfStr0x00(redirDom)
    else:
        return False

def spfInclude0x00(spfrec):
    domInc = spfrec.get_include_domains()

    for domInclu in domInc:
        print((O+" [!] Processing an SPF include domain : %s" % domInclu) + '...')

        spfStro = spfStr0x00(domInclu)

        if spfStro:
            return True

    return False

def spfCheck0x00(spfrec):
    print(O+" [!] Checking SPF redirect domian : %(domain)s" % {"domain": spfrec.get_redirect_domain})
    redirStro = spfrec._is_redirect_mechanism_strong()
    if redirStro:
        print(R+" [-] SPF redirect mechanism is strong...")
    else:
        print(G+" [+] SPF redirect mechanism is not strong...")

    return redirStro


def spfInclStr0x00(spfrec):
    print(GR+" [*] Checking SPF include mechanisms...")
    incStro = spfrec._are_include_mechanisms_strong()
    if incStro:
        print(R+" [-] SPF include mechanisms include a strong record...")
    else:
        print(GR+" [-] SPF include mechanisms are not strong...")

    return incStro


def spfInc0x00(spfrec):
    othStr = False
    if spfrec.get_redirect_domain() is not None:
        othStr = spfCheck0x00(spfrec)

    if not othStr:
        othStr = spfInclStr0x00(spfrec)

    return othStr


def spfGetall0x00(spfrec):
    spfPolStr = True
    if spfrec.all_string is not None:
        if spfrec.all_string == "~all" or spfrec.all_string == "-all":
            print(GR+" [-] SPF record contains an All item : " + spfrec.all_string)
        else:
            print(G+" [+] SPF record All item is too weak : " + spfrec.all_string)
            spfPolStr = False
    else:
        print(G+" [+] SPF record has no All string...")
        spfPolStr = False

    if not spfPolStr:
        spfPolStr = spfInc0x00(spfrec)

    return spfPolStr


def spfStr0x00(domain):

    print(GR+' [*] Getting SPF records...')
    time.sleep(0.6)
    spfVal = True
    print(C+' [*] Setting parameters...')
    spfrec = spflib.SpfRecord.from_domain(domain)
    if spfrec is not None and spfrec.record is not None:
        print(O+" [!] Found SPF record : " + str(spfrec.record))

        spfStro = spfGetall0x00(spfrec)
        if spfStro is False:

            redirStren = spfRedir0x00(spfrec)
            incStren = spfInclude0x00(spfrec)

            spfVal = False

            if redirStren is True:
                spfVal = True

            if incStren is True:
                spfVal = True
    else:
        print(G+' [+] ' + domain + " has no SPF record!")
        spfVal = False

    return spfVal


def dmGet0x00(domain):
    print(C+' [*] Setting request parameters...')
    dmarc = dmarclib.DmarcRecord.from_domain(domain)
    print(GR+' [*] Analysing responses...')
    if dmarc is not None and dmarc.record is not None:
        print(O+" [!] Found DMARC record : " + str(dmarc.record))

    return dmarc

def dmGetOrg0x00(record):
    orgRec = record.get_org_record()
    print(C+' [*] Analysing responses...')
    if orgRec is not None:
        print(O+" [!] Found DMARC Organizational record : " + str(orgRec.record))

    return orgRec

def dmExtras0x00(dmrecord):
    if dmrecord.pct is not None and dmrecord.pct != str(100):
        print(GR+" [-] DMARC pct is set to " + dmrecord.pct + "% - might be possible")

    if dmrecord.rua is not None:
        print(GR+" [-] Aggregate reports will be sent : " + dmrecord.rua)

    if dmrecord.ruf is not None:
        print(O+" [-] Forensics reports will be sent : " + dmrecord.ruf)


def dmCheckPol0x00(dmrecord):
    polstr = False
    if dmrecord.policy is not None:
        if dmrecord.policy == "reject" or dmrecord.policy == "quarantine":
            polstr = True
            print(R+" [-] DMARC policy set to : " + dmrecord.policy)
        else:
            print(G+" [+] DMARC policy set to : " + dmrecord.policy)
    else:
        print(G+" [+] DMARC record has no Policy...")

    return polstr


def dmPolicy0x00(record):
    policystr = False

    try:
        orgRec = record.get_org_record()
        if orgRec is not None and orgRec.record is not None:
            print(O+" [!] Found organizational DMARC record : " + str(orgRec.record))

            if orgRec.subdomain_policy is not None:

                if orgRec.subdomain_policy == "none":
                    print(G+" [+] Organizational subdomain policy set to %(sp)s" % {"sp": orgRec.subdomain_policy})

                elif orgRec.subdomain_policy == "quarantine" or orgRec.subdomain_policy == "reject":
                    print(R+" [-] Organizational subdomain policy explicitly set to %(sp)s" % {"sp": orgRec.subdomain_policy})
                    policystr = True

            else:
                print(O+" [!] No explicit organizational subdomain policy...")
                print(GR+" [*] Defaulting to organizational policy...")
                policystr = dmCheckPol0x00(orgRec)

        else:
            print(G+" [+] No organizational DMARC record...")

    except dmarclib.OrgDomainException:
        print(G+" [+] No organizational DMARC record...")

    except Exception as e:
        print(R+' [-] Exception encountered : ' +str(e))

    return policystr


def dmCheck0x00(domain):
    dmVal = False

    dmarc = dmGet0x00(domain)

    if dmarc is not None and dmarc.record is not None:
        dmVal = dmCheckPol0x00(dmarc)
        dmExtras0x00(dmarc)

    elif dmarc.get_org_domain() is not None:
        print(O+" [!] No DMARC record found...")
        time.sleep(0.5)
        print(GR+" [*] Looking for organizational record...")
        time.sleep(0.6)
        dmVal = dmPolicy0x00(dmarc)

    else:
        print(G+' [+] ' +O+domain +G+ " has no DMARC record!")

    return dmVal

def mailspoof(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = inspect.stack()[0][3]
    global module
    module = "VulnAnalysis"
    global lvl1
    lvl1 = "Basic Bugs & Misconfigurations"
    global lvl3
    lvl3 = ""
    time.sleep(0.5)
    #print(R+'\n     =========================')
    #print(R+'\n      M A I L   S P O O F E R ')
    #print(R+'     ---<>----<>----<>----<>--\n')
    from core.methods.print import pvln
    pvln("mail spoofer")            
    spoofable = False
    try:
        domain = web
        print(O+' [!] Getting txt records...')
        spfstr = spfStr0x00(domain)
        dmValStr = dmCheck0x00(domain)

        if dmValStr is False:
            spoofable = True
        else:
            spoofable = False

        if spoofable == True:
            print(G+" [+] Spoofing possible for " +O+ domain + "!")
            save_data(database, module, lvl1, lvl2, lvl3, name, "Spoofing possible for " + domain)
        else:
            print(R+" [-] Spoofing not possible for " +O+ domain+'...')
            save_data(database, module, lvl1, lvl2, lvl3, name, "Spoofing not possible for " + domain)

    except Exception as e:
        print(R+" [-] Undefault KeyError encountered!")
        print(R+' [-] Exception : ' +str(e))

def attack(web):
    web = web.fullurl
    mailspoof(web)
