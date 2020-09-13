#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: 0xInfection (@_tID)
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import urllib.request
from bs4 import BeautifulSoup
import modules.VlnAnalysis.Severe.uri as uri
import re
from core.Core.colors import *

info = ""
searchinfo = ""
properties = {}

def removeIDs(uri):

    p = re.compile('=[0-9]+')
    uri = p.sub('=',uri)
    p = re.compile('(title=)[^&]*')
    uri = p.sub('\\1',uri)
    return uri

class Crawler():

    def __init__(self, start,opener):

        self.visited = []
        self.toVisit = []
        self.uriPatterns = []
        self.currentURI = '';
        self.opener = opener;
        self.toVisit.append(start)

    def getVisited(self):
        return self.visited

    def addVisited(self,uri):
        self.visited.append(uri)

    def getToVisit(self):
        return self.toVisit

    def addToVisit(self,uri):
        self.toVisit.append(uri)

    def getUriPatterns(self):
        return self.uriPatterns

    def addUriPatterns(self,uri):
        self.uriPatterns.append(uri)

    def process(self, root):
        url = self.currentURI

        try:
            query = self.opener.open(url)

        except urllib.error.HTTPError as msg: #couldn't perform the query
            print(R+' [-] Request Error: '+msg.__str__())
            if url in self.toVisit:
                self.toVisit.remove(url)
            return

        #if content is not html
        if not re.search('html',query.info()['Content-Type']):
            return

        print(GR+' [*] Making request to new location...')
        if hasattr(query.info(),'Location'):
            url=query.info()['Location']
        print(C+' [*] Reading response...')
        response = query.read()

        try:
            print(O+' [*] Trying to parse response...')
            soup = BeautifulSoup(response)

        except HTMLParser.HTMLParseError:
            print(R+' [-] BeautifulSoup Error: '+url)
            self.visited.append(url)

            if url in self.toVisit:
                self.toVisit.remove(url)
            return

        #retrieve all links (<a href="...")
        for m in soup.findAll('a',href=True):
            app=''
            #if href is not a function or begins with http://
            if not re.match(r'javascript:',m['href']) or re.match('http://',m['href']):
                app = uri.buildUrl(url,m['href'])
            #if we get a valid link
            if app!='' and re.search(root, app):
                #get rid of ../
                while re.search(r'/\.\./',app):
                    p = re.compile('/[^/]*/../')
                    app = p.sub('/',app)
                #get rid of ./
                p = re.compile('\./')
                app = p.sub('',app)

                #add new link to the queue only if its pattern has not been added yet
                uriPattern=removeIDs(app)
                if self.notExist(uriPattern) and app!=url:
                    print(G+' [+] Added :> ' +O+ app)
                    self.toVisit.append(app)
                    self.uriPatterns.append(uriPattern)
        #current url has been processed
        self.visited.append(url)
        return soup

    def noinit(self):
        if len(self.toVisit)>0:
            return True
        else:
            return False

    def next(self):
        self.currentURI = self.toVisit[0]
        self.toVisit.remove(self.currentURI)
        return self.currentURI

    def notExist(self, test):

        if (test not in self.uriPatterns):
            return 1
        return 0
