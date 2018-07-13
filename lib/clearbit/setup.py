import os
import sys
import warnings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = []
install_requires.append('requests >= 0.8.8')

# Don't import clearbit module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'clearbit'))
from version import VERSION

# Get simplejson if we don't already have json
if sys.version_info < (3, 0):
    try:
        from util import json
    except ImportError:
        install_requires.append('simplejson')

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='clearbit',
    cmdclass={'build_py': build_py},
    version=VERSION,
    description='Clearbit python bindings',
    long_description=read('README.rst'),
    author='Clearbit',
    author_email='support@clearbit.com',
    url='https://clearbit.com',
    packages=['clearbit', 'clearbit.enrichment'],
    package_data={'clearbit': ['../VERSION']},
    install_requires=install_requires,
    use_2to3=True,
    include_package_data=True,
    test_suite='tests',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])
