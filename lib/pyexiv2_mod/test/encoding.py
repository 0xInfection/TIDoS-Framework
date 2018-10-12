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
import os
import sys
import binascii
import locale
from tempfile import gettempdir

from pyexiv2.metadata import ImageMetadata


_HEXDATA = """
ff d8 ff e0 00 10 4a 46  49 46 00 01 01 01 00 48
00 48 00 00 ff e1 00 36  45 78 69 66 00 00 49 49
2a 00 08 00 00 00 01 00  32 01 02 00 14 00 00 00
1a 00 00 00 00 00 00 00  32 30 31 30 3a 30 33 3a
31 38 20 31 33 3a 33 39  3a 35 38 00 ff db 00 43
00 05 03 04 04 04 03 05  04 04 04 05 05 05 06 07
0c 08 07 07 07 07 0f 0b  0b 09 0c 11 0f 12 12 11
0f 11 11 13 16 1c 17 13  14 1a 15 11 11 18 21 18
1a 1d 1d 1f 1f 1f 13 17  22 24 22 1e 24 1c 1e 1f
1e ff db 00 43 01 05 05  05 07 06 07 0e 08 08 0e
1e 14 11 14 1e 1e 1e 1e  1e 1e 1e 1e 1e 1e 1e 1e
1e 1e 1e 1e 1e 1e 1e 1e  1e 1e 1e 1e 1e 1e 1e 1e
1e 1e 1e 1e 1e 1e ff c0  00 11 08 00 01 00 01 03
01 22 00 02 11 01 03 11  01 ff c4 00 15 00 01 01
00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 08
ff c4 00 14 10 01 00 00  00 00 00 00 00 00 00 00
00 00 00 00 00 00 ff c4  00 14 01 01 00 00 00 00
00 00 00 00 00 00 00 00  00 00 00 00 ff c4 00 14
11 01 00 00 00 00 00 00  00 00 00 00 00 00 00 00
00 00 ff da 00 0c 03 01  00 02 11 03 11 00 3f 00
b2 c0 07 ff d9
"""

_BINDATA = binascii.unhexlify(''.join(_HEXDATA.split()))


class TestEncodings(unittest.TestCase):

    def setUp(self):
        self._cwd = os.getcwd()
        os.chdir(gettempdir())
        try:
            locale.setlocale(locale.LC_ALL, '')
        except locale.Error:
            self.encoding = None
        else:
            lc, self.encoding = locale.getlocale()

    def tearDown(self):
        os.chdir(self._cwd)

    def _create_file(self, filename):
        try:
            os.remove(filename)
        except OSError:
            pass
        fd = open(filename, 'wb')
        fd.write(_BINDATA)
        fd.close()

    def _test_filename(self, filename):
        self._create_file(filename)
        m = ImageMetadata(filename)
        m.read()
        os.remove(filename)

    def test_ascii(self):
        self._test_filename('test.jpg')

    def test_latin1(self):
        self._test_filename('tést.jpg')

    def test_latin1_escaped(self):
        self._test_filename('t\xc3\xa9st.jpg')

    def test_unicode_ascii(self):
        if self.encoding is not None:
            self._test_filename(u'test.jpg')

    def test_unicode_latin1(self):
        if self.encoding is not None:
            self._test_filename(u'tést.jpg')

    def test_unicode_latin1_escaped(self):
        if self.encoding is not None:
            self._test_filename(u't\xe9st.jpg')

