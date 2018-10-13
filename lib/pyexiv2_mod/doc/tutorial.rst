Tutorial
========

This tutorial is meant to give you a quick overview of what pyexiv2 allows you
to do. You can just read it through or follow it interactively, in which case
you will need to have pyexiv2 installed.
It doesn't cover all the possibilities offered by pyexiv2, only a basic subset
of them. For complete reference, see the :doc:`api`.

Let's get started!

First of all, we import the pyexiv2 module::

  >>> import pyexiv2

We then load an image file and read its metadata::

  >>> metadata = pyexiv2.ImageMetadata('test.jpg')
  >>> metadata.read()

Reading and writing EXIF tags
#############################

Let's retrieve a list of all the available EXIF tags available in the image::

  >>> metadata.exif_keys
  ['Exif.Image.ImageDescription',
   'Exif.Image.XResolution',
   'Exif.Image.YResolution',
   'Exif.Image.ResolutionUnit',
   'Exif.Image.Software',
   'Exif.Image.DateTime',
   'Exif.Image.Artist',
   'Exif.Image.Copyright',
   'Exif.Image.ExifTag',
   'Exif.Photo.Flash',
   'Exif.Photo.PixelXDimension',
   'Exif.Photo.PixelYDimension']

Each of those tags can be accessed with the ``[]`` operator on the metadata,
much like a python dictionary::

  >>> tag = metadata['Exif.Image.DateTime']

The value of an :class:`ExifTag` object can be accessed in two different ways:
with the :attr:`raw_value` and with the :attr:`value` attributes::

  >>> tag.raw_value
  '2004-07-13T21:23:44Z'

  >>> tag.value
  datetime.datetime(2004, 7, 13, 21, 23, 44)

The raw value is always a byte string, this is how the value is stored in the
file. The value is lazily computed from the raw value depending on the EXIF type
of the tag, and is represented as a convenient python object to allow easy
manipulation.

Note that querying the value of a tag may raise an :exc:`ExifValueError` if the
format of the raw value is invalid according to the EXIF specification (may
happen if it was written by other software that implements the specification in
a broken manner), or if pyexiv2 doesn't know how to convert it to a convenient
python object.

Accessing the value of a tag as a python object allows easy manipulation and
formatting::

  >>> tag.value.strftime('%A %d %B %Y, %H:%M:%S')
  'Tuesday 13 July 2004, 21:23:44'

Now let's modify the value of the tag and write it back to the file::

  >>> import datetime
  >>> tag.value = datetime.datetime.today()

  >>> metadata.write()

Similarly to reading the value of a tag, one can set either the
:attr:`raw_value` or the :attr:`value` (which will be automatically converted to
a correctly formatted byte string by pyexiv2).

You can also add new tags to the metadata by providing a valid key and value
pair (see exiv2's documentation for a list of valid
`EXIF tags <http://exiv2.org/tags.html>`_)::

  >>> key = 'Exif.Photo.UserComment'
  >>> value = 'This is a useful comment.'
  >>> metadata[key] = pyexiv2.ExifTag(key, value)

As a handy shortcut, you can always assign a value for a given key regardless
of whether it's already present in the metadata.
If a tag was present, its value is overwritten.
If the tag was not present, one is created and its value is set::

  >>> metadata[key] = value

The EXIF data may optionally embed a thumbnail in the JPEG or TIFF format.
The thumbnail can be accessed, set from a JPEG file or buffer, saved to disk and
erased::

  >>> thumb = metadata.exif_thumbnail
  >>> thumb.set_from_file('/tmp/thumbnail.jpg')
  >>> thumb.write_to_file('/tmp/copy')
  >>> thumb.erase()
  >>> metadata.write()


Reading and writing IPTC tags
#############################

Reading and writing IPTC tags works pretty much the same way as with EXIF tags.
Let's retrieve the list of all available IPTC tags in the image::

  >>> metadata.iptc_keys
  ['Iptc.Application2.Caption',
   'Iptc.Application2.Writer',
   'Iptc.Application2.Byline',
   'Iptc.Application2.ObjectName',
   'Iptc.Application2.DateCreated',
   'Iptc.Application2.City',
   'Iptc.Application2.ProvinceState',
   'Iptc.Application2.CountryName',
   'Iptc.Application2.Category',
   'Iptc.Application2.Keywords',
   'Iptc.Application2.Copyright']

Each of those tags can be accessed with the ``[]`` operator on the metadata::

  >>> tag = metadata['Iptc.Application2.DateCreated']

An IPTC tag always has a list of values rather than a single value.
This is because some tags have a repeatable character.
Tags that are not repeatable only hold one value in their list of values.

Check the :attr:`repeatable` attribute to know whether a tag can hold more than
one value::

  >>> tag.repeatable
  False

As with EXIF tags, the values of an :class:`IptcTag` object can be accessed in
two different ways: with the :attr:`raw_value` and with the :attr:`value`
attributes::

  >>> tag.raw_value
  ['2004-07-13']

  >>> tag.value
  [datetime.date(2004, 7, 13)]

