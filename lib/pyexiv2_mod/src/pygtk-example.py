#!/usr/bin/python
# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2007-2010 Olivier Tilloy <olivier@tilloy.net>
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
import gtk
from pyexiv2 import ImageMetadata


if __name__ == '__main__':
    """
    Example of how to combine pygtk and pyexiv2 to display thumbnail data.

    Minimalistic example of how to load and display with pygtk the thumbnail
    data extracted from an image.
    The path to the image file from which the thumbnail data should be extracted
    should be passed as the only argument of the script.

    It is of course assumed that you have pygtk installed.
    """
    if (len(sys.argv) != 2):
        print 'Usage: ' + sys.argv[0] + ' path/to/picture/file/containing/jpeg/thumbnail'
        sys.exit(1)

    app = gtk.Window(gtk.WINDOW_TOPLEVEL)
    app.connect('destroy', lambda app: gtk.main_quit())

    # Load the image, read the metadata and extract the thumbnail data
    metadata = ImageMetadata(sys.argv[1])
    metadata.read()
    previews = metadata.previews
    if not previews:
        print "This image doesn't contain any thumbnail."
        sys.exit(1)

    # Get the largest preview available
    preview = previews[-1]

    # Create a pixbuf loader to read the thumbnail data
    pbloader = gtk.gdk.PixbufLoader()
    pbloader.write(preview.data)
    # Get the resulting pixbuf and build an image to be displayed
    pixbuf = pbloader.get_pixbuf()
    pbloader.close()
    imgwidget = gtk.Image()
    imgwidget.set_from_pixbuf(pixbuf)

    # Show the application's main window
    app.add(imgwidget)
    imgwidget.show()
    app.show()
    sys.exit(gtk.main())

