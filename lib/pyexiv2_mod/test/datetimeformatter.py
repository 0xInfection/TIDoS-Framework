# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2011 Olivier Tilloy <olivier@tilloy.net>
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

from pyexiv2.utils import DateTimeFormatter, FixedOffset

import datetime


class TestDateTimeFormatter(unittest.TestCase):

    def test_timedelta_to_offset(self):
        # positive deltas
        t = datetime.timedelta(hours=5)
        self.assertEqual(DateTimeFormatter.timedelta_to_offset(t), '+05:00')
        t = datetime.timedelta(minutes=300)
        self.assertEqual(DateTimeFormatter.timedelta_to_offset(t), '+05:00')
        t = datetime.timedelta(hours=5, minutes=12)
        self.assertEqual(DateTimeFormatter.timedelta_to_offset(t), '+05:12')
        t = datetime.timedelta(seconds=10800)
        self.assertEqual(DateTimeFormatter.timedelta_to_offset(t), '+03:00')

        # negative deltas
        t = datetime.timedelta(hours=-4)
        self.assertEqual(DateTimeFormatter.timedelta_to_offset(t), '-04:00')
        t = datetime.timedelta(minutes=-258)
        self.assertEqual(DateTimeFormatter.timedelta_to_offset(t), '-04:18')
        t = datetime.timedelta(hours=-2, minutes=-12)
        self.assertEqual(DateTimeFormatter.timedelta_to_offset(t), '-02:12')
        t = datetime.timedelta(seconds=-10000)
        self.assertEqual(DateTimeFormatter.timedelta_to_offset(t), '-02:46')

    def test_exif(self):
        # datetime
        d = datetime.datetime(1899, 12, 31)
        self.assertEqual(DateTimeFormatter.exif(d), '1899:12:31 00:00:00')
        d = datetime.datetime(1899, 12, 31, 23)
        self.assertEqual(DateTimeFormatter.exif(d), '1899:12:31 23:00:00')
        d = datetime.datetime(1899, 12, 31, 23, 59)
        self.assertEqual(DateTimeFormatter.exif(d), '1899:12:31 23:59:00')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59)
        self.assertEqual(DateTimeFormatter.exif(d), '1899:12:31 23:59:59')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, 999999)
        self.assertEqual(DateTimeFormatter.exif(d), '1899:12:31 23:59:59')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, tzinfo=FixedOffset())
        self.assertEqual(DateTimeFormatter.exif(d), '1899:12:31 23:59:59')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, tzinfo=FixedOffset(hours=5))
        self.assertEqual(DateTimeFormatter.exif(d), '1899:12:31 23:59:59')
        d = datetime.datetime(2011, 8, 8, 19, 3, 37)
        self.assertEqual(DateTimeFormatter.exif(d), '2011:08:08 19:03:37')

        # date
        d = datetime.date(1899, 12, 31)
        self.assertEqual(DateTimeFormatter.exif(d), '1899:12:31')
        d = datetime.date(2011, 8, 8)
        self.assertEqual(DateTimeFormatter.exif(d), '2011:08:08')

        # invalid type
        self.assertRaises(TypeError, DateTimeFormatter.exif, None)
        self.assertRaises(TypeError, DateTimeFormatter.exif, 3.14)

    def test_iptc_date(self):
        # datetime
        d = datetime.datetime(1899, 12, 31)
        self.assertEqual(DateTimeFormatter.iptc_date(d), '1899-12-31')
        d = datetime.datetime(1899, 12, 31, 23)
        self.assertEqual(DateTimeFormatter.iptc_date(d), '1899-12-31')
        d = datetime.datetime(1899, 12, 31, 23, 59)
        self.assertEqual(DateTimeFormatter.iptc_date(d), '1899-12-31')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59)
        self.assertEqual(DateTimeFormatter.iptc_date(d), '1899-12-31')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, 999999)
        self.assertEqual(DateTimeFormatter.iptc_date(d), '1899-12-31')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, tzinfo=FixedOffset())
        self.assertEqual(DateTimeFormatter.iptc_date(d), '1899-12-31')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, tzinfo=FixedOffset(hours=5))
        self.assertEqual(DateTimeFormatter.iptc_date(d), '1899-12-31')
        d = datetime.datetime(2011, 8, 8, 19, 3, 37)
        self.assertEqual(DateTimeFormatter.iptc_date(d), '2011-08-08')

        # date
        d = datetime.date(1899, 12, 31)
        self.assertEqual(DateTimeFormatter.iptc_date(d), '1899-12-31')
        d = datetime.date(2011, 8, 8)
        self.assertEqual(DateTimeFormatter.iptc_date(d), '2011-08-08')

        # invalid type
        self.assertRaises(TypeError, DateTimeFormatter.iptc_date, None)
        self.assertRaises(TypeError, DateTimeFormatter.iptc_date, 3.14)

    def test_iptc_time(self):
        # datetime
        d = datetime.datetime(1899, 12, 31)
        self.assertEqual(DateTimeFormatter.iptc_time(d), '00:00:00+00:00')
        d = datetime.datetime(1899, 12, 31, 23)
        self.assertEqual(DateTimeFormatter.iptc_time(d), '23:00:00+00:00')
        d = datetime.datetime(1899, 12, 31, 23, 59)
        self.assertEqual(DateTimeFormatter.iptc_time(d), '23:59:00+00:00')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59)
        self.assertEqual(DateTimeFormatter.iptc_time(d), '23:59:59+00:00')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, 999999)
        self.assertEqual(DateTimeFormatter.iptc_time(d), '23:59:59+00:00')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, tzinfo=FixedOffset())
        self.assertEqual(DateTimeFormatter.iptc_time(d), '23:59:59+00:00')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, tzinfo=FixedOffset(hours=5))
        self.assertEqual(DateTimeFormatter.iptc_time(d), '23:59:59+05:00')
        d = datetime.datetime(2011, 8, 8, 19, 3, 37)
        self.assertEqual(DateTimeFormatter.iptc_time(d), '19:03:37+00:00')

        # time
        d = datetime.time(23)
        self.assertEqual(DateTimeFormatter.iptc_time(d), '23:00:00+00:00')
        d = datetime.time(23, 59)
        self.assertEqual(DateTimeFormatter.iptc_time(d), '23:59:00+00:00')
        d = datetime.time(23, 59, 59)
        self.assertEqual(DateTimeFormatter.iptc_time(d), '23:59:59+00:00')
        d = datetime.time(23, 59, 59, 999999)
        self.assertEqual(DateTimeFormatter.iptc_time(d), '23:59:59+00:00')
        d = datetime.time(23, 59, 59, tzinfo=FixedOffset())
        self.assertEqual(DateTimeFormatter.iptc_time(d), '23:59:59+00:00')
        d = datetime.time(23, 59, 59, tzinfo=FixedOffset(hours=5))
        self.assertEqual(DateTimeFormatter.iptc_time(d), '23:59:59+05:00')
        d = datetime.time(19, 3, 37)
        self.assertEqual(DateTimeFormatter.iptc_time(d), '19:03:37+00:00')

        # invalid type
        self.assertRaises(TypeError, DateTimeFormatter.iptc_time, None)
        self.assertRaises(TypeError, DateTimeFormatter.iptc_time, 3.14)

    def test_xmp(self):
        # datetime
        d = datetime.datetime(1899, 12, 31)
        self.assertEqual(DateTimeFormatter.xmp(d), '1899-12-31')
        d = datetime.datetime(1899, 12, 31, tzinfo=FixedOffset())
        self.assertEqual(DateTimeFormatter.xmp(d), '1899-12-31')
        d = datetime.datetime(1899, 12, 31, 23, 59)
        self.assertEqual(DateTimeFormatter.xmp(d), '1899-12-31T23:59Z')
        d = datetime.datetime(1899, 12, 31, 23, 59, tzinfo=FixedOffset())
        self.assertEqual(DateTimeFormatter.xmp(d), '1899-12-31T23:59Z')
        d = datetime.datetime(1899, 12, 31, 23, 59, tzinfo=FixedOffset(hours=3))
        self.assertEqual(DateTimeFormatter.xmp(d), '1899-12-31T23:59+03:00')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59)
        self.assertEqual(DateTimeFormatter.xmp(d), '1899-12-31T23:59:59Z')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, tzinfo=FixedOffset())
        self.assertEqual(DateTimeFormatter.xmp(d), '1899-12-31T23:59:59Z')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, tzinfo=FixedOffset(hours=3))
        self.assertEqual(DateTimeFormatter.xmp(d), '1899-12-31T23:59:59+03:00')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, 999999)
        self.assertEqual(DateTimeFormatter.xmp(d), '1899-12-31T23:59:59.999999Z')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, 999999, tzinfo=FixedOffset())
        self.assertEqual(DateTimeFormatter.xmp(d), '1899-12-31T23:59:59.999999Z')
        d = datetime.datetime(1899, 12, 31, 23, 59, 59, 999999, tzinfo=FixedOffset(hours=3))
        self.assertEqual(DateTimeFormatter.xmp(d), '1899-12-31T23:59:59.999999+03:00')
        d = datetime.datetime(2011, 8, 11, 9, 23, 44)
        self.assertEqual(DateTimeFormatter.xmp(d), '2011-08-11T09:23:44Z')

        # date
        d = datetime.date(1899, 12, 31)
        self.assertEqual(DateTimeFormatter.xmp(d), '1899-12-31')
        d = datetime.date(2011, 8, 8)
        self.assertEqual(DateTimeFormatter.xmp(d), '2011-08-08')

        # invalid type
        self.assertRaises(TypeError, DateTimeFormatter.xmp, None)
        self.assertRaises(TypeError, DateTimeFormatter.xmp, 3.14)

