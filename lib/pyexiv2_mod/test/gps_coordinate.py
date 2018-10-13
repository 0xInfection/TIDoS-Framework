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

from pyexiv2.utils import GPSCoordinate


class TestGPSCoordinate(unittest.TestCase):

    def test_constructor(self):
        r = GPSCoordinate(62, 58, 2, 'W')
        self.assertEqual(r.degrees, 62)
        self.assertEqual(r.minutes, 58)
        self.assertEqual(r.seconds, 2)
        self.assertEqual(r.direction, 'W')
        r = GPSCoordinate(92, 58, 2, 'W')
        self.assertEqual(r.degrees, 92)
        self.assertEqual(r.minutes, 58)
        self.assertEqual(r.seconds, 2)
        self.assertEqual(r.direction, 'W')
        self.assertRaises(ValueError, GPSCoordinate, -23, 58, 2, 'W')
        self.assertRaises(ValueError, GPSCoordinate, 91, 58, 2, 'S')
        self.assertRaises(ValueError, GPSCoordinate, 62, -23, 2, 'W')
        self.assertRaises(ValueError, GPSCoordinate, 62, 61, 2, 'W')
        self.assertRaises(ValueError, GPSCoordinate, 62, 58, -23, 'W')
        self.assertRaises(ValueError, GPSCoordinate, 62, 58, 61, 'W')
        self.assertRaises(ValueError, GPSCoordinate, 62, 58, 2, 'A')

    def test_read_only(self):
        r = GPSCoordinate(62, 58, 2, 'W')
        try:
            r.degrees = 5
        except AttributeError:
            pass
        else:
            self.fail('Degrees is not read-only.')
        try:
            r.minutes = 5
        except AttributeError:
            pass
        else:
            self.fail('Minutes is not read-only.')
        try:
            r.seconds = 5
        except AttributeError:
            pass
        else:
            self.fail('Seconds is not read-only.')
        try:
            r.direction = 'S'
        except AttributeError:
            pass
        else:
            self.fail('Direction is not read-only.')

    def test_from_string(self):
        self.assertEqual(GPSCoordinate.from_string('54,59.380000N'),
                         GPSCoordinate(54, 59, 23, 'N'))
        self.assertEqual(GPSCoordinate.from_string('1,54.850000W'),
                         GPSCoordinate(1, 54, 51, 'W'))
        self.assertRaises(ValueError, GPSCoordinate.from_string, '51N')
        self.assertRaises(ValueError, GPSCoordinate.from_string, '48 24 3 S')
        self.assertRaises(ValueError, GPSCoordinate.from_string, '48°24\'3"S')
        self.assertRaises(ValueError, GPSCoordinate.from_string, 'invalid')

    def test_to_string(self):
        self.assertEqual(str(GPSCoordinate(54, 59, 23, 'N')), '54,59,23N')

