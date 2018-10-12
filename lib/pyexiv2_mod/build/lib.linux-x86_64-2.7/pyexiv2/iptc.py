# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2006-2011 Olivier Tilloy <olivier@tilloy.net>
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

"""
IPTC specific code.
"""

import libexiv2python

from pyexiv2.utils import ListenerInterface, NotifyingList, \
                          FixedOffset, DateTimeFormatter

import time
import datetime
import re
import warnings


class IptcValueError(ValueError):

    """
    Exception raised when failing to parse the *value* of an IPTC tag.

    :attribute value: the value that fails to be parsed
    :type value: string
    :attribute type: the IPTC type of the tag
    :type type: string
    """

    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return 'Invalid value for IPTC type [%s]: [%s]' % \
               (self.type, self.value)


class IptcTag(ListenerInterface):

    """
    An IPTC tag.

    This tag can have several values (tags that have the *repeatable* property).

    Here is a correspondance table between the IPTC types and the possible
    python types the value of a tag may take:

    - Short: int
    - String: string
    - Date: :class:`datetime.date`
    - Time: :class:`datetime.time`
    - Undefined: string
    """

    # strptime is not flexible enough to handle all valid Time formats, we use a
    # custom regular expression
    _time_zone_re = r'(?P<sign>\+|-)(?P<ohours>\d{2}):(?P<ominutes>\d{2})'
    _time_re = re.compile(r'(?P<hours>\d{2}):(?P<minutes>\d{2}):(?P<seconds>\d{2})(?P<tzd>%s)' % _time_zone_re)

    def __init__(self, key, values=None, _tag=None):
        """
        The tag can be initialized with an optional list of values which
        expected type depends on the IPTC type of the tag.

        :param key: the key of the tag
        :type key: string
        :param values: the values of the tag
        """
        super(IptcTag, self).__init__()
        if _tag is not None:
            self._tag = _tag
        else:
            self._tag = libexiv2python._IptcTag(key)
        self._raw_values = None
        self._values = None
        self._values_cookie = False
        if values is not None:
            self._set_values(values)

    def _set_owner(self, metadata):
        self._tag._setParentImage(metadata._image)

    @staticmethod
    def _from_existing_tag(_tag):
        # Build a tag from an already existing libexiv2python._IptcTag
        tag = IptcTag(_tag._getKey(), _tag=_tag)
        # Do not set the raw_value property, as it would call
        # _tag._setRawValues
        # (see https://bugs.launchpad.net/pyexiv2/+bug/582445).
        tag._raw_values = _tag._getRawValues()
        tag._values_cookie = True
        return tag

    @property
    def key(self):
        """The key of the tag in the dotted form
        ``familyName.groupName.tagName`` where ``familyName`` = ``iptc``."""
        return self._tag._getKey()

    @property
    def type(self):
        """The IPTC type of the tag (one of Short, String, Date, Time,
        Undefined)."""
        return self._tag._getType()

    @property
    def name(self):
        """The name of the tag (this is also the third part of the key)."""
        return self._tag._getName()

    @property
    def title(self):
        """The title (label) of the tag."""
        return self._tag._getTitle()

    @property
    def description(self):
        """The description of the tag."""
        return self._tag._getDescription()

    @property
    def photoshop_name(self):
        """The Photoshop name of the tag."""
        return self._tag._getPhotoshopName()

    @property
    def repeatable(self):
        """Whether the tag is repeatable (accepts several values)."""
        return self._tag._isRepeatable()

    @property
    def record_name(self):
        """The name of the tag's record."""
        return self._tag._getRecordName()

    @property
    def record_description(self):
        """The description of the tag's record."""
        return self._tag._getRecordDescription()

    def _get_raw_values(self):
        return self._raw_values

    def _set_raw_values(self, values):
        if not isinstance(values, (list, tuple)):
            raise TypeError('Expecting a list of values')
        self._tag._setRawValues(values)
        self._raw_values = values
        self._values_cookie = True

    raw_value = property(fget=_get_raw_values, fset=_set_raw_values,
                         doc='The raw values of the tag as a list of strings.')

    def _get_raw_values_deprecated(self):
        msg = "The 'raw_values' property is deprecated, " \
              "use the 'raw_value' property instead."
        warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
        return self._get_raw_values()

    def _set_raw_values_deprecated(self, values):
        msg = "The 'raw_values' property is deprecated, " \
              "use the 'raw_value' property instead."
        warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
        return self._set_raw_values(values)

    raw_values = property(fget=_get_raw_values_deprecated,
                          fset=_set_raw_values_deprecated)

    def _compute_values(self):
        # Lazy computation of the values from the raw values
        self._values = \
            NotifyingList(map(self._convert_to_python, self._raw_values))
        self._values.register_listener(self)
        self._values_cookie = False

    def _get_values(self):
        if self._values_cookie:
            self._compute_values()
        return self._values

    def _set_values(self, values):
        if not isinstance(values, (list, tuple)):
            raise TypeError('Expecting a list of values')
        self.raw_value = map(self._convert_to_string, values)

        if isinstance(self._values, NotifyingList):
            self._values.unregister_listener(self)

        if isinstance(values, NotifyingList):
            # Already a notifying list
            self._values = values
        else:
            # Make the values a notifying list 
            self._values = NotifyingList(values)

        self._values.register_listener(self)
        self._values_cookie = False

    value = property(fget=_get_values, fset=_set_values,
                     doc='The values of the tag as a list of python objects.')

    def _get_values_deprecated(self):
        msg = "The 'values' property is deprecated, " \
              "use the 'value' property instead."
        warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
        return self._get_values()

    def _set_values_deprecated(self, values):
        msg = "The 'values' property is deprecated, " \
              "use the 'value' property instead."
        warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
        return self._set_values(values)

    values = property(fget=_get_values_deprecated, fset=_set_values_deprecated)

    def contents_changed(self):
        # Implementation of the ListenerInterface.
        # React on changes to the list of values of the tag.
        # The contents of self._values was changed.
        # The following is a quick, non optimal solution.
        self._set_values(self._values)

    def _convert_to_python(self, value):
        """
        Convert one raw value to its corresponding python type.

        :param value: the raw value to be converted
        :type value: string

        :return: the value converted to its corresponding python type

        :raise IptcValueError: if the conversion fails
        """
        if self.type == 'Short':
            try:
                return int(value)
            except ValueError:
                raise IptcValueError(value, self.type)

        elif self.type == 'String':
            # There is currently no charset conversion.
            # TODO: guess the encoding and decode accordingly into unicode
            # where relevant.
            return value

        elif self.type == 'Date':
            # According to the IPTC specification, the format for a string field
            # representing a date is '%Y%m%d'. However, the string returned by
            # exiv2 using method DateValue::toString() is formatted using
            # pattern '%Y-%m-%d'.
            format = '%Y-%m-%d'
            try:
                t = time.strptime(value, format)
                return datetime.date(*t[:3])
            except ValueError:
                raise IptcValueError(value, self.type)

        elif self.type == 'Time':
            # According to the IPTC specification, the format for a string field
            # representing a time is '%H%M%S±%H%M'. However, the string returned
            # by exiv2 using method TimeValue::toString() is formatted using
            # pattern '%H:%M:%S±%H:%M'.
            match = IptcTag._time_re.match(value)
            if match is None:
                raise IptcValueError(value, self.type)
            gd = match.groupdict()
            try:
                tzinfo = FixedOffset(gd['sign'], int(gd['ohours']),
                                     int(gd['ominutes']))
            except TypeError:
                raise IptcValueError(value, self.type)
            try:
                return datetime.time(int(gd['hours']), int(gd['minutes']),
                                     int(gd['seconds']), tzinfo=tzinfo)
            except (TypeError, ValueError):
                raise IptcValueError(value, self.type)

        elif self.type == 'Undefined':
            # Binary data, return it unmodified
            return value

        raise IptcValueError(value, self.type)

    def _convert_to_string(self, value):
        """
        Convert one value to its corresponding string representation, suitable
        to pass to libexiv2.

        :param value: the value to be converted

        :return: the value converted to its corresponding string representation
        :rtype: string

        :raise IptcValueError: if the conversion fails
        """
        if self.type == 'Short':
            if isinstance(value, int):
                return str(value)
            else:
                raise IptcValueError(value, self.type)

        elif self.type == 'String':
            if isinstance(value, unicode):
                try:
                    return value.encode('utf-8')
                except UnicodeEncodeError:
                    raise IptcValueError(value, self.type)
            elif isinstance(value, str):
                return value
            else:
                raise IptcValueError(value, self.type)

        elif self.type == 'Date':
            if isinstance(value, (datetime.date, datetime.datetime)):
                return DateTimeFormatter.iptc_date(value)
            else:
                raise IptcValueError(value, self.type)

        elif self.type == 'Time':
            if isinstance(value, (datetime.time, datetime.datetime)):
                return DateTimeFormatter.iptc_time(value)
            else:
                raise IptcValueError(value, self.type)

        elif self.type == 'Undefined':
            if isinstance(value, str):
                return value
            else:
                raise IptcValueError(value, self.type)

        raise IptcValueError(value, self.type)

    def __str__(self):
        """
        :return: a string representation of the IPTC tag for debugging purposes
        :rtype: string
        """
        left = '%s [%s]' % (self.key, self.type)
        if self._raw_values is None:
            right = '(No values)'
        else:
             right = self._raw_values
        return '<%s = %s>' % (left, right)

    # Support for pickling.
    def __getstate__(self):
        return (self.key, self.raw_value)

    def __setstate__(self, state):
        key, raw_value = state
        self._tag = libexiv2python._IptcTag(key)
        self.raw_value = raw_value

