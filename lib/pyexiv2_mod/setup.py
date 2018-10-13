from setuptools import setup, find_packages, Extension

version = "0.3.2"

setup(
    name="pyexiv2",
    version=version,
    url='http://tilloy.net/dev/pyexiv2/',
    author='Olivier Tilloy',
    author_email='olivier@tilloy.net',
    description='A python binding to exiv2, the C++ library for manipulation '
                'of EXIF, IPTC and XMP image metadata.',
    long_description=open('README').read(),
    license='GNU GPL v2',
    download_url=('https://launchpad.net/pyexiv2/0.3.x/{version}/+download/'
                  'pyexiv2-{version}.tar.bz2').format(version=version),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    ext_modules=[
        Extension('libexiv2python',
                  ['src/exiv2wrapper.cpp', 'src/exiv2wrapper_python.cpp'],
                  libraries=['boost_python', 'exiv2']),
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: C++',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
