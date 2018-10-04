import os
from distutils.core import setup

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name='builtwith', 
    version='1.3.3',
    packages=['builtwith'],
    package_dir={'builtwith' : '.'}, # look for package contents in current directory
    author='Richard Penman',
    author_email='richard@webscraping.com',
    description='Detect the technology used by a website, such as Apache, JQuery, and Wordpress.',
    long_description=read('README.rst'),
    url='https://bitbucket.org/richardpenman/builtwith',
    license='lgpl',
    install_requires=['six'],
)
