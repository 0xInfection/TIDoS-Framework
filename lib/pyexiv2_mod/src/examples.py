#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyexiv2 import ImageMetadata

import sys, os
from datetime import datetime, date


def print_key_value(metadata, key):
    print key, '=', metadata[key]


if __name__ == '__main__':
    # Read an image file's metadata
    image_file = sys.argv[1]
    metadata = ImageMetadata(image_file)
    metadata.read()

    # Print a list of all the keys of the EXIF tags in the image
    print 'EXIF keys:', metadata.exif_keys

    try:
        # Print the value of the Exif.Image.DateTime tag
        key = 'Exif.Image.DateTime'
        print_key_value(metadata, key)

        # Set the value of the Exif.Image.DateTime tag
        metadata[key] = datetime.now()
        print_key_value(metadata, key)
    except KeyError:
        print '[not set]'

    # Add a new tag
    key = 'Exif.Image.Orientation'
    metadata[key] = 1
    print_key_value(metadata, key)

    # Print a list of all the keys of the IPTC tags in the image
    print os.linesep, 'IPTC keys:', metadata.iptc_keys

    try:
        # Print the value of the Iptc.Application2.DateCreated tag
        key = 'Iptc.Application2.DateCreated'
        print_key_value(metadata, key)

        # Set the value of the Iptc.Application2.DateCreated tag
        metadata[key] = [date.today()]
        print_key_value(metadata, key)
    except KeyError:
        print '[not set]'

    # Add a new tag
    key = 'Iptc.Application2.Keywords'
    keywords = ['little', 'big', 'man']
    metadata[key] = keywords
    print_key_value(metadata, key)

    # Print a list of all the keys of the XMP tags in the image
    print os.linesep, 'XMP keys:', metadata.xmp_keys

    try:
        # Print the value of the Xmp.dc.subject tag
        key = 'Xmp.dc.subject'
        print_key_value(metadata, key)

        # Set the value of the Xmp.dc.subject tag
        metadata[key] = keywords
        print_key_value(metadata, key)
    except KeyError:
        print '[not set]'

    # Add a new tag
    key = 'Xmp.dc.title'
    metadata[key] = {'x-default': 'Sunset', 'fr': 'Coucher de soleil'}
    print_key_value(metadata, key)

    # Write back the metadata to the file
    metadata.write()

