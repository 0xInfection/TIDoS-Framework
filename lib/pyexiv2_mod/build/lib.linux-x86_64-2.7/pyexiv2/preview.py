# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2010 Olivier Tilloy <olivier@tilloy.net>
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

"""
Provide the Preview class.
"""

class Preview(object):

    """
    A preview image (properties and data buffer) embedded in image metadata.
    """

    def __init__(self, preview):
        self.__preview = preview

    @property
    def mime_type(self):
        """The mime type of the preview image (e.g. ``image/jpeg``)."""
        return self.__preview.mime_type

    @property
    def extension(self):
        """The file extension of the preview image with a leading dot
        (e.g. ``.jpg``)."""
        return self.__preview.extension

    @property
    def size(self):
        """The size of the preview image in bytes."""
        return self.__preview.size

    @property
    def dimensions(self):
        """A tuple containing the width and height of the preview image
        in pixels."""
        return self.__preview.dimensions

    @property
    def data(self):
        """The preview image data buffer."""
        return self.__preview.data

    def write_to_file(self, path):
        """
        Write the preview image to a file on disk.
        The file extension will be automatically appended to the path.

        :param path: path to write the preview to (without an extension)
        :type path: string
        """
        return self.__preview.write_to_file(path)

