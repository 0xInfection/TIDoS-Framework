#!/bin/sh

# Copyright (C) 2010-2011 Olivier Tilloy <olivier@tilloy.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

###############################################################################
# This script retrieves all the dependencies required and cross-compiles
# pyexiv2 for windows on a linux host.
#
# Typical dependencies (of this script) on an Ubuntu system:
#  wget unzip tar build-essential mingw32 p7zip-full
#
# After execution is complete, copy the following file and folder to the
# site-packages directory of a Python 2.7 windows setup:
#  - $BASE/pyexiv2/build/libexiv2python.pyd
#  - $BASE/pyexiv2/src/pyexiv2
#
###############################################################################

# Determine the absolute path of the pyexiv2 branch
# (this is where this script is located)
cd $(dirname $0) && BRANCH="$PWD" && cd -

# Where to retrieve and compile dependencies
BASE=$HOME/dev/win32
mkdir -p $BASE
cd $BASE

PLATFORM=i586-mingw32msvc
COMPILER=$PLATFORM-g++
ARCHIVER=$PLATFORM-ar
BUILD=i586-linux

# zlib (for exiv2)
wget --trust-server-names=on http://gnuwin32.sourceforge.net/downlinks/zlib-lib-zip.php
unzip -d zlib zlib-*.zip

# iconv (for exiv2)
wget http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.14.tar.gz
tar xf libiconv-1.14.tar.gz
cd libiconv-1.14
./configure --enable-static --disable-visibility --target=$PLATFORM --host=$PLATFORM --build=$BUILD --prefix=$BASE/libiconv
make -j3 install
cd ..

# expat (for exiv2)
wget --trust-server-names=on http://sourceforge.net/projects/expat/files/expat/2.0.1/expat-2.0.1.tar.gz/download
tar xf expat-2.0.1.tar.gz
cd expat-2.0.1
./configure --disable-shared --disable-visibility --target=$PLATFORM --host=$PLATFORM --build=$BUILD --prefix=$BASE/expat
make -j3 install
cd ..

# exiv2
wget http://www.exiv2.org/exiv2-0.22.tar.gz
tar xf exiv2-0.22.tar.gz
cd exiv2-0.22
./configure --disable-shared --disable-visibility --target=$PLATFORM --host=$PLATFORM --build=$BUILD --disable-nls --with-zlib=$BASE/zlib --with-libiconv-prefix=$BASE/libiconv --with-expat=$BASE/expat --prefix=$BASE/exiv2
make -j3 install
cd ..

# python
wget http://python.org/ftp/python/2.7.2/python-2.7.2.msi
7z x python-2.7.2.msi -opython
7z x python/python -opython

# boost-python
wget --trust-server-names=on http://sourceforge.net/projects/boost/files/boost/1.47.0/boost_1_47_0.tar.bz2/download
tar xf boost_1_47_0.tar.bz2
cd boost_1_47_0
echo "using gcc : : $COMPILER : <compileflags>-I$BASE/python <archiver>$ARCHIVER ;" >> tools/build/v2/user-config.jam
./bootstrap.sh
./bjam install -j 3 --prefix=$BASE/boost --with-python toolset=gcc link=static
cd ..

# pyexiv2
cd $BRANCH
mkdir -p build
$COMPILER -o build/libexiv2python.pyd -DBOOST_PYTHON_STATIC_LIB -shared src/exiv2wrapper.cpp src/exiv2wrapper_python.cpp $BASE/exiv2/lib/libexiv2.a $BASE/zlib/lib/libz.a $BASE/libiconv/lib/libiconv.a $BASE/expat/lib/libexpat.a $BASE/boost/lib/libboost_python.a -I$BASE/exiv2/include -I$BASE/python -I$BASE/boost/include -L$BASE/python -lpython27

