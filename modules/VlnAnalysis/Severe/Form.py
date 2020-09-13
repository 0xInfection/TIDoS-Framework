
# Just some modified version of CSRFProbe
# https://github.com/0xInfection/CSRFProbe
#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: 0xInfection (@_tID)
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

import modules.VlnAnalysis.Severe.uri
import re
from random import Random
import string
from core.Core.colors import *

info = ""
searchinfo = ""
properties = {}

class Form():

    def prepareFormInputs(self, form):
        print(C+' [*] Crafting inputs as form type...')
        print(GR+' [*] Parsing final inputs...')
        input = {}
        print(B+' [*] Processing '+C+'<input type="test" name="'+B+'...')
        for m in form.findAll('input',{'name' : True,'type' : 'text'}):
            if re.search(' value=',m.__str__()):
                value=m['value'].encode('utf8')
            else:
                value=randString()
            input[m['name']] = value
        print(B+' [*] Processing'+C+' <input type="password" name="...')
        for m in form.findAll('input',{'name' : True,'type' : 'password'}):
            if re.search(' value=',m.__str__()):
                value=m['value'].encode('utf8')
            else:
                value=randString()
            input[m['name']] = value
        print(B+' [*] Processing '+C+'<input type="submit" name="...')
        for m in form.findAll('input',{'name' : True,'type' : 'submit'}):
            if re.search(' value=',m.__str__()):
                value=m['value'].encode('utf8')
            else:
                value=randString()
            input[m['name']] = value
        print(B+' [*] Processing'+C+' <input type="hidden" name="...')
        for m in form.findAll('input',{'name' : True,'type' : 'hidden'}):
            if re.search(' value=',m.__str__()):
                value=m['value'].encode('utf8')
            else:
                value=randString()
            input[m['name']] = value
        print(B+' [*] Processing'+C+' <input type="checkbox" name="...')
        for m in form.findAll('input',{'name' : True,'type' : 'checkbox'}):
            if re.search(' value=',m.__str__()):
                value=m['value'].encode('utf8')
            else:
                value=randString()
            input[m['name']] = value
        print(B+' [*] Processing'+C+' <input type="radio" name="...')
        listRadio = []
        for m in form.findAll('input',{'name' : True,'type' : 'radio'}):
            if (not m['name'] in listRadio) and re.search(' value=',m.__str__()):
                listRadio.append(m['name'])
                input[m['name']] = value.encode('utf8')
        print(B+' [*] Processing'+C+' <textarea name="...')
        for m in form.findAll('textarea',{'name' : True}):
            if len(m.contents)==0:
                m.contents.append(randString())
            input[m['name']] = m.contents[0].encode('utf8')
        print(B+' [*] Processing'+C+' <select name="...')
        for m in form.findAll('select',{'name' : True}):
            if len(m.findAll('option',value=True))>0:
                name = m['name']
                input[name] = m.findAll('option',value=True)[0]['value'].encode('utf8')
        return input

def randString():
    return ''.join( Random().sample(string.ascii_letters, 6))

def getAllForms(soup):
    return soup.findAll('form',action=True,method=re.compile("post", re.IGNORECASE))
