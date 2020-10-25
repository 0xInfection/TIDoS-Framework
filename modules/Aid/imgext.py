#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
import PIL.ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image
from core.Core.colors import *
from collections import namedtuple
import os

Header= namedtuple('Header',
    "profile_size,cmm_type,version,device_class,colour_space,"
    "PCS,date_time,signature,sig_platform,flags,dev_manufacturer,"
    "dev_model,dev_attributes,intent,illuminant,sig_creator,"
    "id"
    )

info = "Image Analysis based on metadata."
searchinfo = "Image Analysis"
properties = {}

def gps(exif):

    gpsinfo = {}
    if 'GPSInfo' in exif:
        Nsec = exif['GPSInfo'][2][2][0] / float(exif['GPSInfo'][2][2][1])
        Nmin = exif['GPSInfo'][2][1][0] / float(exif['GPSInfo'][2][1][1])
        Ndeg = exif['GPSInfo'][2][0][0] / float(exif['GPSInfo'][2][0][1])
        Wsec = exif['GPSInfo'][4][2][0] / float(exif['GPSInfo'][4][2][1])
        Wmin = exif['GPSInfo'][4][1][0] / float(exif['GPSInfo'][4][1][1])
        Wdeg = exif['GPSInfo'][4][0][0] / float(exif['GPSInfo'][4][0][1])
        if exif['GPSInfo'][1] == 'N':
            Nmult = 1
        else:
            Nmult = -1
        if exif['GPSInfo'][1] == 'E':
            Wmult = 1
        else:
            Wmult = -1
        Lat = Nmult * (Ndeg + (Nmin + Nsec/60.0)/60.0)
        Lng = Wmult * (Wdeg + (Wmin + Wsec/60.0)/60.0)
        exif['GPSInfo'] = {"Lat" : Lat, "Lng" : Lng}


def exif1meta(image_path):

    ret = {}
    image = Image.open(image_path)
    if hasattr(image, '_getexif'):
        exifinfo = image._getexif()
        if exifinfo is not None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
    gps(ret)
    return ret

def exif3meta(image_path):

    print(GR+'\n [*] Reading METADATA info...')
    for tag, value in Image.open(image_path)._getexif().iteritems():
        print(O+' [+] '+str(TAGS.get(tag))+' : '+C+str(value))

def imgext():

    #print(R+'\n    =============================')
    print(R+'\n     I M A G E   A N A L Y S I S')
    print(R+'    ---<>----<>----<>----<>----<>\n')
                 
    name = input(O+' [§] Enter path to image file :> ')

    if os.path.exists(name):
        print(GR+" [+] Metadata for file: %s " %(name))
        try:
            print(O+' [!] Extracting METADATA info...\n')
            time.sleep(0.7)
            exifData = {}
            exif = exif1meta(name)
            for metadata in exif:
                print(G+" [+] "+str(metadata)+O+ " - Value :"+C+" %s " %(str(exif[metadata])))
                time.sleep(0.1)
            exif3meta(name)

        except Exception as e:
            print(R+' [-] Caught Exception : '+str(e))
    else:
        print(R+' [-] No such file/directory present...')
    print(G+'\n [+] Forensic Image Analysis Done!\n')

def attack(web):
    imgext()
