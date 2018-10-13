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

from pyexiv2.metadata import ImageMetadata

import unittest
import testutils
import os
import tempfile
from testutils import EMPTY_JPG_DATA


class TestUserCommentReadWrite(unittest.TestCase):

    checksums = {
        'usercomment-ascii.jpg': 'ad29ac65fb6f63c8361aaed6cb02f8c7',
        'usercomment-unicode-ii.jpg': '13b7cc09129a8677f2cf18634f5abd3c',
        'usercomment-unicode-mm.jpg': '7addfed7823c556ba489cd4ab2037200',
        }

    def _read_image(self, filename):
        filepath = testutils.get_absolute_file_path(os.path.join('data', filename))
        self.assert_(testutils.CheckFileSum(filepath, self.checksums[filename]))
        m = ImageMetadata(filepath)
        m.read()
        return m

    def _expected_raw_value(self, endianness, value):
        from pyexiv2 import __exiv2_version__
        if __exiv2_version__ >= '0.20':
            return value
        else:
            encodings = {'ii': 'utf-16le', 'mm': 'utf-16be'}
            return value.decode('utf-8').encode(encodings[endianness])

    def test_read_ascii(self):
        m = self._read_image('usercomment-ascii.jpg')
        tag = m['Exif.Photo.UserComment']
        self.assertEqual(tag.type, 'Comment')
        self.assertEqual(tag.raw_value, 'charset="Ascii" deja vu')
        self.assertEqual(tag.value, u'deja vu')

    def test_read_unicode_little_endian(self):
        m = self._read_image('usercomment-unicode-ii.jpg')
        tag = m['Exif.Photo.UserComment']
        self.assertEqual(tag.type, 'Comment')
        self.assertEqual(tag.raw_value, 'charset="Unicode" %s' % self._expected_raw_value('ii', 'déjà vu'))
        self.assertEqual(tag.value, u'déjà vu')

    def test_read_unicode_big_endian(self):
        m = self._read_image('usercomment-unicode-mm.jpg')
        tag = m['Exif.Photo.UserComment']
        self.assertEqual(tag.type, 'Comment')
        self.assertEqual(tag.raw_value, 'charset="Unicode" %s' % self._expected_raw_value('mm', 'déjà vu'))
        self.assertEqual(tag.value, u'déjà vu')

    def test_write_ascii(self):
        m = self._read_image('usercomment-ascii.jpg')
        tag = m['Exif.Photo.UserComment']
        self.assertEqual(tag.type, 'Comment')
        tag.value = 'foo bar'
        self.assertEqual(tag.raw_value, 'charset="Ascii" foo bar')
        self.assertEqual(tag.value, u'foo bar')

    def test_write_unicode_over_ascii(self):
        m = self._read_image('usercomment-ascii.jpg')
        tag = m['Exif.Photo.UserComment']
        self.assertEqual(tag.type, 'Comment')
        tag.value = u'déjà vu'
        self.assertEqual(tag.raw_value, 'déjà vu')
        self.assertEqual(tag.value, u'déjà vu')

    def test_write_unicode_little_endian(self):
        m = self._read_image('usercomment-unicode-ii.jpg')
        tag = m['Exif.Photo.UserComment']
        self.assertEqual(tag.type, 'Comment')
        tag.value = u'DÉJÀ VU'
        self.assertEqual(tag.raw_value, 'charset="Unicode" %s' % self._expected_raw_value('ii', 'DÉJÀ VU'))
        self.assertEqual(tag.value, u'DÉJÀ VU')

    def test_write_unicode_big_endian(self):
        m = self._read_image('usercomment-unicode-mm.jpg')
        tag = m['Exif.Photo.UserComment']
        self.assertEqual(tag.type, 'Comment')
        tag.value = u'DÉJÀ VU'
        self.assertEqual(tag.raw_value, 'charset="Unicode" %s' % self._expected_raw_value('mm', 'DÉJÀ VU'))
        self.assertEqual(tag.value, u'DÉJÀ VU')


class TestUserCommentAdd(unittest.TestCase):

    def setUp(self):
        # Create an empty image file
        fd, self.pathname = tempfile.mkstemp(suffix='.jpg')
        os.write(fd, EMPTY_JPG_DATA)
        os.close(fd)

    def tearDown(self):
        os.remove(self.pathname)

    def _test_add_comment(self, value):
        metadata = ImageMetadata(self.pathname)
        metadata.read()
        key = 'Exif.Photo.UserComment'
        metadata[key] = value
        metadata.write()

        metadata = ImageMetadata(self.pathname)
        metadata.read()
        self.assert_(key in metadata.exif_keys)
        tag = metadata[key]
        self.assertEqual(tag.type, 'Comment')
        self.assertEqual(tag.value, value)

    def test_add_comment_ascii(self):
        self._test_add_comment('deja vu')

    def test_add_comment_unicode(self):
        self._test_add_comment(u'déjà vu')

