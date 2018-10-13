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
from PyQt4 import QtGui
from pyexiv2 import ImageMetadata


if __name__ == '__main__':
    """
    Example of how to combine PyQt4 and pyexiv2 to display thumbnail data.

    Minimalistic example of how to load and display with PyQt the thumbnail data
    extracted from an image.
    The path to the image file from which the thumbnail data should be extracted
    should be passed as the only argument of the script.

    It is of course assumed that you have PyQt4 installed.
    """
    if (len(sys.argv) != 2):
        print 'Usage: ' + sys.argv[0] + ' path/to/picture/file/containing/jpeg/thumbnail'
        sys.exit(1)

    app = QtGui.QApplication([])

    # Load the image, read the metadata and extract the thumbnail data
    metadata = ImageMetadata(sys.argv[1])
    metadata.read()
    previews = metadata.previews
    if not previews:
        print "This image doesn't contain any thumbnail."
        sys.exit(1)

    # Get the largest preview available
    preview = previews[-1]

    # Create a pixmap from the thumbnail data
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(preview.data, 'JPEG')

    # Create a QT label to display the pixmap
    label = QtGui.QLabel(None)
    label.setPixmap(pixmap)

    # Show the application's main window
    label.show()
    sys.exit(app.exec_())

