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

from pyexiv2.metadata import ImageMetadata
from pyexiv2.exif import ExifTag
from pyexiv2.iptc import IptcTag
from pyexiv2.xmp import XmpTag
from pyexiv2.utils import FixedOffset, make_fraction

import datetime
import os
import tempfile
import time
import unittest
from testutils import EMPTY_JPG_DATA


class TestImageMetadata(unittest.TestCase):

    def setUp(self):
        # Create an empty image file
        fd, self.pathname = tempfile.mkstemp(suffix='.jpg')
        os.write(fd, EMPTY_JPG_DATA)
        os.close(fd)
        # Write some metadata
        m = ImageMetadata(self.pathname)
        m.read()
        m['Exif.Image.Make'] = 'EASTMAN KODAK COMPANY'
        m['Exif.Image.DateTime'] = datetime.datetime(2009, 2, 9, 13, 33, 20)
        m['Iptc.Application2.Caption'] = ['blabla']
        m['Iptc.Application2.DateCreated'] = [datetime.date(2004, 7, 13)]
        m['Xmp.dc.format'] = ('image', 'jpeg')
        m['Xmp.dc.subject'] = ['image', 'test', 'pyexiv2']
        m.comment = 'Hello World!'
        m.write()
        self.metadata = ImageMetadata(self.pathname)

    def tearDown(self):
        os.remove(self.pathname)

    ######################
    # Test general methods
    ######################

    def test_not_read_raises(self):
        # http://bugs.launchpad.net/pyexiv2/+bug/687373
        self.assertRaises(IOError, self.metadata.write)
        self.assertRaises(IOError, getattr, self.metadata, 'dimensions')
        self.assertRaises(IOError, getattr, self.metadata, 'mime_type')
        self.assertRaises(IOError, getattr, self.metadata, 'exif_keys')
        self.assertRaises(IOError, getattr, self.metadata, 'iptc_keys')
        self.assertRaises(IOError, getattr, self.metadata, 'xmp_keys')
        self.assertRaises(IOError, self.metadata._get_exif_tag, 'Exif.Image.Make')
        self.assertRaises(IOError, self.metadata._get_iptc_tag, 'Iptc.Application2.Caption')
        self.assertRaises(IOError, self.metadata._get_xmp_tag, 'Xmp.dc.format')
        self.assertRaises(IOError, self.metadata._set_exif_tag, 'Exif.Image.Make', 'foobar')
        self.assertRaises(IOError, self.metadata._set_iptc_tag, 'Iptc.Application2.Caption', ['foobar'])
        self.assertRaises(IOError, self.metadata._set_xmp_tag, 'Xmp.dc.format', ('foo', 'bar'))
        self.assertRaises(IOError, self.metadata._delete_exif_tag, 'Exif.Image.Make')
        self.assertRaises(IOError, self.metadata._delete_iptc_tag, 'Iptc.Application2.Caption')
        self.assertRaises(IOError, self.metadata._delete_xmp_tag, 'Xmp.dc.format')
        self.assertRaises(IOError, getattr, self.metadata, 'comment')
        self.assertRaises(IOError, setattr, self.metadata, 'comment', 'foobar')
        self.assertRaises(IOError, delattr, self.metadata, 'comment')
        self.assertRaises(IOError, getattr, self.metadata, 'previews')
        other = ImageMetadata(self.pathname)
        self.assertRaises(IOError, self.metadata.copy, other)
        self.assertRaises(IOError, getattr, self.metadata, 'buffer')
        thumb = self.metadata.exif_thumbnail
        self.assertRaises(IOError, getattr, thumb, 'mime_type')
        self.assertRaises(IOError, getattr, thumb, 'extension')
        self.assertRaises(IOError, thumb.write_to_file, '/tmp/foobar.jpg')
        self.assertRaises(IOError, thumb.erase)
        self.assertRaises(IOError, thumb.set_from_file, '/tmp/foobar.jpg')
        self.assertRaises(IOError, getattr, thumb, 'data')
        self.assertRaises(IOError, setattr, thumb, 'data', EMPTY_JPG_DATA)
        self.assertRaises(IOError, getattr, self.metadata, 'iptc_charset')

    def test_read(self):
        self.assertRaises(IOError, getattr, self.metadata, '_image')
        self.metadata.read()
        self.failIfEqual(self.metadata._image, None)

    def test_read_nonexistent_file(self):
        metadata = ImageMetadata('idontexist')
        self.failUnlessRaises(IOError, metadata.read)

    def test_write_preserve_timestamps(self):
        stat = os.stat(self.pathname)
        atime = round(stat.st_atime)
        mtime = round(stat.st_mtime)
        metadata = ImageMetadata(self.pathname)
        metadata.read()
        metadata.comment = 'Yellow Submarine'
        time.sleep(1.1)
        metadata.write(preserve_timestamps=True)
        stat2 = os.stat(self.pathname)
        atime2 = round(stat2.st_atime)
        mtime2 = round(stat2.st_mtime)
        self.failUnlessEqual(atime2, atime)
        self.failUnlessEqual(mtime2, mtime)

    def test_write_dont_preserve_timestamps(self):
        stat = os.stat(self.pathname)
        atime = round(stat.st_atime)
        mtime = round(stat.st_mtime)
        metadata = ImageMetadata(self.pathname)
        metadata.read()
        metadata.comment = 'Yellow Submarine'
        time.sleep(1.1)
        metadata.write()
        stat2 = os.stat(self.pathname)
        atime2 = round(stat2.st_atime)
        mtime2 = round(stat2.st_mtime)
        # It is not safe to assume that atime will have been modified when the
        # file has been read, as it may depend on mount options (e.g. noatime,
        # relatime).
        # See discussion at http://bugs.launchpad.net/pyexiv2/+bug/624999.
        #self.failIfEqual(atime2, atime)
        self.failIfEqual(mtime2, mtime)
        metadata.comment = 'Yesterday'
        time.sleep(1.1)
        metadata.write(preserve_timestamps=True)
        stat3 = os.stat(self.pathname)
        atime3 = round(stat3.st_atime)
        mtime3 = round(stat3.st_mtime)
        self.failUnlessEqual(atime3, atime2)
        self.failUnlessEqual(mtime3, mtime2)

    ###########################
    # Test EXIF-related methods
    ###########################

    def test_exif_keys(self):
        self.metadata.read()
        self.assertEqual(self.metadata._keys['exif'], None)
        keys = self.metadata.exif_keys
        self.assertEqual(len(keys), 2)
        self.assertEqual(self.metadata._keys['exif'], keys)

    def test_get_exif_tag(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['exif'], {})
        # Get an existing tag
        key = 'Exif.Image.Make'
        tag = self.metadata._get_exif_tag(key)
        self.assert_(isinstance(tag, ExifTag))
        self.assertEqual(self.metadata._tags['exif'][key], tag)
        # Try to get an nonexistent tag
        key = 'Exif.Photo.Sharpness'
        self.failUnlessRaises(KeyError, self.metadata._get_exif_tag, key)

    def test_set_exif_tag_wrong(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['exif'], {})
        # Try to set a tag with wrong type
        tag = 'Not an exif tag'
        self.failUnlessRaises(TypeError, self.metadata._set_exif_tag, tag)
        self.assertEqual(self.metadata._tags['exif'], {})

    def test_set_exif_tag_create(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['exif'], {})
        # Create a new tag
        tag = ExifTag('Exif.Thumbnail.Orientation', 1)
        self.assert_(tag.key not in self.metadata.exif_keys)
        self.metadata._set_exif_tag(tag.key, tag)
        self.assert_(tag.key in self.metadata.exif_keys)
        self.assertEqual(self.metadata._tags['exif'], {tag.key: tag})
        self.assert_(tag.key in self.metadata._image._exifKeys())
        self.assertEqual(self.metadata._image._getExifTag(tag.key)._getRawValue(),
                         tag.raw_value)

    def test_set_exif_tag_overwrite(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['exif'], {})
        # Overwrite an existing tag
        tag = ExifTag('Exif.Image.DateTime', datetime.datetime(2009, 3, 20, 20, 32, 0))
        self.metadata._set_exif_tag(tag.key, tag)
        self.assertEqual(self.metadata._tags['exif'], {tag.key: tag})
        self.assert_(tag.key in self.metadata._image._exifKeys())
        self.assertEqual(self.metadata._image._getExifTag(tag.key)._getRawValue(),
                         tag.raw_value)

    def test_set_exif_tag_overwrite_already_cached(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['exif'], {})
        # Overwrite an existing tag already cached
        key = 'Exif.Image.Make'
        tag = self.metadata._get_exif_tag(key)
        self.assertEqual(self.metadata._tags['exif'][key], tag)
        new_tag = ExifTag(key, 'World Company')
        self.metadata._set_exif_tag(key, new_tag)
        self.assertEqual(self.metadata._tags['exif'], {key: new_tag})
        self.assert_(key in self.metadata._image._exifKeys())
        self.assertEqual(self.metadata._image._getExifTag(key)._getRawValue(),
                         new_tag.raw_value)

    def test_set_exif_tag_direct_value_assignment(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['exif'], {})
        # Direct value assignment: pass a value instead of a fully-formed tag
        key = 'Exif.Thumbnail.Orientation'
        value = 1
        self.metadata._set_exif_tag(key, value)
        self.assert_(key in self.metadata.exif_keys)
        self.assert_(key in self.metadata._image._exifKeys())
        tag = self.metadata._get_exif_tag(key)
        self.assertEqual(tag.value, value)
        self.assertEqual(self.metadata._tags['exif'], {key: tag})
        self.assertEqual(self.metadata._image._getExifTag(key)._getRawValue(),
                         tag.raw_value)

    def test_delete_exif_tag_inexistent(self):
        self.metadata.read()
        key = 'Exif.Image.Artist'
        self.failUnlessRaises(KeyError, self.metadata._delete_exif_tag, key)

    def test_delete_exif_tag_not_cached(self):
        self.metadata.read()
        key = 'Exif.Image.DateTime'
        self.assertEqual(self.metadata._tags['exif'], {})
        self.assert_(key in self.metadata.exif_keys)
        self.metadata._delete_exif_tag(key)
        self.assertEqual(self.metadata._tags['exif'], {})
        self.failIf(key in self.metadata.exif_keys)

    def test_delete_exif_tag_cached(self):
        self.metadata.read()
        key = 'Exif.Image.DateTime'
        self.assert_(key in self.metadata.exif_keys)
        tag = self.metadata._get_exif_tag(key)
        self.assertEqual(self.metadata._tags['exif'][key], tag)
        self.metadata._delete_exif_tag(key)
        self.assertEqual(self.metadata._tags['exif'], {})
        self.failIf(key in self.metadata.exif_keys)

    ###########################
    # Test IPTC-related methods
    ###########################

    def test_iptc_keys(self):
        self.metadata.read()
        self.assertEqual(self.metadata._keys['iptc'], None)
        keys = self.metadata.iptc_keys
        self.assertEqual(len(keys), 2)
        self.assertEqual(self.metadata._keys['iptc'], keys)

    def test_get_iptc_tag(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['iptc'], {})
        # Get an existing tag
        key = 'Iptc.Application2.DateCreated'
        tag = self.metadata._get_iptc_tag(key)
        self.assert_(isinstance(tag, IptcTag))
        self.assertEqual(self.metadata._tags['iptc'][key], tag)
        # Try to get an nonexistent tag
        key = 'Iptc.Application2.Copyright'
        self.failUnlessRaises(KeyError, self.metadata._get_iptc_tag, key)

    def test_set_iptc_tag_wrong(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['iptc'], {})
        # Try to set a tag with wrong type
        tag = 'Not an iptc tag'
        self.failUnlessRaises(TypeError, self.metadata._set_iptc_tag, tag)
        self.assertEqual(self.metadata._tags['iptc'], {})

    def test_set_iptc_tag_create(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['iptc'], {})
        # Create a new tag
        tag = IptcTag('Iptc.Application2.Writer', ['Nobody'])
        self.assert_(tag.key not in self.metadata.iptc_keys)
        self.metadata._set_iptc_tag(tag.key, tag)
        self.assert_(tag.key in self.metadata.iptc_keys)
        self.assertEqual(self.metadata._tags['iptc'], {tag.key: tag})
        self.assert_(tag.key in self.metadata._image._iptcKeys())
        self.assertEqual(self.metadata._image._getIptcTag(tag.key)._getRawValues(),
                         tag.raw_value)

    def test_set_iptc_tag_overwrite(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['iptc'], {})
        # Overwrite an existing tag
        tag = IptcTag('Iptc.Application2.Caption', ['A picture.'])
        self.metadata._set_iptc_tag(tag.key, tag)
        self.assertEqual(self.metadata._tags['iptc'], {tag.key: tag})
        self.assert_(tag.key in self.metadata._image._iptcKeys())
        self.assertEqual(self.metadata._image._getIptcTag(tag.key)._getRawValues(),
                         tag.raw_value)

    def test_set_iptc_tag_overwrite_already_cached(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['iptc'], {})
        # Overwrite an existing tag already cached
        key = 'Iptc.Application2.Caption'
        tag = self.metadata._get_iptc_tag(key)
        self.assertEqual(self.metadata._tags['iptc'][key], tag)
        new_tag = IptcTag(key, ['A picture.'])
        self.metadata._set_iptc_tag(key, new_tag)
        self.assertEqual(self.metadata._tags['iptc'], {key: new_tag})
        self.assert_(key in self.metadata._image._iptcKeys())
        self.assertEqual(self.metadata._image._getIptcTag(key)._getRawValues(),
                         new_tag.raw_value)

    def test_set_iptc_tag_direct_value_assignment(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['iptc'], {})
        # Direct value assignment: pass a value instead of a fully-formed tag
        key = 'Iptc.Application2.Writer'
        values = ['Nobody']
        self.metadata._set_iptc_tag(key, values)
        self.assert_(key in self.metadata.iptc_keys)
        self.assert_(key in self.metadata._image._iptcKeys())
        tag = self.metadata._get_iptc_tag(key)
        self.assertEqual(tag.value, values)
        self.assertEqual(self.metadata._tags['iptc'], {key: tag})
        self.assertEqual(self.metadata._image._getIptcTag(key)._getRawValues(),
                         tag.raw_value)

    def test_delete_iptc_tag_inexistent(self):
        self.metadata.read()
        key = 'Iptc.Application2.LocationCode'
        self.failUnlessRaises(KeyError, self.metadata._delete_iptc_tag, key)

    def test_delete_iptc_tag_not_cached(self):
        self.metadata.read()
        key = 'Iptc.Application2.Caption'
        self.assertEqual(self.metadata._tags['iptc'], {})
        self.assert_(key in self.metadata.iptc_keys)
        self.metadata._delete_iptc_tag(key)
        self.assertEqual(self.metadata._tags['iptc'], {})
        self.failIf(key in self.metadata.iptc_keys)

    def test_delete_iptc_tag_cached(self):
        self.metadata.read()
        key = 'Iptc.Application2.Caption'
        self.assert_(key in self.metadata.iptc_keys)
        tag = self.metadata._get_iptc_tag(key)
        self.assertEqual(self.metadata._tags['iptc'][key], tag)
        self.metadata._delete_iptc_tag(key)
        self.assertEqual(self.metadata._tags['iptc'], {})
        self.failIf(key in self.metadata.iptc_keys)

    ##########################
    # Test XMP-related methods
    ##########################

    def test_xmp_keys(self):
        self.metadata.read()
        self.assertEqual(self.metadata._keys['xmp'], None)
        keys = self.metadata.xmp_keys
        self.assertEqual(len(keys), 2)
        self.assertEqual(self.metadata._keys['xmp'], keys)

    def test_get_xmp_tag(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['xmp'], {})
        # Get an existing tag
        key = 'Xmp.dc.subject'
        tag = self.metadata._get_xmp_tag(key)
        self.assert_(isinstance(tag, XmpTag))
        self.assertEqual(self.metadata._tags['xmp'][key], tag)
        # Try to get an nonexistent tag
        key = 'Xmp.xmp.Label'
        self.failUnlessRaises(KeyError, self.metadata._get_xmp_tag, key)

    def test_set_xmp_tag_wrong(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['xmp'], {})
        # Try to set a tag with wrong type
        tag = 'Not an xmp tag'
        self.failUnlessRaises(TypeError, self.metadata._set_xmp_tag, tag)
        self.assertEqual(self.metadata._tags['xmp'], {})

    def test_set_xmp_tag_create(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['xmp'], {})
        # Create a new tag
        tag = XmpTag('Xmp.dc.title', {'x-default': 'This is not a title',
                                      'fr-FR': "Ceci n'est pas un titre"})
        self.assert_(tag.key not in self.metadata.xmp_keys)
        self.metadata._set_xmp_tag(tag.key, tag)
        self.assert_(tag.key in self.metadata.xmp_keys)
        self.assertEqual(self.metadata._tags['xmp'], {tag.key: tag})
        self.assert_(tag.key in self.metadata._image._xmpKeys())
        self.assertEqual(self.metadata._image._getXmpTag(tag.key)._getLangAltValue(),
                         tag.raw_value)

    def test_set_xmp_tag_overwrite(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['xmp'], {})
        # Overwrite an existing tag
        tag = XmpTag('Xmp.dc.format', ('image', 'png'))
        self.metadata._set_xmp_tag(tag.key, tag)
        self.assertEqual(self.metadata._tags['xmp'], {tag.key: tag})
        self.assert_(tag.key in self.metadata._image._xmpKeys())
        self.assertEqual(self.metadata._image._getXmpTag(tag.key)._getTextValue(),
                         tag.raw_value)

    def test_set_xmp_tag_overwrite_already_cached(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['xmp'], {})
        # Overwrite an existing tag already cached
        key = 'Xmp.dc.subject'
        tag = self.metadata._get_xmp_tag(key)
        self.assertEqual(self.metadata._tags['xmp'][key], tag)
        new_tag = XmpTag(key, ['hello', 'world'])
        self.metadata._set_xmp_tag(key, new_tag)
        self.assertEqual(self.metadata._tags['xmp'], {key: new_tag})
        self.assert_(key in self.metadata._image._xmpKeys())
        self.assertEqual(self.metadata._image._getXmpTag(key)._getArrayValue(),
                         new_tag.raw_value)

    def test_set_xmp_tag_direct_value_assignment(self):
        self.metadata.read()
        self.assertEqual(self.metadata._tags['xmp'], {})
        # Direct value assignment: pass a value instead of a fully-formed tag
        key = 'Xmp.dc.title'
        value = {'x-default': 'This is not a title',
                 'fr-FR': "Ceci n'est pas un titre"}
        self.metadata._set_xmp_tag(key, value)
        self.assert_(key in self.metadata.xmp_keys)
        self.assert_(key in self.metadata._image._xmpKeys())
        tag = self.metadata._get_xmp_tag(key)
        self.assertEqual(tag.value, value)
        self.assertEqual(self.metadata._tags['xmp'], {key: tag})
        self.assertEqual(self.metadata._image._getXmpTag(key)._getLangAltValue(), tag.raw_value)

    def test_delete_xmp_tag_inexistent(self):
        self.metadata.read()
        key = 'Xmp.xmp.CreatorTool'
        self.failUnlessRaises(KeyError, self.metadata._delete_xmp_tag, key)

    def test_delete_xmp_tag_not_cached(self):
        self.metadata.read()
        key = 'Xmp.dc.subject'
        self.assertEqual(self.metadata._tags['xmp'], {})
        self.assert_(key in self.metadata.xmp_keys)
        self.metadata._delete_xmp_tag(key)
        self.assertEqual(self.metadata._tags['xmp'], {})
        self.failIf(key in self.metadata.xmp_keys)

    def test_delete_xmp_tag_cached(self):
        self.metadata.read()
        key = 'Xmp.dc.subject'
        self.assert_(key in self.metadata.xmp_keys)
        tag = self.metadata._get_xmp_tag(key)
        self.assertEqual(self.metadata._tags['xmp'][key], tag)
        self.metadata._delete_xmp_tag(key)
        self.assertEqual(self.metadata._tags['xmp'], {})
        self.failIf(key in self.metadata.xmp_keys)

    ###########################
    # Test dictionary interface
    ###########################

    def test_getitem(self):
        self.metadata.read()
        # Get existing tags
        key = 'Exif.Image.DateTime'
        tag = self.metadata[key]
        self.assert_(isinstance(tag, ExifTag))
        key = 'Iptc.Application2.Caption'
        tag = self.metadata[key]
        self.assert_(isinstance(tag, IptcTag))
        key = 'Xmp.dc.format'
        tag = self.metadata[key]
        self.assert_(isinstance(tag, XmpTag))
        # Try to get nonexistent tags
        keys = ('Exif.Image.SamplesPerPixel', 'Iptc.Application2.FixtureId',
                'Xmp.xmp.Rating', 'Wrong.Noluck.Raise')
        for key in keys:
            self.failUnlessRaises(KeyError, self.metadata.__getitem__, key)

    def test_setitem(self):
        self.metadata.read()
        # Set new tags
        key = 'Exif.Photo.ExposureBiasValue'
        tag = ExifTag(key, make_fraction(0, 3))
        self.metadata[key] = tag
        self.failUnless(key in self.metadata._tags['exif'])
        self.failUnlessEqual(self.metadata._tags['exif'][key], tag)
        key = 'Iptc.Application2.City'
        tag = IptcTag(key, ['Barcelona'])
        self.metadata[key] = tag
        self.failUnless(key in self.metadata._tags['iptc'])
        self.failUnlessEqual(self.metadata._tags['iptc'][key], tag)
        key = 'Xmp.dc.description'
        tag = XmpTag(key, {'x-default': 'Sunset picture.'})
        self.metadata[key] = tag
        self.failUnless(key in self.metadata._tags['xmp'])
        self.failUnlessEqual(self.metadata._tags['xmp'][key], tag)
        # Replace existing tags
        key = 'Exif.Photo.ExifVersion'
        tag = ExifTag(key, '0220')
        self.metadata[key] = tag
        self.failUnless(key in self.metadata._tags['exif'])
        self.failUnlessEqual(self.metadata._tags['exif'][key], tag)
        key = 'Iptc.Application2.Caption'
        tag = IptcTag(key, ['Sunset on Barcelona.'])
        self.metadata[key] = tag
        self.failUnless(key in self.metadata._tags['iptc'])
        self.failUnlessEqual(self.metadata._tags['iptc'][key], tag)
        key = 'Xmp.dc.subject'
        tag = XmpTag(key, ['sunset', 'Barcelona', 'beautiful', 'beach'])
        self.metadata[key] = tag
        self.failUnless(key in self.metadata._tags['xmp'])
        self.failUnlessEqual(self.metadata._tags['xmp'][key], tag)

    def test_delitem(self):
        self.metadata.read()
        # Delete existing tags
        key = 'Exif.Image.Make'
        del self.metadata[key]
        self.failIf(key in self.metadata._keys['exif'])
        self.failIf(key in self.metadata._tags['exif'])
        key = 'Iptc.Application2.Caption'
        del self.metadata[key]
        self.failIf(key in self.metadata._keys['iptc'])
        self.failIf(key in self.metadata._tags['iptc'])
        key = 'Xmp.dc.subject'
        del self.metadata[key]
        self.failIf(key in self.metadata._keys['xmp'])
        self.failIf(key in self.metadata._tags['xmp'])
        # Try to delete nonexistent tags
        keys = ('Exif.Image.SamplesPerPixel', 'Iptc.Application2.FixtureId',
                'Xmp.xmp.Rating', 'Wrong.Noluck.Raise')
        for key in keys:
            self.failUnlessRaises(KeyError, self.metadata.__delitem__, key)

    def test_replace_tag_by_itself(self):
        # Test that replacing an existing tag by itself
        # doesn’t result in an ugly segmentation fault
        # (see https://bugs.launchpad.net/pyexiv2/+bug/622739).
        self.metadata.read()
        keys = self.metadata.exif_keys + \
               self.metadata.iptc_keys + \
               self.metadata.xmp_keys
        for key in keys:
            self.metadata[key] = self.metadata[key]        

    def test_nonexistent_tag_family(self):
        self.metadata.read()
        key = 'Bleh.Image.DateTime'
        self.failUnlessRaises(KeyError, self.metadata.__getitem__, key)
        self.failUnlessRaises(KeyError, self.metadata.__setitem__, key, datetime.date.today())
        self.failUnlessRaises(KeyError, self.metadata.__delitem__, key)

    ##########################
    # Test the image comment #
    ##########################
    
    def test_get_comment(self):
        self.metadata.read()
        self.failUnlessEqual(self.metadata.comment, 'Hello World!')

    def test_set_comment(self):
        self.metadata.read()
        comment = 'Welcome to the real world.'
        self.metadata.comment = comment
        self.failUnlessEqual(self.metadata.comment, comment)
        self.metadata.comment = None
        self.failUnlessEqual(self.metadata.comment, '')

    def test_delete_comment(self):
        self.metadata.read()
        del self.metadata.comment
        self.failUnlessEqual(self.metadata.comment, '')

    ####################
    # Test metadata copy
    ####################

    def _set_up_other(self):
        self.other = ImageMetadata.from_buffer(EMPTY_JPG_DATA)

    def test_copy_metadata(self):
        self.metadata.read()
        self._set_up_other()
        self.other.read()
        families = ('exif', 'iptc', 'xmp')

        for family in families:
            self.failUnlessEqual(getattr(self.other, '%s_keys' % family), [])

        self.metadata.copy(self.other)

        for family in ('exif', 'iptc', 'xmp'):
            self.failUnlessEqual(self.other._keys[family], None)
            self.failUnlessEqual(self.other._tags[family], {})
            keys = getattr(self.metadata, '%s_keys' % family)
            self.failUnlessEqual(getattr(self.other._image, '_%sKeys' % family)(), keys)
            self.failUnlessEqual(getattr(self.other, '%s_keys' % family), keys)

        for key in self.metadata.exif_keys:
            self.failUnlessEqual(self.metadata[key].value, self.other[key].value)

        for key in self.metadata.iptc_keys:
            self.failUnlessEqual(self.metadata[key].value, self.other[key].value)

        for key in self.metadata.xmp_keys:
            self.failUnlessEqual(self.metadata[key].value, self.other[key].value)

        self.failUnlessEqual(self.metadata.comment, self.other.comment)

    #############################
    # Test MutableMapping methods
    #############################

    def _set_up_clean(self):
        self.clean = ImageMetadata.from_buffer(EMPTY_JPG_DATA)

    def test_mutablemapping(self):
        self._set_up_clean()
        self.clean.read()

        self.assertEqual(len(self.clean), 0)
        self.assertTrue('Exif.Image.DateTimeOriginal' not in self.clean)

        key = 'Exif.Image.DateTimeOriginal'
        correctDate = datetime.datetime(2007,03,11)
        incorrectDate = datetime.datetime(2009,03,25)
        tag_date = ExifTag(key,correctDate)
        false_tag_date = ExifTag(key,incorrectDate)
        self.clean[key] = tag_date

        self.assertEqual(len(self.clean), 1)
        self.assertTrue('Exif.Image.DateTimeOriginal' in self.clean)
        self.assertEqual(self.clean.get('Exif.Image.DateTimeOriginal', false_tag_date), tag_date)
        self.assertEqual(self.clean.get('Exif.Image.DateTime', tag_date), tag_date)

        key = 'Exif.Photo.UserComment'
        tag = ExifTag(key,'UserComment')
        self.clean[key] = tag        
        key = 'Iptc.Application2.Caption'
        tag = IptcTag(key,['Caption'])
        self.clean[key] = tag 
        key = 'Xmp.dc.subject'
        tag = XmpTag(key, ['subject', 'values'])
        self.clean[key] = tag

        self.assertTrue('Exif.Photo.UserComment' in self.clean)
        self.assertTrue('Iptc.Application2.Caption' in self.clean)
        self.assertTrue('Xmp.dc.subject' in self.clean)

        self.clean.clear()
        self.assertEqual(len(self.clean), 0)

        self.assertTrue('Exif.Photo.UserComment' not in self.clean)
        self.assertTrue('Iptc.Application2.Caption' not in self.clean)
        self.assertTrue('Xmp.dc.subject' not in self.clean)

    ###########################
    # Test the EXIF thumbnail #
    ###########################

    def _test_thumbnail_tags(self, there):
        keys = ('Exif.Thumbnail.Compression',
                'Exif.Thumbnail.JPEGInterchangeFormat',
                'Exif.Thumbnail.JPEGInterchangeFormatLength')
        for key in keys:
            self.assertEqual(key in self.metadata.exif_keys, there)

    def test_no_exif_thumbnail(self):
        self.metadata.read()
        thumb = self.metadata.exif_thumbnail
        self.assertEqual(thumb.mime_type, '')
        self.assertEqual(thumb.extension, '')
        self.assertEqual(thumb.data, '')
        self._test_thumbnail_tags(False)

    def test_set_exif_thumbnail_from_data(self):
        self.metadata.read()
        self._test_thumbnail_tags(False)
        thumb = self.metadata.exif_thumbnail
        thumb.data = EMPTY_JPG_DATA
        self.assertEqual(thumb.mime_type, 'image/jpeg')
        self.assertEqual(thumb.extension, '.jpg')
        self.assertEqual(thumb.data, EMPTY_JPG_DATA)
        self._test_thumbnail_tags(True)

    def test_set_exif_thumbnail_from_file(self):
        fd, pathname = tempfile.mkstemp(suffix='.jpg')
        os.write(fd, EMPTY_JPG_DATA)
        os.close(fd)
        self.metadata.read()
        self._test_thumbnail_tags(False)
        thumb = self.metadata.exif_thumbnail
        thumb.set_from_file(pathname)
        os.remove(pathname)
        self.assertEqual(thumb.mime_type, 'image/jpeg')
        self.assertEqual(thumb.extension, '.jpg')
        self.assertEqual(thumb.data, EMPTY_JPG_DATA)
        self._test_thumbnail_tags(True)

    def test_write_exif_thumbnail_to_file(self):
        self.metadata.read()
        self._test_thumbnail_tags(False)
        thumb = self.metadata.exif_thumbnail
        thumb.data = EMPTY_JPG_DATA
        fd, pathname = tempfile.mkstemp()
        os.close(fd)
        os.remove(pathname)
        thumb.write_to_file(pathname)
        pathname = pathname + thumb.extension
        fd = open(pathname, 'rb')
        self.assertEqual(fd.read(), EMPTY_JPG_DATA)
        fd.close()
        os.remove(pathname)

    def test_erase_exif_thumbnail(self):
        self.metadata.read()
        self._test_thumbnail_tags(False)
        thumb = self.metadata.exif_thumbnail
        thumb.data = EMPTY_JPG_DATA
        self.assertEqual(thumb.mime_type, 'image/jpeg')
        self.assertEqual(thumb.extension, '.jpg')
        self.assertEqual(thumb.data, EMPTY_JPG_DATA)
        self._test_thumbnail_tags(True)
        thumb.erase()
        self.assertEqual(thumb.mime_type, '')
        self.assertEqual(thumb.extension, '')
        self.assertEqual(thumb.data, '')
        self._test_thumbnail_tags(False)

    def test_set_exif_thumbnail_from_invalid_data(self):
        # No check on the format of the buffer is performed, therefore it will
        # always work.
        self.metadata.read()
        self._test_thumbnail_tags(False)
        thumb = self.metadata.exif_thumbnail
        thumb.data = 'invalid'
        self.assertEqual(thumb.mime_type, 'image/jpeg')
        self._test_thumbnail_tags(True)

    def test_set_exif_thumbnail_from_inexistent_file(self):
        self.metadata.read()
        self._test_thumbnail_tags(False)
        thumb = self.metadata.exif_thumbnail
        fd, pathname = tempfile.mkstemp()
        os.close(fd)
        os.remove(pathname)
        self.failUnlessRaises(IOError, thumb.set_from_file, pathname)
        self._test_thumbnail_tags(False)

    def test_exif_thumbnail_is_preview(self):
        self.metadata.read()
        self._test_thumbnail_tags(False)
        self.assertEqual(len(self.metadata.previews), 0)
        thumb = self.metadata.exif_thumbnail
        thumb.data = EMPTY_JPG_DATA
        self._test_thumbnail_tags(True)
        self.assertEqual(len(self.metadata.previews), 1)
        preview = self.metadata.previews[0]
        self.assertEqual(thumb.mime_type, preview.mime_type)
        self.assertEqual(thumb.extension, preview.extension)
        self.assertEqual(thumb.data, preview.data)

    #########################
    # Test the IPTC charset #
    #########################

    def test_guess_iptc_charset(self):
        # If no charset is defined, exiv2 guesses it from the encoding of the
        # metadata.
        self.metadata.read()
        self.assertEqual(self.metadata.iptc_charset, 'ascii')
        self.metadata['Iptc.Application2.City'] = [u'Córdoba']
        self.assertEqual(self.metadata.iptc_charset, 'utf-8')

    def test_set_iptc_charset_utf8(self):
        self.metadata.read()
        self.assert_('Iptc.Envelope.CharacterSet' not in self.metadata.iptc_keys)
        self.assertEqual(self.metadata.iptc_charset, 'ascii')
        values = ('utf-8', 'utf8', 'u8', 'utf', 'utf_8')
        for value in values:
            self.metadata.iptc_charset = value
            self.assertEqual(self.metadata.iptc_charset, 'utf-8')
            self.metadata.iptc_charset = value.upper()
            self.assertEqual(self.metadata.iptc_charset, 'utf-8')

    def test_set_invalid_iptc_charset(self):
        self.metadata.read()
        self.assert_('Iptc.Envelope.CharacterSet' not in self.metadata.iptc_keys)
        values = ('invalid', 'utf-9', '3.14')
        for value in values:
            self.assertRaises(ValueError, self.metadata.__setattr__,
                              'iptc_charset', value)

    def test_set_unhandled_iptc_charset(self):
        # At the moment, the only charset handled is UTF-8.
        self.metadata.read()
        self.assert_('Iptc.Envelope.CharacterSet' not in self.metadata.iptc_keys)
        values = ('ascii', 'iso8859_15', 'shift_jis')
        for value in values:
            self.assertRaises(ValueError, self.metadata.__setattr__,
                              'iptc_charset', value)

    def test_delete_iptc_charset(self):
        self.metadata.read()
        key = 'Iptc.Envelope.CharacterSet'

        self.assertEqual(self.metadata.iptc_charset, 'ascii')
        self.assert_(key not in self.metadata.iptc_keys)
        del self.metadata.iptc_charset
        self.assertEqual(self.metadata.iptc_charset, 'ascii')
        self.assert_(key not in self.metadata.iptc_keys)

        self.metadata.iptc_charset = 'utf-8'
        self.assertEqual(self.metadata.iptc_charset, 'utf-8')
        self.assert_(key in self.metadata.iptc_keys)
        del self.metadata.iptc_charset
        self.assertEqual(self.metadata.iptc_charset, 'ascii')
        self.assert_(key not in self.metadata.iptc_keys)

        self.metadata.iptc_charset = 'utf-8'
        self.assertEqual(self.metadata.iptc_charset, 'utf-8')
        self.assert_(key in self.metadata.iptc_keys)
        self.metadata.iptc_charset = None
        self.assertEqual(self.metadata.iptc_charset, 'ascii')
        self.assert_(key not in self.metadata.iptc_keys)

