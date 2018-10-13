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

from pyexiv2.exif import ExifTag
from pyexiv2.iptc import IptcTag
from pyexiv2.xmp import XmpTag
from pyexiv2.utils import make_fraction, FixedOffset

import unittest
import pickle
import datetime


class TestPicklingTags(unittest.TestCase):

    def test_pickle_exif_tag(self):
        tags = []
        tags.append(ExifTag('Exif.Image.DateTime',
                            datetime.datetime(2010, 12, 22, 19, 21, 0)))
        tags.append(ExifTag('Exif.GPSInfo.GPSDateStamp', datetime.date.today()))
        tags.append(ExifTag('Exif.Image.Copyright', '(C) 2010 Santa Claus'))
        tags.append(ExifTag('Exif.GPSInfo.GPSVersionID', '0'))
        tags.append(ExifTag('Exif.Pentax.Temperature', '14'))
        tags.append(ExifTag('Exif.Photo.UserComment', 'foo bar baz'))
        tags.append(ExifTag('Exif.Image.BitsPerSample', 8))
        tags.append(ExifTag('Exif.Image.TimeZoneOffset', 7))
        tags.append(ExifTag('Exif.Image.ImageWidth', 7492))
        tags.append(ExifTag('Exif.OlympusCs.ManometerReading', 29))
        tags.append(ExifTag('Exif.Image.XResolution', make_fraction(7, 3)))
        tags.append(ExifTag('Exif.Image.BaselineExposure', make_fraction(-7, 3)))
        tags.append(ExifTag('Exif.Photo.ExifVersion', '0100'))
        for tag in tags:
            s = pickle.dumps(tag)
            t = pickle.loads(s)
            self.assert_(isinstance(t, ExifTag))
            self.assertEqual(t.key, tag.key)
            self.assertEqual(t.type, tag.type)
            self.assertEqual(t.name, tag.name)
            self.assertEqual(t.label, tag.label)
            self.assertEqual(t.description, tag.description)
            self.assertEqual(t.section_name, tag.section_name)
            self.assertEqual(t.section_description, tag.section_description)
            self.assertEqual(t.raw_value, tag.raw_value)
            self.assertEqual(t.value, tag.value)
            self.assertEqual(t.human_value, tag.human_value)

    def test_pickle_iptc_tag(self):
        tags = []
        tags.append(IptcTag('Iptc.Envelope.FileFormat', [23]))
        tags.append(IptcTag('Iptc.Application2.Subject', ['foo', 'bar', 'baz']))
        tags.append(IptcTag('Iptc.Envelope.DateSent', [datetime.date.today()]))
        tags.append(IptcTag('Iptc.Envelope.TimeSent',
                            [datetime.time(23, 37, 4, tzinfo=FixedOffset('+', 6, 0))]))
        tags.append(IptcTag('Iptc.Application2.Preview', ['01001101']))
        for tag in tags:
            s = pickle.dumps(tag)
            t = pickle.loads(s)
            self.assert_(isinstance(t, IptcTag))
            self.assertEqual(t.key, tag.key)
            self.assertEqual(t.type, tag.type)
            self.assertEqual(t.name, tag.name)
            self.assertEqual(t.title, tag.title)
            self.assertEqual(t.description, tag.description)
            self.assertEqual(t.photoshop_name, tag.photoshop_name)
            self.assertEqual(t.repeatable, tag.repeatable)
            self.assertEqual(t.record_name, tag.record_name)
            self.assertEqual(t.record_description, tag.record_description)
            self.assertEqual(t.raw_value, tag.raw_value)
            self.assertEqual(t.value, tag.value)

    def test_pickle_xmp_tag(self):
        tags = []
        tags.append(XmpTag('Xmp.dc.subject', ['foo', 'bar', 'baz']))
        tags.append(XmpTag('Xmp.xmpRights.Marked', True))
        tags.append(XmpTag('Xmp.xmp.CreateDate', datetime.date.today()))
        tags.append(XmpTag('Xmp.xmpMM.SaveID', 34))
        tags.append(XmpTag('Xmp.dc.format', ('image', 'jpeg')))
        tags.append(XmpTag('Xmp.photoshop.CaptionWriter', 'John Doe'))
        tags.append(XmpTag('Xmp.dc.source', 'bleh'))
        tags.append(XmpTag('Xmp.xmpMM.DocumentID', 'http://example.com'))
        tags.append(XmpTag('Xmp.xmp.BaseURL', 'http://example.com'))
        tags.append(XmpTag('Xmp.xmpDM.videoPixelAspectRatio', make_fraction(5, 3)))
        for tag in tags:
            s = pickle.dumps(tag)
            t = pickle.loads(s)
            self.assert_(isinstance(t, XmpTag))
            self.assertEqual(t.key, tag.key)
            self.assertEqual(t.type, tag.type)
            self.assertEqual(t.name, tag.name)
            self.assertEqual(t.title, tag.title)
            self.assertEqual(t.description, tag.description)
            self.assertEqual(t.raw_value, tag.raw_value)
            self.assertEqual(t.value, tag.value)

