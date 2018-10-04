#!/usr/bin/env python

# Copyright (c) 2009-2017, Mario Vilas
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from os import chdir
from os.path import abspath, join, split

# Make sure we are standing in the correct directory.
# Old versions of distutils didn't take care of this.
here = split(abspath(__file__))[0]
chdir(here)

# Package metadata.
metadata = dict(
    name='google',
    provides=['googlesearch'],
    requires=['beautifulsoup4'],
    packages=['googlesearch'],
    scripts=[join('scripts', 'google')],
    package_data={'googlesearch': ['user_agents.txt']},
    include_package_data=True,
    version="2.0.1",
    description="Python bindings to the Google search engine.",
    author="Mario Vilas",
    author_email="mvilas@gmail.com",
    url="http://breakingcode.wordpress.com/",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Environment :: Console",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)

# Prefer setuptools over the old distutils.
# If setuptools is available, use install_requires.
try:
    from setuptools import setup
    metadata['install_requires'] = metadata['requires']
except ImportError:
    from distutils.core import setup

# Get the long description from the readme file.
try:
    metadata['long_description'] = open(join(here, 'README.md'), 'rU').read()
except Exception:
    pass

# Run the setup script.
setup(**metadata)
