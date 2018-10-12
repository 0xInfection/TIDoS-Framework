# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2008-2010 Olivier Tilloy <olivier@tilloy.net>
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

from pyexiv2.utils import Rational


class TestRational(unittest.TestCase):

    def test_constructor(self):
        r = Rational(2, 1)
        self.assertEqual(r.numerator, 2)
        self.assertEqual(r.denominator, 1)
        self.assertRaises(ZeroDivisionError, Rational, 1, 0)

    def test_read_only(self):
        r = Rational(3, 4)
        try:
            r.numerator = 5
        except AttributeError:
            pass
        else:
            self.fail('Numerator is not read-only.')
        try:
            r.denominator = 5
        except AttributeError:
            pass
        else:
            self.fail('Denominator is not read-only.')

    def test_match_string(self):
        self.assertEqual(Rational.match_string('4/3'), (4, 3))
        self.assertEqual(Rational.match_string('-4/3'), (-4, 3))
        self.assertEqual(Rational.match_string('0/3'), (0, 3))
        self.assertEqual(Rational.match_string('0/0'), (0, 0))
        self.assertRaises(ValueError, Rational.match_string, '+3/5')
        self.assertRaises(ValueError, Rational.match_string, '3 / 5')
        self.assertRaises(ValueError, Rational.match_string, '3/-5')
        self.assertRaises(ValueError, Rational.match_string, 'invalid')

    def test_from_string(self):
        self.assertEqual(Rational.from_string('4/3'), Rational(4, 3))
        self.assertEqual(Rational.from_string('-4/3'), Rational(-4, 3))
        self.assertRaises(ValueError, Rational.from_string, '+3/5')
        self.assertRaises(ValueError, Rational.from_string, '3 / 5')
        self.assertRaises(ValueError, Rational.from_string, '3/-5')
        self.assertRaises(ValueError, Rational.from_string, 'invalid')
        self.assertRaises(ZeroDivisionError, Rational.from_string, '1/0')
        self.assertRaises(ZeroDivisionError, Rational.from_string, '0/0')

    def test_to_string(self):
        self.assertEqual(str(Rational(3, 5)), '3/5')
        self.assertEqual(str(Rational(-3, 5)), '-3/5')

    def test_repr(self):
        self.assertEqual(repr(Rational(3, 5)), 'Rational(3, 5)')
        self.assertEqual(repr(Rational(-3, 5)), 'Rational(-3, 5)')
        self.assertEqual(repr(Rational(0, 3)), 'Rational(0, 3)')

    def test_to_float(self):
        self.assertEqual(Rational(3, 6).to_float(), 0.5)
        self.assertEqual(Rational(11, 11).to_float(), 1.0)
        self.assertEqual(Rational(-2, 8).to_float(), -0.25)
        self.assertEqual(Rational(0, 3).to_float(), 0.0)

    def test_equality(self):
        r1 = Rational(2, 1)
        r2 = Rational(2, 1)
        r3 = Rational(8, 4)
        r4 = Rational(3, 2)
        self.assertEqual(r1, r2)
        self.assertEqual(r1, r3)
        self.assertNotEqual(r1, r4)