Note that querying the values of a tag may raise an :exc:`IptcValueError` if the
format of the raw values is invalid according to the IPTC specification (may
happen if it was written by other software that implements the specification in
a broken manner), or if pyexiv2 doesn't know how to convert it to a convenient
python object.

Now let's modify the values of the tag and write it back to the file::

  >>> tag.value = [datetime.date.today()]

  >>> metadata.write()

Similarly to reading the values of a tag, one can set either the
:attr:`raw_value` or the :attr:`value` (which will be automatically converted
to correctly formatted byte strings by pyexiv2).

You can also add new tags to the metadata by providing a valid key and values
pair (see exiv2's documentation for a list of valid
`IPTC tags <http://exiv2.org/iptc.html>`_)::

  >>> key = 'Iptc.Application2.Contact'
  >>> values = ['John', 'Paul', 'Ringo', 'George']
  >>> metadata[key] = pyexiv2.IptcTag(key, values)

As a handy shortcut, you can always assign values for a given key regardless
of whether it's already present in the metadata.
If a tag was present, its values are overwritten.
If the tag was not present, one is created and its values are set::

  >>> metadata[key] = values

The IPTC metadata in an image may embed an optional character set for its
encoding. This is defined by the ``Iptc.Envelope.CharacterSet`` tag.
The :class:`ImageMetadata` class has an :attr:`iptc_charset` property that
allows to easily get, set and delete this value::

  >>> metadata.iptc_charset
  'ascii'

  >>> metadata.iptc_charset = 'utf-8'

  >>> del metadata.iptc_charset

Note that at the moment, the only supported charset that can be assigned to the
property is ``utf-8``.
Also note that even if the charset is not explicitly set, its value may be
inferred from the contents of the image. If not, it will be ``None``.

Reading and writing XMP tags
############################

Reading and writing XMP tags works pretty much the same way as with EXIF tags.
Let's retrieve the list of all available XMP tags in the image::

  >>> metadata.xmp_keys
  ['Xmp.dc.creator',
   'Xmp.dc.description',
   'Xmp.dc.rights',
   'Xmp.dc.source',
   'Xmp.dc.subject',
   'Xmp.dc.title',
   'Xmp.xmp.CreateDate',
   'Xmp.xmp.ModifyDate']

Each of those tags can be accessed with the ``[]`` operator on the metadata::

  >>> tag = metadata['Xmp.xmp.ModifyDate']

As with EXIF tags, the value of an :class:`XmpTag` object can be accessed in
two different ways: with the :attr:`raw_value` and with the :attr:`value`
attributes::

  >>> tag.raw_value
  '2002-07-19T13:28:10'

  >>> tag.value
  datetime.datetime(2002, 7, 19, 13, 28, 10)

Note that querying the value of a tag may raise an :exc:`XmpValueError` if the
format of the raw value is invalid according to the XMP specification (may
happen if it was written by other software that implements the specification in
a broken manner), or if pyexiv2 doesn't know how to convert it to a convenient
python object.

Now let's modify the value of the tag and write it back to the file::

  >>> tag.value = datetime.datetime.today()

  >>> metadata.write()

Similarly to reading the value of a tag, one can set either the
:attr:`raw_value` or the :attr:`value` (which will be automatically converted to
a correctly formatted byte string by pyexiv2).

You can also add new tags to the metadata by providing a valid key and value
pair (see exiv2's documentation for a list of valid
`XMP tags <http://exiv2.org/tags-xmp-dc.html>`_)::

  >>> key = 'Xmp.xmp.Label'
  >>> value = 'A beautiful picture.'
  >>> metadata[key] = pyexiv2.XmpTag(key, value)

As a handy shortcut, you can always assign a value for a given key regardless
of whether it's already present in the metadata.
If a tag was present, its value is overwritten.
If the tag was not present, one is created and its value is set::

  >>> metadata[key] = value

If you need to write custom metadata, you can register a custom XMP namespace::

  >>> pyexiv2.xmp.register_namespace('http://example.org/foo/', 'foo')
  >>> metadata['Xmp.foo.bar'] = 'baz'

Note that a limitation of the current implementation is that only simple text
values can be written to tags in a custom namespace.

A custom namespace can be unregistered. This has the effect of invalidating all
tags in this namespace for images that have not been written back yet::

  >>> pyexiv2.xmp.unregister_namespace('http://example.org/foo/')

Accessing embedded previews
###########################

Images may embed previews (also called thumbnails) of various sizes in their
metadata. pyexiv2 allows to easily access them::

  >>> previews = metadata.previews

  >>> len(previews)
  2

They are sorted by increasing size. Let's play with the largest one::

  >>> largest = previews[-1]

  >>> largest.dimensions
  (320, 240)

  >>> largest.mime_type
  'image/jpeg'

  >>> largest.write_to_file('largest')

