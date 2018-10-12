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

from pyexiv2.xmp import XmpTag, XmpValueError, register_namespace, \
                        unregister_namespace, unregister_namespaces
from pyexiv2.utils import FixedOffset, make_fraction
from pyexiv2.metadata import ImageMetadata

import datetime
from testutils import EMPTY_JPG_DATA

# Optional dependency on python-tz, more tests can be run if it is installed
try:
    import pytz
except ImportError:
    pytz = None


class TestXmpTag(unittest.TestCase):

    def test_convert_to_python_bag(self):
        # Valid values
        tag = XmpTag('Xmp.dc.subject')
        self.assertEqual(tag.type, 'bag Text')
        self.assertEqual(tag._convert_to_python('', 'Text'), u'')
        self.assertEqual(tag._convert_to_python('One value only', 'Text'),
                         u'One value only')

    def test_convert_to_string_bag(self):
        # Valid values
        tag = XmpTag('Xmp.dc.subject')
        self.assertEqual(tag.type, 'bag Text')
        self.assertEqual(tag._convert_to_string(u'', 'Text'), '')
        self.assertEqual(tag._convert_to_string('One value only', 'Text'), 'One value only')
        self.assertEqual(tag._convert_to_string(u'One value only', 'Text'), 'One value only')
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, [1, 2, 3], 'Text')

    def test_convert_to_python_boolean(self):
        # Valid values
        tag = XmpTag('Xmp.xmpRights.Marked')
        self.assertEqual(tag.type, 'Boolean')
        self.assertEqual(tag._convert_to_python('True', 'Boolean'), True)
        self.assertEqual(tag._convert_to_python('False', 'Boolean'), False)
        # Invalid values: not converted
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, 'invalid', 'Boolean')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, None, 'Boolean')

    def test_convert_to_string_boolean(self):
        # Valid values
        tag = XmpTag('Xmp.xmpRights.Marked')
        self.assertEqual(tag.type, 'Boolean')
        self.assertEqual(tag._convert_to_string(True, 'Boolean'), 'True')
        self.assertEqual(tag._convert_to_string(False, 'Boolean'), 'False')
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, 'invalid', 'Boolean')
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, None, 'Boolean')

    def test_convert_to_python_date(self):
        # Valid values
        tag = XmpTag('Xmp.xmp.CreateDate')
        self.assertEqual(tag.type, 'Date')
        self.assertEqual(tag._convert_to_python('1999', 'Date'),
                         datetime.date(1999, 1, 1))
        self.assertEqual(tag._convert_to_python('1999-10', 'Date'),
                         datetime.date(1999, 10, 1))
        self.assertEqual(tag._convert_to_python('1999-10-13', 'Date'),
                         datetime.date(1999, 10, 13))
        self.assertEqual(tag._convert_to_python('1999-10-13T05:03Z', 'Date') - \
                         datetime.datetime(1999, 10, 13, 5, 3, tzinfo=FixedOffset()),
                         datetime.timedelta(0))
        self.assertEqual(tag._convert_to_python('1999-10-13T05:03+06:00', 'Date') - \
                         datetime.datetime(1999, 10, 13, 5, 3, tzinfo=FixedOffset('+', 6, 0)),
                         datetime.timedelta(0))
        self.assertEqual(tag._convert_to_python('1999-10-13T05:03-06:00', 'Date') - \
                         datetime.datetime(1999, 10, 13, 5, 3, tzinfo=FixedOffset('-', 6, 0)),
                         datetime.timedelta(0))
        self.assertEqual(tag._convert_to_python('1999-10-13T05:03:54Z', 'Date') - \
                         datetime.datetime(1999, 10, 13, 5, 3, 54, tzinfo=FixedOffset()),
                         datetime.timedelta(0))
        self.assertEqual(tag._convert_to_python('1999-10-13T05:03:54+06:00', 'Date') - \
                         datetime.datetime(1999, 10, 13, 5, 3, 54, tzinfo=FixedOffset('+', 6, 0)),
                         datetime.timedelta(0))
        self.assertEqual(tag._convert_to_python('1999-10-13T05:03:54-06:00', 'Date') - \
                         datetime.datetime(1999, 10, 13, 5, 3, 54, tzinfo=FixedOffset('-', 6, 0)),
                         datetime.timedelta(0))
        self.assertEqual(tag._convert_to_python('1999-10-13T05:03:54.721Z', 'Date') - \
                         datetime.datetime(1999, 10, 13, 5, 3, 54, 721000, tzinfo=FixedOffset()),
                         datetime.timedelta(0))
        self.assertEqual(tag._convert_to_python('1999-10-13T05:03:54.721+06:00', 'Date') - \
                         datetime.datetime(1999, 10, 13, 5, 3, 54, 721000, tzinfo=FixedOffset('+', 6, 0)),
                         datetime.timedelta(0))
        self.assertEqual(tag._convert_to_python('1999-10-13T05:03:54.721-06:00', 'Date') - \
                         datetime.datetime(1999, 10, 13, 5, 3, 54, 721000, tzinfo=FixedOffset('-', 6, 0)),
                         datetime.timedelta(0))
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, 'invalid', 'Date')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, '11/10/1983', 'Date')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, '-1000', 'Date')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, '2009-13', 'Date')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, '2009-10-32', 'Date')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, '2009-10-30T25:12Z', 'Date')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, '2009-10-30T23:67Z', 'Date')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, '2009-01-22T21', 'Date')

    def test_convert_to_string_date(self):
        # Valid values
        tag = XmpTag('Xmp.xmp.CreateDate')
        self.assertEqual(tag.type, 'Date')
        self.assertEqual(tag._convert_to_string(datetime.date(2009, 2, 4), 'Date'),
                         '2009-02-04')
        self.assertEqual(tag._convert_to_string(datetime.date(1899, 12, 31), 'Date'),
                         '1899-12-31')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13), 'Date'),
                         '1999-10-13')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3), 'Date'),
                         '1999-10-13T05:03Z')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59), 'Date'),
                         '1899-12-31T23:59Z')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, tzinfo=FixedOffset()), 'Date'),
                         '1999-10-13T05:03Z')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, tzinfo=FixedOffset()), 'Date'),
                         '1899-12-31T23:59Z')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, tzinfo=FixedOffset('+', 5, 30)), 'Date'),
                         '1999-10-13T05:03+05:30')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, tzinfo=FixedOffset('-', 11, 30)), 'Date'),
                         '1999-10-13T05:03-11:30')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, tzinfo=FixedOffset('+', 5, 30)), 'Date'),
                         '1899-12-31T23:59+05:30')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27), 'Date'),
                         '1999-10-13T05:03:27Z')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, 59), 'Date'),
                         '1899-12-31T23:59:59Z')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27, tzinfo=FixedOffset()), 'Date'),
                         '1999-10-13T05:03:27Z')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, 59, tzinfo=FixedOffset()), 'Date'),
                         '1899-12-31T23:59:59Z')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27, tzinfo=FixedOffset('+', 5, 30)), 'Date'),
                         '1999-10-13T05:03:27+05:30')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27, tzinfo=FixedOffset('-', 11, 30)), 'Date'),
                         '1999-10-13T05:03:27-11:30')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, 59, tzinfo=FixedOffset('+', 5, 30)), 'Date'),
                         '1899-12-31T23:59:59+05:30')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27, 124300), 'Date'),
                         '1999-10-13T05:03:27.1243Z')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, 59, 124300), 'Date'),
                         '1899-12-31T23:59:59.1243Z')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27, 124300, tzinfo=FixedOffset()), 'Date'),
                         '1999-10-13T05:03:27.1243Z')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, 59, 124300, tzinfo=FixedOffset()), 'Date'),
                         '1899-12-31T23:59:59.1243Z')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27, 124300, tzinfo=FixedOffset('+', 5, 30)), 'Date'),
                         '1999-10-13T05:03:27.1243+05:30')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27, 124300, tzinfo=FixedOffset('-', 11, 30)), 'Date'),
                         '1999-10-13T05:03:27.1243-11:30')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, 59, 124300, tzinfo=FixedOffset('+', 5, 30)), 'Date'),
                         '1899-12-31T23:59:59.1243+05:30')
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, 'invalid', 'Date')
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, None, 'Date')

    def test_convert_to_string_date_with_real_timezones(self):
        if pytz is None:
            # Poor man’s test skipping. Starting with Python 2.7, decorators are
            # available to implement this in a cleaner fashion
            # (http://docs.python.org/library/unittest.html#unittest-skipping).
            print 'Install python-tz to run this test. Skipping.'
            return
        tag = XmpTag('Xmp.xmp.CreateDate')
        self.assertEqual(tag.type, 'Date')
        t = pytz.timezone('UTC').localize(datetime.datetime(2011, 2, 2, 10, 52, 4))
        self.assertEqual(tag._convert_to_string(t, 'Date'), '2011-02-02T10:52:04Z')
        t = pytz.timezone('CET').localize(datetime.datetime(2011, 2, 2, 10, 52, 4))
        self.assertEqual(tag._convert_to_string(t, 'Date'), '2011-02-02T10:52:04+01:00')

    def test_convert_to_python_integer(self):
        # Valid values
        tag = XmpTag('Xmp.xmpMM.SaveID')
        self.assertEqual(tag.type, 'Integer')
        self.assertEqual(tag._convert_to_python('23', 'Integer'), 23)
        self.assertEqual(tag._convert_to_python('+5628', 'Integer'), 5628)
        self.assertEqual(tag._convert_to_python('-4', 'Integer'), -4)
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, 'abc', 'Integer')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, '5,64', 'Integer')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, '47.0001', 'Integer')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, '1E3', 'Integer')

    def test_convert_to_string_integer(self):
        # Valid values
        tag = XmpTag('Xmp.xmpMM.SaveID')
        self.assertEqual(tag.type, 'Integer')
        self.assertEqual(tag._convert_to_string(123, 'Integer'), '123')
        self.assertEqual(tag._convert_to_string(-57, 'Integer'), '-57')
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, 'invalid', 'Integer')
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, 3.14, 'Integer')

    def test_convert_to_python_mimetype(self):
        # Valid values
        tag = XmpTag('Xmp.dc.format')
        self.assertEqual(tag.type, 'MIMEType')
        self.assertEqual(tag._convert_to_python('image/jpeg', 'MIMEType'),
                         ('image', 'jpeg'))
        self.assertEqual(tag._convert_to_python('video/ogg', 'MIMEType'),
                         ('video', 'ogg'))
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, 'invalid', 'MIMEType')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, 'image-jpeg', 'MIMEType')

    def test_convert_to_string_mimetype(self):
        # Valid values
        tag = XmpTag('Xmp.dc.format')
        self.assertEqual(tag.type, 'MIMEType')
        self.assertEqual(tag._convert_to_string(('image', 'jpeg'), 'MIMEType'), 'image/jpeg')
        self.assertEqual(tag._convert_to_string(('video', 'ogg'), 'MIMEType'), 'video/ogg')
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, 'invalid', 'MIMEType')
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, ('image',), 'MIMEType')

    def test_convert_to_python_propername(self):
        # Valid values
        tag = XmpTag('Xmp.photoshop.CaptionWriter')
        self.assertEqual(tag.type, 'ProperName')
        self.assertEqual(tag._convert_to_python('Gérard', 'ProperName'), u'Gérard')
        self.assertEqual(tag._convert_to_python('Python Software Foundation', 'ProperName'), u'Python Software Foundation')
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, None, 'ProperName')

    def test_convert_to_string_propername(self):
        # Valid values
        tag = XmpTag('Xmp.photoshop.CaptionWriter')
        self.assertEqual(tag.type, 'ProperName')
        self.assertEqual(tag._convert_to_string('Gérard', 'ProperName'), 'Gérard')
        self.assertEqual(tag._convert_to_string(u'Gérard', 'ProperName'), 'Gérard')
        self.assertEqual(tag._convert_to_string(u'Python Software Foundation', 'ProperName'), 'Python Software Foundation')
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, None, 'ProperName')

    def test_convert_to_python_text(self):
        # Valid values
        tag = XmpTag('Xmp.dc.source')
        self.assertEqual(tag.type, 'Text')
        self.assertEqual(tag._convert_to_python('Some text.', 'Text'), u'Some text.')
        self.assertEqual(tag._convert_to_python('Some text with exotic chàräctérʐ.', 'Text'),
                         u'Some text with exotic chàräctérʐ.')
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, None, 'Text')

    def test_convert_to_string_text(self):
        # Valid values
        tag = XmpTag('Xmp.dc.source')
        self.assertEqual(tag.type, 'Text')
        self.assertEqual(tag._convert_to_string(u'Some text', 'Text'), 'Some text')
        self.assertEqual(tag._convert_to_string(u'Some text with exotic chàräctérʐ.', 'Text'),
                         'Some text with exotic chàräctérʐ.')
        self.assertEqual(tag._convert_to_string('Some text with exotic chàräctérʐ.', 'Text'),
                         'Some text with exotic chàräctérʐ.')
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, None, 'Text')

    def test_convert_to_python_uri(self):
        # Valid values
        tag = XmpTag('Xmp.xmpMM.DocumentID')
        self.assertEqual(tag.type, 'URI')
        self.assertEqual(tag._convert_to_python('http://example.com', 'URI'), 'http://example.com')
        self.assertEqual(tag._convert_to_python('https://example.com', 'URI'), 'https://example.com')
        self.assertEqual(tag._convert_to_python('http://localhost:8000/resource', 'URI'),
                         'http://localhost:8000/resource')
        self.assertEqual(tag._convert_to_python('uuid:9A3B7F52214211DAB6308A7391270C13', 'URI'),
                         'uuid:9A3B7F52214211DAB6308A7391270C13')

    def test_convert_to_string_uri(self):
        # Valid values
        tag = XmpTag('Xmp.xmpMM.DocumentID')
        self.assertEqual(tag.type, 'URI')
        self.assertEqual(tag._convert_to_string('http://example.com', 'URI'), 'http://example.com')
        self.assertEqual(tag._convert_to_string(u'http://example.com', 'URI'), 'http://example.com')
        self.assertEqual(tag._convert_to_string('https://example.com', 'URI'), 'https://example.com')
        self.assertEqual(tag._convert_to_string('http://localhost:8000/resource', 'URI'),
                         'http://localhost:8000/resource')
        self.assertEqual(tag._convert_to_string('uuid:9A3B7F52214211DAB6308A7391270C13', 'URI'),
                         'uuid:9A3B7F52214211DAB6308A7391270C13')
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, None, 'URI')

    def test_convert_to_python_url(self):
        # Valid values
        tag = XmpTag('Xmp.xmp.BaseURL')
        self.assertEqual(tag.type, 'URL')
        self.assertEqual(tag._convert_to_python('http://example.com', 'URL'), 'http://example.com')
        self.assertEqual(tag._convert_to_python('https://example.com', 'URL'), 'https://example.com')
        self.assertEqual(tag._convert_to_python('http://localhost:8000/resource', 'URL'),
                         'http://localhost:8000/resource')

    def test_convert_to_string_url(self):
        # Valid values
        tag = XmpTag('Xmp.xmp.BaseURL')
        self.assertEqual(tag.type, 'URL')
        self.assertEqual(tag._convert_to_string('http://example.com', 'URL'), 'http://example.com')
        self.assertEqual(tag._convert_to_string(u'http://example.com', 'URL'), 'http://example.com')
        self.assertEqual(tag._convert_to_string('https://example.com', 'URL'), 'https://example.com')
        self.assertEqual(tag._convert_to_string('http://localhost:8000/resource', 'URL'),
                         'http://localhost:8000/resource')
        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, None, 'URL')

    def test_convert_to_python_rational(self):
        # Valid values
        tag = XmpTag('Xmp.xmpDM.videoPixelAspectRatio')
        self.assertEqual(tag.type, 'Rational')
        self.assertEqual(tag._convert_to_python('5/3', 'Rational'), make_fraction(5, 3))
        self.assertEqual(tag._convert_to_python('-5/3', 'Rational'), make_fraction(-5, 3))

        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, 'invalid', 'Rational')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, '5 / 3', 'Rational')
        self.failUnlessRaises(XmpValueError, tag._convert_to_python, '5/-3', 'Rational')

    def test_convert_to_string_rational(self):
        # Valid values
        tag = XmpTag('Xmp.xmpDM.videoPixelAspectRatio')
        self.assertEqual(tag.type, 'Rational')
        self.assertEqual(tag._convert_to_string(make_fraction(5, 3), 'Rational'), '5/3')
        self.assertEqual(tag._convert_to_string(make_fraction(-5, 3), 'Rational'), '-5/3')

        # Invalid values
        self.failUnlessRaises(XmpValueError, tag._convert_to_string, 'invalid', 'Rational')

    # TODO: other types


    def test_set_value(self):
        tag = XmpTag('Xmp.xmp.ModifyDate', datetime.datetime(2005, 9, 7, 15, 9, 51, tzinfo=FixedOffset('-', 7, 0)))
        old_value = tag.value
        tag.value = datetime.datetime(2009, 4, 22, 8, 30, 27, tzinfo=FixedOffset())
        self.failIfEqual(tag.value, old_value)

    def test_set_value_empty(self):
        tag = XmpTag('Xmp.dc.creator')
        self.failUnlessEqual(tag.type, 'seq ProperName')
        self.failUnlessRaises(ValueError, setattr, tag, 'value', [])
        tag = XmpTag('Xmp.dc.title')
        self.failUnlessEqual(tag.type, 'Lang Alt')
        self.failUnlessRaises(ValueError, setattr, tag, 'value', {})

    def test_set_value_incorrect_type(self):
        # Expecting a list of values
        tag = XmpTag('Xmp.dc.publisher')
        self.failUnlessEqual(tag.type, 'bag ProperName')
        self.failUnlessRaises(TypeError, setattr, tag, 'value', None)
        self.failUnlessRaises(TypeError, setattr, tag, 'value', 'bleh')
        # Expecting a dictionary mapping language codes to values
        tag = XmpTag('Xmp.dc.description')
        self.failUnlessEqual(tag.type, 'Lang Alt')
        self.failUnlessRaises(TypeError, setattr, tag, 'value', None)
        self.failUnlessRaises(TypeError, setattr, tag, 'value', ['bleh'])

    def test_set_value_basestring_for_langalt(self):
        tag = XmpTag('Xmp.dc.description')
        self.failUnlessEqual(tag.type, 'Lang Alt')
        tag.value = 'bleh'
        self.failUnlessEqual(tag.value, {'x-default': 'bleh'})


