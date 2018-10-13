#!/usr/bin/python
# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2006-2010 Olivier Tilloy <olivier@tilloy.net>
#
# This file is part of the pyexiv2 distribution.
#
# pyexiv2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# pyexiv2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyexiv2; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, 5th Floor, Boston, MA 02110-1301 USA.
#
# Author: Olivier Tilloy <olivier@tilloy.net>
#
# ******************************************************************************

import sys

from pyexiv2.metadata import ImageMetadata


if __name__ == '__main__':
    args = sys.argv

    if len(args) != 2:
        print 'Usage: %s image_file' % args[0]
        sys.exit(-1)

    metadata = ImageMetadata(args[1])
    metadata.read()

    for key in metadata.exif_keys:
        tag = metadata[key]
        print '%-45s%-11s%s' % (key, tag.type, str(tag))

    for key in metadata.iptc_keys:
        tag = metadata[key]
        print '%-45s%-11s%s' % (key, tag.type, str(tag))

    # TODO: print XMP tags.

