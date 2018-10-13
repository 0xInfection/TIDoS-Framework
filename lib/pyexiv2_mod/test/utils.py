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

from pyexiv2.utils import undefined_to_string, string_to_undefined, \
                          Rational, Fraction, \
                          is_fraction, make_fraction, fraction_to_string


class TestConversions(unittest.TestCase):

    def test_undefined_to_string(self):
        self.assertEqual(undefined_to_string("48 50 50 49"), "0221")
        self.assertEqual(undefined_to_string("48 50 50 49 "), "0221")
        self.assertRaises(ValueError, undefined_to_string, "")
        self.assertRaises(ValueError, undefined_to_string, "foo")
        self.assertRaises(ValueError, undefined_to_string, "48 50  50 49")

    def test_string_to_undefined(self):
        self.assertEqual(string_to_undefined("0221"), "48 50 50 49")
        self.assertEqual(string_to_undefined(""), "")

    def test_identity(self):
        value = "0221"
        self.assertEqual(undefined_to_string(string_to_undefined(value)), value)
        value = "48 50 50 49"
        self.assertEqual(string_to_undefined(undefined_to_string(value)), value)


class TestFractions(unittest.TestCase):

    def test_is_fraction(self):
        if Fraction is not None:
            self.failUnless(is_fraction(Fraction()))
            self.failUnless(is_fraction(Fraction(3, 5)))
            self.failUnless(is_fraction(Fraction(Fraction(4, 5))))
            self.failUnless(is_fraction(Fraction('3/2')))
            self.failUnless(is_fraction(Fraction('-4/5')))
        self.failUnless(is_fraction(Rational(3, 5)))
        self.failUnless(is_fraction(Rational(-4, 5)))
        self.failUnless(is_fraction(Rational.from_string("3/5")))
        self.failUnless(is_fraction(Rational.from_string("-4/5")))

        self.failIf(is_fraction(3 / 5))
        self.failIf(is_fraction('3/5'))
        self.failIf(is_fraction('2.7'))
        self.failIf(is_fraction(2.7))
        self.failIf(is_fraction('notafraction'))
        self.failIf(is_fraction(None))

    def test_make_fraction(self):
        if Fraction is not None:
            self.assertEqual(make_fraction(3, 5), Fraction(3, 5))
            self.assertEqual(make_fraction(-3, 5), Fraction(-3, 5))
            self.assertEqual(make_fraction('3/2'), Fraction(3, 2))
            self.assertEqual(make_fraction('-3/4'), Fraction(-3, 4))
            self.assertEqual(make_fraction('0/0'), Fraction(0, 1))
        else:
            self.assertEqual(make_fraction(3, 5), Rational(3, 5))
            self.assertEqual(make_fraction(-3, 5), Rational(-3, 5))
            self.assertEqual(make_fraction('3/2'), Rational(3, 2))
            self.assertEqual(make_fraction('-3/4'), Rational(-3, 4))
            self.assertEqual(make_fraction('0/0'), Rational(0, 1))

        self.assertRaises(ZeroDivisionError, make_fraction, 3, 0)
        self.assertRaises(ZeroDivisionError, make_fraction, '3/0')
        self.assertRaises(TypeError, make_fraction, 5, 3, 2)
        self.assertRaises(TypeError, make_fraction, None)

    def test_fraction_to_string(self):
        self.assertEqual(fraction_to_string(make_fraction(3, 5)), '3/5')
        self.assertEqual(fraction_to_string(make_fraction(-3, 5)), '-3/5')
        self.assertEqual(fraction_to_string(make_fraction(0, 1)), '0/1')
        self.assertRaises(TypeError, fraction_to_string, None)
        self.assertRaises(TypeError, fraction_to_string, 'invalid')

