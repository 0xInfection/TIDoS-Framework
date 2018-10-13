# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2009-2010 Olivier Tilloy <olivier@tilloy.net>
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
from pyexiv2.utils import ListenerInterface, NotifyingList
import random


class SimpleListener(ListenerInterface):

    def __init__(self):
        self.changes = 0

    def contents_changed(self):
        self.changes += 1


class TestNotifyingList(unittest.TestCase):

    def setUp(self):
        self.values = NotifyingList([5, 7, 9, 14, 57, 3, 2])

    def test_no_listener(self):
        # No listener is registered, nothing should happen.
        self.values[3] = 13
        del self.values[5]
        self.values.append(17)
        self.values.extend([11, 22])
        self.values.insert(4, 24)
        self.values.pop()
        self.values.remove(9)
        self.values.reverse()
        self.values.sort()
        self.values += [8, 4]
        self.values *= 3
        self.values[3:4] = [8, 4]
        del self.values[3:5]

    def test_listener_interface(self):
        self.values.register_listener(ListenerInterface())
        self.failUnlessRaises(NotImplementedError,
                              self.values.__setitem__, 3, 13)
        self.failUnlessRaises(NotImplementedError, self.values.__delitem__, 5)
        self.failUnlessRaises(NotImplementedError, self.values.append, 17)
        self.failUnlessRaises(NotImplementedError, self.values.extend, [11, 22])
        self.failUnlessRaises(NotImplementedError, self.values.insert, 4, 24)
        self.failUnlessRaises(NotImplementedError, self.values.pop)
        self.failUnlessRaises(NotImplementedError, self.values.remove, 9)
        self.failUnlessRaises(NotImplementedError, self.values.reverse)
        self.failUnlessRaises(NotImplementedError, self.values.sort)
        self.failUnlessRaises(NotImplementedError, self.values.__iadd__, [8, 4])
        self.failUnlessRaises(NotImplementedError, self.values.__imul__, 3)
        self.failUnlessRaises(NotImplementedError, self.values.__setslice__,
                              3, 4, [8, 4])
        self.failUnlessRaises(NotImplementedError, self.values.__delslice__,
                              3, 5)

    def _register_listeners(self):
        # Register a random number of listeners
        listeners = [SimpleListener() for i in xrange(random.randint(3, 20))]
        for listener in listeners:
            self.values.register_listener(listener)
        return listeners

    def test_setitem(self):
        listeners = self._register_listeners()

        self.values[3] = 13
        self.failUnlessEqual(self.values, [5, 7, 9, 13, 57, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

        self.failUnlessRaises(IndexError, self.values.__setitem__, 9, 27)
        self.failUnlessEqual(self.values, [5, 7, 9, 13, 57, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

    def test_delitem(self):
        listeners = self._register_listeners()

        del self.values[5]
        self.failUnlessEqual(self.values, [5, 7, 9, 14, 57, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

        self.failUnlessRaises(IndexError, self.values.__delitem__, 9)
        self.failUnlessEqual(self.values, [5, 7, 9, 14, 57, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

    def test_append(self):
        listeners = self._register_listeners()

        self.values.append(17)
        self.failUnlessEqual(self.values, [5, 7, 9, 14, 57, 3, 2, 17])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

    def test_extend(self):
        listeners = self._register_listeners()

        self.values.extend([11, 22])
        self.failUnlessEqual(self.values, [5, 7, 9, 14, 57, 3, 2, 11, 22])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

        self.failUnlessRaises(TypeError, self.values.extend, 26)
        self.failUnlessEqual(self.values, [5, 7, 9, 14, 57, 3, 2, 11, 22])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

    def test_insert(self):
        listeners = self._register_listeners()

        self.values.insert(4, 24)
        self.failUnlessEqual(self.values, [5, 7, 9, 14, 24, 57, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

    def test_pop(self):
        listeners = self._register_listeners()

        self.values.pop()
        self.failUnlessEqual(self.values, [5, 7, 9, 14, 57, 3])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

        self.values.pop(4)
        self.failUnlessEqual(self.values, [5, 7, 9, 14, 3])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 2)

        self.values.pop(-2)
        self.failUnlessEqual(self.values, [5, 7, 9, 3])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 3)

        self.failUnlessRaises(IndexError, self.values.pop, 33)
        self.failUnlessEqual(self.values, [5, 7, 9, 3])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 3)

    def test_remove(self):
        listeners = self._register_listeners()

        self.values.remove(9)
        self.failUnlessEqual(self.values, [5, 7, 14, 57, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

        self.failUnlessRaises(ValueError, self.values.remove, 33)
        self.failUnlessEqual(self.values, [5, 7, 14, 57, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

    def test_reverse(self):
        listeners = self._register_listeners()

        self.values.reverse()
        self.failUnlessEqual(self.values, [2, 3, 57, 14, 9, 7, 5])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

    def test_sort(self):
        listeners = self._register_listeners()

        self.values.sort()
        self.failUnlessEqual(self.values, [2, 3, 5, 7, 9, 14, 57])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

        self.values.sort(cmp=lambda x, y: y - x)
        self.failUnlessEqual(self.values, [57, 14, 9, 7, 5, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 2)

        self.values.sort(key=lambda x: x * x)
        self.failUnlessEqual(self.values, [2, 3, 5, 7, 9, 14, 57])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 3)

        self.values.sort(reverse=True)
        self.failUnlessEqual(self.values, [57, 14, 9, 7, 5, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 4)

    def test_iadd(self):
        listeners = self._register_listeners()

        self.values += [44, 31, 19]
        self.failUnlessEqual(self.values, [5, 7, 9, 14, 57, 3, 2, 44, 31, 19])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

    def test_imul(self):
        listeners = self._register_listeners()

        self.values *= 3
        self.failUnlessEqual(self.values,
                             [5, 7, 9, 14, 57, 3, 2,
                              5, 7, 9, 14, 57, 3, 2,
                              5, 7, 9, 14, 57, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

    def test_setslice(self):
        listeners = self._register_listeners()

        # Basic slicing (of the form [i:j]): implemented as __setslice__.

        self.values[2:4] = [3, 4]
        self.failUnlessEqual(self.values, [5, 7, 3, 4, 57, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

        self.values[3:5] = [77, 8, 12]
        self.failUnlessEqual(self.values, [5, 7, 3, 77, 8, 12, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 2)

        self.values[2:5] = [1, 0]
        self.failUnlessEqual(self.values, [5, 7, 1, 0, 12, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 3)

        self.values[0:2] = []
        self.failUnlessEqual(self.values, [1, 0, 12, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 4)

        self.values[2:2] = [7, 5]
        self.failUnlessEqual(self.values, [1, 0, 7, 5, 12, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 5)

        # With negatives indexes

        self.values[4:-2] = [9]
        self.failUnlessEqual(self.values, [1, 0, 7, 5, 9, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 6)

        self.values[-2:1] = [6, 4]
        self.failUnlessEqual(self.values, [1, 0, 7, 5, 9, 6, 4, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 7)

        self.values[-5:-2] = [8]
        self.failUnlessEqual(self.values, [1, 0, 7, 5, 8, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 8)

        # With missing (implicit) indexes

        self.values[:2] = [4]
        self.failUnlessEqual(self.values, [4, 7, 5, 8, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 9)

        self.values[4:] = [1]
        self.failUnlessEqual(self.values, [4, 7, 5, 8, 1])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 10)

        self.values[:] = [5, 7, 9, 14, 57, 3, 2]
        self.failUnlessEqual(self.values, [5, 7, 9, 14, 57, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 11)

    def test_delslice(self):
        listeners = self._register_listeners()

        del self.values[2:3]
        self.failUnlessEqual(self.values, [5, 7, 14, 57, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

        del self.values[2:2]
        self.failUnlessEqual(self.values, [5, 7, 14, 57, 3, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 1)

        # With negatives indexes

        del self.values[4:-1]
        self.failUnlessEqual(self.values, [5, 7, 14, 57, 2])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 2)

        del self.values[-1:5]
        self.failUnlessEqual(self.values, [5, 7, 14, 57])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 3)

        del self.values[-2:-1]
        self.failUnlessEqual(self.values, [5, 7, 57])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 4)

        # With missing (implicit) indexes

        del self.values[:1]
        self.failUnlessEqual(self.values, [7, 57])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 5)

        del self.values[1:]
        self.failUnlessEqual(self.values, [7])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 6)

        del self.values[:]
        self.failUnlessEqual(self.values, [])
        for listener in listeners:
            self.failUnlessEqual(listener.changes, 7)
