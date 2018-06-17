#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

from colors import *
from cgi import escape
from time import sleep
import StringIO
import gzip

def url0x00(url):
    dat = {   " ": "%20", "!": "%21", "#": "%23", "$": "%24", "%": "%25", "&": "%26", "'": "%27", "(": "%28",
              ")": "%29", "*": "%30", "+": "%2B", ",": "%2C",
              "-": "%2D", ".": "%2E", "/": "%2F", "0": "%30", "1": "%31", "2": "%32", "3": "%33", "4": "%34",
              "5": "%35", "6": "%36", "7": "%37", "8": "%38",
              "9": "%39", ":": "%3A", ";": "%3B", "<": "%3C", "=": "%3D", ">": "%3E", "?": "%3F", "@": "%40",
              "A": "%41", "B": "%42", "C": "%43", "D": "%44",
              "E": "%45", "F": "%46", "G": "%47", "H": "%48", "I": "%49", "J": "%4A", "K": "%4B", "L": "%4C",
              "M": "%4D", "N": "%4E", "O": "%4F", "P": "%50",
              "Q": "%51", "R": "%52", "S": "%53", "T": "%54", "U": "%55", "V": "%56", "W": "%57", "X": "%58",
              "Y": "%59", "Z": "%5A", "[": "%5B", "]": "%5D",
              "^": "%5E", "_": "%5F", "`": "%60", "a": "%61", "b": "%62", "c": "%63", "d": "%64", "e": "%65",
              "f": "%66", "g": "%67", "h": "%68", "i": "%69",
              "j": "%6A", "k": "%6B", "l": "%6C", "m": "%6D", "n": "%6E", "o": "%6F", "p": "%70", "q": "%71",
              "r": "%72", "s": "%73", "t": "%74", "u": "%75",
              "v": "%76", "w": "%77", "y": "%78", "z": "%7A", "{": "%7B", "|": "%7C", "}": "%7D", "~": "%7E"}
    encodeURL = ""
    for i in url:
        encodeURL += dat[i]
    print G+" [+] Encoded string : "+O+'',encodeURL

def html0x00(st):

	for i in st:
		encoded += escape(i)
	print G+' [+] Encoded String : '+O+'',encoded

def base640x00(st):
	
	m = st.encode('base64', 'strict')
	print G+' [+] Encoded String : '+O+m

def ascii0x00(st):

	m = st.decode('unicode_escape')
	print G+' [+] Encoded String : '+O+m

def hex0x00(st):

	m = st.encode('hex', 'strict')
	print G+' [+] Encoded String : '+O+m

def octal0x00(st):

	m = int(st, 8)
	print G+' [+] Encoded String : '+O+m

def binary0x00(st):

	m = ''.join(format(ord(x),'b') for x in st)
	print G+' [+] Encoded String : '+O+m

def gzip0x00(st):

	m = st.encode('zlib','strict')
	print G+' [+] Encoded String : '+O+m
	

def encodeall():

	print R+'\n    ============================='
	print R+'     S T R I N G   E N C O D E R'
	print R+'    =============================\n'
	st = raw_input(O+' [-] Enter a string to be encoded :> ')
	def encode0x00(st):
	    while True:
		print O+'\n  Choose from the options to encode to:\n'
		print B+'    [1]'+C+' URL Encode'
		print B+'    [2]'+C+' HTML Encode'
		print B+'    [3]'+C+' Base64 Encode'
		print B+'    [4]'+C+' Plain ASCII Encode'
		print B+'    [5]'+C+' Hex Encode'
		print B+'    [6]'+C+' Octal Encode'
		print B+'    [7]'+C+' Binary Encode'
		print B+'    [8]'+C+' GZip Encode\n'
		r = input(O+' [#] Enter your option...')
		print GR+' [*] Encoding string...'
		sleep(0.5)
		if r == '1':
			url0x00(st)
			time.sleep(2)
			encode0x00(st)
		elif r == '2':
			html0x00(st)
			time.sleep(2)
			encode0x00(st)
		elif r == '3':
			base640x00(st)
			time.sleep(2)
			encode0x00(st)
		elif r == '4':
			ascii0x00(st)
			time.sleep(2)
			encode0x00(st)
		elif r == '5':
			hex0x00(st)
			time.sleep(2)
			encode0x00(st)
		elif r == '6':
			octal0x00(st)
			time.sleep(2)
			encode0x00(st)
		elif r == '7':
			binary0x00(st)
			time.sleep(2)
			encode0x00(st)
		elif r == '8':
			gzip0x00(st)
			time.sleep(2)
			encode0x00(st)

