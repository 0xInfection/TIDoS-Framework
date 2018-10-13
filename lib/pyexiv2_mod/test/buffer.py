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

import unittest
import os.path
import hashlib
from datetime import datetime

from pyexiv2.metadata import ImageMetadata

import testutils


class TestBuffer(unittest.TestCase):

    def setUp(self):
        filename = os.path.join('data', 'smiley1.jpg')
        self.filepath = testutils.get_absolute_file_path(filename)
        self.md5sum = 'c066958457c685853293058f9bf129c1'
        self.assert_(testutils.CheckFileSum(self.filepath, self.md5sum))

    def _metadata_from_buffer(self):
        fd = open(self.filepath, 'rb')
        data = fd.read()
        fd.close()
        return ImageMetadata.from_buffer(data)

    def test_from_file_and_from_buffer(self):
        # from file
        m1 = ImageMetadata(self.filepath)
        m1.read()
        self.assertEqual(hashlib.md5(m1.buffer).hexdigest(), self.md5sum)

        # from buffer
        m2 = self._metadata_from_buffer()
        self.assertEqual(hashlib.md5(m2.buffer).hexdigest(), self.md5sum)

    def test_buffer_not_updated_until_write_called(self):
        m = self._metadata_from_buffer()
        m.read()
        self.assertEqual(hashlib.md5(m.buffer).hexdigest(), self.md5sum)

        # Modify the value of an EXIF tag
        m['Exif.Image.DateTime'].value = datetime.today()
        # Check that the buffer is unchanged until write() is called
        self.assertEqual(hashlib.md5(m.buffer).hexdigest(), self.md5sum)
        # Write back the changes
        m.write()
        # Check that the buffer has changed
        self.failIfEqual(hashlib.md5(m.buffer).hexdigest(), self.md5sum)

    def test_from_original_buffer(self):
        m1 = self._metadata_from_buffer()
        m2 = ImageMetadata.from_buffer(m1.buffer)
        self.assertEqual(hashlib.md5(m2.buffer).hexdigest(), self.md5sum)

    def test_from_modified_buffer(self):
        m1 = self._metadata_from_buffer()
        m1.read()
        key = 'Exif.Image.ImageDescription'
        value = 'my kingdom for a semiquaver'
        m1[key] = value
        m1.write()

        m2 = ImageMetadata.from_buffer(m1.buffer)
        m2.read()
        self.assertEqual(m2[key].value, value)

