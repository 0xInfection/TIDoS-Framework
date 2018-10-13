API documentation
=================

pyexiv2
#######

.. module:: pyexiv2
.. autodata:: version_info
.. autodata:: __version__
.. autodata:: exiv2_version_info
.. autodata:: __exiv2_version__

pyexiv2.metadata
################

.. module:: pyexiv2.metadata
.. autoclass:: ImageMetadata
   :members: from_buffer, read, write, dimensions, mime_type,
             exif_keys, iptc_keys, iptc_charset, xmp_keys,
             __getitem__, __setitem__, __delitem__,
             comment, previews, copy, buffer

pyexiv2.exif
############

.. module:: pyexiv2.exif
.. autoexception:: ExifValueError
.. autoclass:: ExifTag
   :members: key, type, name, label, description, section_name,
             section_description, raw_value, value, human_value
.. autoclass:: ExifThumbnail
   :members: mime_type, extension, data, set_from_file, write_to_file, erase

pyexiv2.iptc
############

.. module:: pyexiv2.iptc
.. autoexception:: IptcValueError
.. autoclass:: IptcTag
   :members: key, type, name, title, description, photoshop_name, repeatable,
             record_name, record_description, raw_value, value

pyexiv2.xmp
###########

.. module:: pyexiv2.xmp
.. autofunction:: register_namespace
.. autofunction:: unregister_namespace
.. autofunction:: unregister_namespaces
.. autoexception:: XmpValueError
.. autoclass:: XmpTag
   :members: key, type, name, title, description, raw_value, value

pyexiv2.preview
###############

.. module:: pyexiv2.preview
.. autoclass:: Preview
   :members: mime_type, extension, size, dimensions, data, write_to_file

pyexiv2.utils
#############

.. module:: pyexiv2.utils
.. autofunction:: undefined_to_string
.. autofunction:: string_to_undefined
.. autofunction:: make_fraction

.. autoclass:: Rational
   :members: numerator, denominator, from_string, to_float, __eq__, __str__, __repr__
.. autoclass:: GPSCoordinate
   :members: degrees, minutes, seconds, direction, from_string, __eq__, __str__

