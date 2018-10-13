// *****************************************************************************
/*
 * Copyright (C) 2006-2010 Olivier Tilloy <olivier@tilloy.net>
 *
 * This file is part of the pyexiv2 distribution.
 *
 * pyexiv2 is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * pyexiv2 is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with pyexiv2; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, 5th Floor, Boston, MA 02110-1301 USA.
 */
/*
  Author: Olivier Tilloy <olivier@tilloy.net>
 */
// *****************************************************************************

#ifndef __exiv2wrapper__
#define __exiv2wrapper__

#include <string>

#include "exiv2/image.hpp"
#include "exiv2/preview.hpp"

#include "boost/python.hpp"

namespace exiv2wrapper
{

class Image;

class ExifTag
{
public:
    // Constructor
    ExifTag(const std::string& key,
            Exiv2::Exifdatum* datum=0, Exiv2::ExifData* data=0,
            Exiv2::ByteOrder byteOrder=Exiv2::invalidByteOrder);

    ~ExifTag();

    void setRawValue(const std::string& value);
    void setParentImage(Image& image);

    const std::string getKey();
    const std::string getType();
    const std::string getName();
    const std::string getLabel();
    const std::string getDescription();
    const std::string getSectionName();
    const std::string getSectionDescription();
    const std::string getRawValue();
    const std::string getHumanValue();
    int getByteOrder();

private:
    Exiv2::ExifKey _key;
    Exiv2::Exifdatum* _datum;
    Exiv2::ExifData* _data;
    std::string _type;
    std::string _name;
    std::string _label;
    std::string _description;
    std::string _sectionName;
    std::string _sectionDescription;
    int _byteOrder;
};


class IptcTag
{
public:
    // Constructor
    IptcTag(const std::string& key, Exiv2::IptcData* data=0);

    ~IptcTag();

    void setRawValues(const boost::python::list& values);
    void setParentImage(Image& image);

    const std::string getKey();
    const std::string getType();
    const std::string getName();
    const std::string getTitle();
    const std::string getDescription();
    const std::string getPhotoshopName();
    const bool isRepeatable();
    const std::string getRecordName();
    const std::string getRecordDescription();
    const boost::python::list getRawValues();

private:
    Exiv2::IptcKey _key;
    bool _from_data; // whether the tag is built from an existing IptcData
    Exiv2::IptcData* _data;
    std::string _type;
    std::string _name;
    std::string _title;
    std::string _description;
    std::string _photoshopName;
    bool _repeatable;
    std::string _recordName;
    std::string _recordDescription;
};


class XmpTag
{
public:
    // Constructor
    XmpTag(const std::string& key, Exiv2::Xmpdatum* datum=0);

    ~XmpTag();

    void setTextValue(const std::string& value);
    void setArrayValue(const boost::python::list& values);
    void setLangAltValue(const boost::python::dict& values);
    void setParentImage(Image& image);

    const std::string getKey();
    const std::string getExiv2Type();
    const std::string getType();
    const std::string getName();
    const std::string getTitle();
    const std::string getDescription();
    const std::string getTextValue();
    const boost::python::list getArrayValue();
    const boost::python::dict getLangAltValue();

private:
    Exiv2::XmpKey _key;
    bool _from_datum; // whether the tag is built from an existing Xmpdatum
    Exiv2::Xmpdatum* _datum;
    std::string _exiv2_type;
    std::string _type;
    std::string _name;
    std::string _title;
    std::string _description;
};


class Preview
{
public:
    Preview(const Exiv2::PreviewImage& previewImage);

    void writeToFile(const std::string& path) const;

    std::string _mimeType;
    std::string _extension;
    unsigned int _size;
    boost::python::tuple _dimensions;
    std::string _data;
};


class Image
{
public:
    // Constructors
    Image(const std::string& filename);
    Image(const std::string& buffer, unsigned long size);
    Image(const Image& image);

    ~Image();

    void readMetadata();
    void writeMetadata();

    // Read-only access to the dimensions of the picture.
    unsigned int pixelWidth() const;
    unsigned int pixelHeight() const;

    // Read-only access to the MIME type of the image.
    std::string mimeType() const;

    // Read and write access to the EXIF tags.
    // For a complete list of the available EXIF tags, see
    // libexiv2's documentation (http://exiv2.org/tags.html).

    // Return a list of all the keys of available EXIF tags set in the
    // image.
    boost::python::list exifKeys();

    // Return the required EXIF tag.
    // Throw an exception if the tag is not set.
    const ExifTag getExifTag(std::string key);

    // Delete the required EXIF tag.
    // Throw an exception if the tag was not set.
    void deleteExifTag(std::string key);

    // Read and write access to the IPTC tags.
    // For a complete list of the available IPTC tags, see
    // libexiv2's documentation (http://exiv2.org/iptc.html).

    // Returns a list of all the keys of available IPTC tags set in the
    // image. This list has no duplicates: each of its items is unique,
    // even if a tag is present more than once.
    boost::python::list iptcKeys();

    // Return the required IPTC tag.
    // Throw an exception if the tag is not set.
    const IptcTag getIptcTag(std::string key);

    // Delete (all the repetitions of) the required IPTC tag.
    // Throw an exception if the tag was not set.
    void deleteIptcTag(std::string key);

    boost::python::list xmpKeys();

    // Return the required XMP tag.
    // Throw an exception if the tag is not set.
    const XmpTag getXmpTag(std::string key);

    // Delete the required XMP tag.
    // Throw an exception if the tag was not set.
    void deleteXmpTag(std::string key);

    // Comment
    const std::string getComment() const;
    void setComment(const std::string& comment);
    void clearComment();

    // Read access to the thumbnail embedded in the image.
    boost::python::list previews();

    // Manipulate the JPEG/TIFF thumbnail embedded in the EXIF data.
    const std::string getExifThumbnailMimeType();
    const std::string getExifThumbnailExtension();
    void writeExifThumbnailToFile(const std::string& path);
    const std::string getExifThumbnailData();
    void eraseExifThumbnail();
    void setExifThumbnailFromFile(const std::string& path);
    void setExifThumbnailFromData(const std::string& data);

    // Copy the metadata to another image.
    void copyMetadata(Image& other, bool exif=true, bool iptc=true, bool xmp=true) const;

    // Return the image data buffer.
    std::string getDataBuffer() const;

    // Accessors
    Exiv2::ExifData* getExifData() { return _exifData; };
    Exiv2::IptcData* getIptcData() { return _iptcData; };
    Exiv2::XmpData* getXmpData() { return _xmpData; };

    Exiv2::ByteOrder getByteOrder() const;

    const std::string getIptcCharset() const;

private:
    std::string _filename;
    Exiv2::byte* _data;
    long _size;
    Exiv2::Image::AutoPtr _image;
    Exiv2::ExifData* _exifData;
    Exiv2::IptcData* _iptcData;
    Exiv2::XmpData* _xmpData;
    Exiv2::ExifThumb* _exifThumbnail;
    Exiv2::ExifThumb* _getExifThumbnail();

    // true if the image's internal metadata has already been read,
    // false otherwise
    bool _dataRead;

    void _instantiate_image();
};


// Translate an Exiv2 generic exception into a Python exception
void translateExiv2Error(Exiv2::Error const& error);


// Functions to manipulate custom XMP namespaces
void registerXmpNs(const std::string& name, const std::string& prefix);
void unregisterXmpNs(const std::string& name);
void unregisterAllXmpNs();

} // End of namespace exiv2wrapper

#endif