class TestXmpNamespaces(unittest.TestCase):

    def setUp(self):
        self.metadata = ImageMetadata.from_buffer(EMPTY_JPG_DATA)
        self.metadata.read()

    def test_not_registered(self):
        self.assertEqual(len(self.metadata.xmp_keys), 0)
        key = 'Xmp.foo.bar'
        value = 'foobar'
        self.assertRaises(KeyError, self.metadata.__setitem__, key, value)

    def test_name_must_end_with_slash(self):
        self.assertRaises(ValueError, register_namespace, 'foobar', 'foo')
        self.assertRaises(ValueError, unregister_namespace, 'foobar')

    def test_cannot_register_builtin(self):
        self.assertRaises(KeyError, register_namespace, 'foobar/', 'dc')

    def test_cannot_register_twice(self):
        name = 'foobar/'
        prefix = 'boo'
        register_namespace(name, prefix)
        self.assertRaises(KeyError, register_namespace, name, prefix)

    def test_register_and_set(self):
        register_namespace('foobar/', 'bar')
        key = 'Xmp.bar.foo'
        value = 'foobar'
        self.metadata[key] = value
        self.assert_(key in self.metadata.xmp_keys)

    def test_can_only_set_text_values(self):
        # At the moment custom namespaces only support setting simple text
        # values.
        register_namespace('foobar/', 'far')
        key = 'Xmp.far.foo'
        value = datetime.date.today()
        self.assertRaises(XmpValueError, self.metadata.__setitem__, key, value)
        value = datetime.datetime.now()
        self.assertRaises(XmpValueError, self.metadata.__setitem__, key, value)
        value = ['foo', 'bar']
        self.assertRaises(XmpValueError, self.metadata.__setitem__, key, value)
        value = {'x-default': 'foo', 'fr-FR': 'bar'}
        self.assertRaises(XmpValueError, self.metadata.__setitem__, key, value)
        value = 'simple text value'
        self.metadata[key] = value

    def test_cannot_unregister_builtin(self):
        name = 'http://purl.org/dc/elements/1.1/' # DC builtin namespace
        self.assertRaises(KeyError, unregister_namespace, name)

    def test_cannot_unregister_inexistent(self):
        name = 'boofar/'
        self.assertRaises(KeyError, unregister_namespace, name)

    def test_cannot_unregister_twice(self):
        name = 'bleh/'
        prefix = 'ble'
        register_namespace(name, prefix)
        unregister_namespace(name)
        self.assertRaises(KeyError, unregister_namespace, name)

    def test_unregister(self):
        name = 'blah/'
        prefix = 'bla'
        register_namespace(name, prefix)
        unregister_namespace(name)

    def test_unregister_invalidates_keys_in_ns(self):
        name = 'blih/'
        prefix = 'bli'
        register_namespace(name, prefix)
        key = 'Xmp.%s.blu' % prefix
        self.metadata[key] = 'foobar'
        self.assert_(key in self.metadata.xmp_keys)
        unregister_namespace(name)
        self.assertRaises(KeyError, self.metadata.write)

    def test_unregister_all_ns(self):
        # Unregistering all custom namespaces will always succeed, even if there
        # are no custom namespaces registered.
        unregister_namespaces()

        name = 'blop/'
        prefix = 'blo'
        register_namespace(name, prefix)
        self.metadata['Xmp.%s.bar' % prefix] = 'foobar'
        name2 = 'blup/'
        prefix2 = 'blu'
        register_namespace(name2, prefix2)
        self.metadata['Xmp.%s.bar' % prefix2] = 'foobar'
        unregister_namespaces()
        self.assertRaises(KeyError, self.metadata.__setitem__, 'Xmp.%s.baz' % prefix, 'foobaz')
        self.assertRaises(KeyError, self.metadata.__setitem__, 'Xmp.%s.baz' % prefix2, 'foobaz')

