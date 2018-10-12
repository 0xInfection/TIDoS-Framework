# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2009-2011 Olivier Tilloy <olivier@tilloy.net>
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

from pyexiv2.exif import ExifTag, ExifValueError
from pyexiv2.metadata import ImageMetadata
from pyexiv2.utils import make_fraction

import testutils

import datetime
import os.path


class TestExifTag(unittest.TestCase):

    def test_convert_to_python_ascii(self):
        # Valid values: datetimes
        tag = ExifTag('Exif.Image.DateTime')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_python('2009-03-01 12:46:51'),
                         datetime.datetime(2009, 03, 01, 12, 46, 51))
        self.assertEqual(tag._convert_to_python('2009:03:01 12:46:51'),
                         datetime.datetime(2009, 03, 01, 12, 46, 51))
        self.assertEqual(tag._convert_to_python('2009-03-01T12:46:51Z'),
                         datetime.datetime(2009, 03, 01, 12, 46, 51))

        # Valid values: dates
        tag = ExifTag('Exif.GPSInfo.GPSDateStamp')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_python('2009:08:04'),
                         datetime.date(2009, 8, 4))

        # Valid values: strings
        tag = ExifTag('Exif.Image.Copyright')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_python('Some text.'), 'Some text.')
        self.assertEqual(tag._convert_to_python(u'Some text with exotic chàräctérʐ.'),
                         u'Some text with exotic chàräctérʐ.')

        # Invalid values: datetimes
        tag = ExifTag('Exif.Image.DateTime')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_python('2009-13-01 12:46:51'),
                         '2009-13-01 12:46:51')
        self.assertEqual(tag._convert_to_python('2009-12-01'), '2009-12-01')

        # Invalid values: dates
        tag = ExifTag('Exif.GPSInfo.GPSDateStamp')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_python('2009:13:01'), '2009:13:01')
        self.assertEqual(tag._convert_to_python('2009-12-01'), '2009-12-01')

    def test_convert_to_string_ascii(self):
        # Valid values: datetimes
        tag = ExifTag('Exif.Image.DateTime')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_string(datetime.datetime(2009, 03, 01, 12, 54, 28)),
                         '2009:03:01 12:54:28')
        self.assertEqual(tag._convert_to_string(datetime.date(2009, 03, 01)),
                         '2009:03:01 00:00:00')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, 59)),
                         '1899:12:31 23:59:59')
        self.assertEqual(tag._convert_to_string(datetime.date(1899, 12, 31)),
                         '1899:12:31 00:00:00')

        # Valid values: dates
        tag = ExifTag('Exif.GPSInfo.GPSDateStamp')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_string(datetime.date(2009, 03, 01)),
                         '2009:03:01')
        self.assertEqual(tag._convert_to_string(datetime.date(1899, 12, 31)),
                         '1899:12:31')

        # Valid values: strings
        tag = ExifTag('Exif.Image.Copyright')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_string(u'Some text'), 'Some text')
        self.assertEqual(tag._convert_to_string(u'Some text with exotic chàräctérʐ.'),
                         'Some text with exotic chàräctérʐ.')
        self.assertEqual(tag._convert_to_string('Some text with exotic chàräctérʐ.'),
                         'Some text with exotic chàräctérʐ.')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, None)

    def test_convert_to_python_byte(self):
        # Valid values
        tag = ExifTag('Exif.GPSInfo.GPSVersionID')
        self.assertEqual(tag.type, 'Byte')
        self.assertEqual(tag._convert_to_python('D'), 'D')

    def test_convert_to_string_byte(self):
        # Valid values
        tag = ExifTag('Exif.GPSInfo.GPSVersionID')
        self.assertEqual(tag.type, 'Byte')
        self.assertEqual(tag._convert_to_string('Some text'), 'Some text')
        self.assertEqual(tag._convert_to_string(u'Some text'), 'Some text')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, None)

    def test_convert_to_python_sbyte(self):
        # Valid values
        tag = ExifTag('Exif.Pentax.Temperature')
        self.assertEqual(tag.type, 'SByte')
        self.assertEqual(tag._convert_to_python('15'), '15')

    def test_convert_to_string_sbyte(self):
        # Valid values
        tag = ExifTag('Exif.Pentax.Temperature')
        self.assertEqual(tag.type, 'SByte')
        self.assertEqual(tag._convert_to_string('13'), '13')
        self.assertEqual(tag._convert_to_string(u'13'), '13')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, None)

    def test_convert_to_python_comment(self):
        # Valid values
        tag = ExifTag('Exif.Photo.UserComment')
        self.assertEqual(tag.type, 'Comment')
        self.assertEqual(tag._convert_to_python('A comment'), 'A comment')
        for charset in ('Ascii', 'Jis', 'Unicode', 'Undefined', 'InvalidCharsetId'):
            self.assertEqual(tag._convert_to_python('charset="%s" A comment' % charset), 'A comment')
        for charset in ('Ascii', 'Jis', 'Undefined', 'InvalidCharsetId'):
            self.failIfEqual(tag._convert_to_python('charset="%s" déjà vu' % charset), u'déjà vu')

    def test_convert_to_string_comment(self):
        # Valid values
        tag = ExifTag('Exif.Photo.UserComment')
        self.assertEqual(tag.type, 'Comment')
        self.assertEqual(tag._convert_to_string('A comment'), 'A comment')
        self.assertEqual(tag._convert_to_string(u'A comment'), 'A comment')
        charsets = ('Ascii', 'Jis', 'Unicode', 'Undefined')
        for charset in charsets:
            tag.raw_value = 'charset="%s" foo' % charset
            self.assertEqual(tag._convert_to_string('A comment'),
                             'charset="%s" A comment' % charset)
            self.assertEqual(tag._convert_to_string('déjà vu'), 'déjà vu')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, None)

    def test_convert_to_python_short(self):
        # Valid values
        tag = ExifTag('Exif.Image.BitsPerSample')
        self.assertEqual(tag.type, 'Short')
        self.assertEqual(tag._convert_to_python('8'), 8)
        self.assertEqual(tag._convert_to_python('+5628'), 5628)

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, 'abc')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5,64')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '47.0001')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '1E3')

    def test_convert_to_string_short(self):
        # Valid values
        tag = ExifTag('Exif.Image.BitsPerSample')
        self.assertEqual(tag.type, 'Short')
        self.assertEqual(tag._convert_to_string(123), '123')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, -57)
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 'invalid')
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 3.14)

    def test_convert_to_python_sshort(self):
        # Valid values
        tag = ExifTag('Exif.Image.TimeZoneOffset')
        self.assertEqual(tag.type, 'SShort')
        self.assertEqual(tag._convert_to_python('8'), 8)
        self.assertEqual(tag._convert_to_python('+5'), 5)
        self.assertEqual(tag._convert_to_python('-6'), -6)

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, 'abc')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5,64')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '47.0001')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '1E3')

    def test_convert_to_string_sshort(self):
        # Valid values
        tag = ExifTag('Exif.Image.TimeZoneOffset')
        self.assertEqual(tag.type, 'SShort')
        self.assertEqual(tag._convert_to_string(12), '12')
        self.assertEqual(tag._convert_to_string(-3), '-3')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 'invalid')
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 3.14)

    def test_convert_to_python_long(self):
        # Valid values
        tag = ExifTag('Exif.Image.ImageWidth')
        self.assertEqual(tag.type, 'Long')
        self.assertEqual(tag._convert_to_python('8'), 8)
        self.assertEqual(tag._convert_to_python('+5628'), 5628)

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, 'abc')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5,64')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '47.0001')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '1E3')

    def test_convert_to_string_long(self):
        # Valid values
        tag = ExifTag('Exif.Image.ImageWidth')
        self.assertEqual(tag.type, 'Long')
        self.assertEqual(tag._convert_to_string(123), '123')
        self.assertEqual(tag._convert_to_string(678024), '678024')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, -57)
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 'invalid')
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 3.14)

    def test_convert_to_python_slong(self):
        # Valid values
        tag = ExifTag('Exif.OlympusCs.ManometerReading')
        self.assertEqual(tag.type, 'SLong')
        self.assertEqual(tag._convert_to_python('23'), 23)
        self.assertEqual(tag._convert_to_python('+5628'), 5628)
        self.assertEqual(tag._convert_to_python('-437'), -437)

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, 'abc')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5,64')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '47.0001')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '1E3')

    def test_convert_to_string_slong(self):
        # Valid values
        tag = ExifTag('Exif.OlympusCs.ManometerReading')
        self.assertEqual(tag.type, 'SLong')
        self.assertEqual(tag._convert_to_string(123), '123')
        self.assertEqual(tag._convert_to_string(678024), '678024')
        self.assertEqual(tag._convert_to_string(-437), '-437')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 'invalid')
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 3.14)

    def test_convert_to_python_rational(self):
        # Valid values
        tag = ExifTag('Exif.Image.XResolution')
        self.assertEqual(tag.type, 'Rational')
        self.assertEqual(tag._convert_to_python('5/3'), make_fraction(5, 3))

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, 'invalid')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '-5/3')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5 / 3')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5/-3')

    def test_convert_to_string_rational(self):
        # Valid values
        tag = ExifTag('Exif.Image.XResolution')
        self.assertEqual(tag.type, 'Rational')
        self.assertEqual(tag._convert_to_string(make_fraction(5, 3)), '5/3')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 'invalid')
        self.failUnlessRaises(ExifValueError,
                              tag._convert_to_string, make_fraction(-5, 3))

    def test_convert_to_python_srational(self):
        # Valid values
        tag = ExifTag('Exif.Image.BaselineExposure')
        self.assertEqual(tag.type, 'SRational')
        self.assertEqual(tag._convert_to_python('5/3'), make_fraction(5, 3))
        self.assertEqual(tag._convert_to_python('-5/3'), make_fraction(-5, 3))

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, 'invalid')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5 / 3')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5/-3')

    def test_convert_to_string_srational(self):
        # Valid values
        tag = ExifTag('Exif.Image.BaselineExposure')
        self.assertEqual(tag.type, 'SRational')
        self.assertEqual(tag._convert_to_string(make_fraction(5, 3)), '5/3')
        self.assertEqual(tag._convert_to_string(make_fraction(-5, 3)), '-5/3')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 'invalid')

    def test_convert_to_python_undefined(self):
        # Valid values
        tag = ExifTag('Exif.Photo.ExifVersion')
        self.assertEqual(tag.type, 'Undefined')
        self.assertEqual(tag._convert_to_python('48 49 48 48'), '0100')

    def test_convert_to_string_undefined(self):
        # Valid values
        tag = ExifTag('Exif.Photo.ExifVersion')
        self.assertEqual(tag.type, 'Undefined')
        self.assertEqual(tag._convert_to_string('0100'), '48 49 48 48')
        self.assertEqual(tag._convert_to_string(u'0100'), '48 49 48 48')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 3)

    def test_set_value(self):
        tag = ExifTag('Exif.Thumbnail.Orientation', 1) # top, left
        old_value = tag.value
        tag.value = 2
        self.failIfEqual(tag.value, old_value)

    def test_set_raw_value_invalid(self):
        tag = ExifTag('Exif.GPSInfo.GPSVersionID')
        value = '2 0 0 foo'
        self.failUnlessRaises(ValueError, setattr, tag, 'raw_value', value)

    def test_makernote_types(self):
        # Makernote tags not attached to an image have an Undefined type by
        # default. When read from an existing image though, their type should be
        # correctly set (see https://bugs.launchpad.net/pyexiv2/+bug/781464).
        tag1 = ExifTag('Exif.Pentax.PreviewResolution')
        tag1.raw_value = '640 480'
        self.assertEqual(tag1.type, 'Undefined')
        self.failUnlessRaises(ValueError, getattr, tag1, 'value')
        tag2 = ExifTag('Exif.Pentax.CameraInfo')
        tag2.raw_value = '76830 20070527 2 1 4228109'
        self.assertEqual(tag2.type, 'Undefined')
        self.failUnlessRaises(ValueError, getattr, tag2, 'value')

        filepath = testutils.get_absolute_file_path(os.path.join('data', 'pentax-makernote.jpg'))
        checksum = '646804b309a4a2d31feafe9bffc5d7f0'
        self.assert_(testutils.CheckFileSum(filepath, checksum))
        metadata = ImageMetadata(filepath)
        metadata.read()
        tag1 = metadata[tag1.key]
        self.assertEqual(tag1.type, 'Short')
        self.assertEqual(tag1.value, [640, 480])
        tag2 = metadata[tag2.key]
        self.assertEqual(tag2.type, 'Long')
        self.assertEqual(tag2.value, [76830L, 20070527L, 2L, 1L, 4228109L])

