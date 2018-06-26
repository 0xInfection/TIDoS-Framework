import os
from setuptools import setup, find_packages

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
    readme = ''

version = '0.9'

exec_dirs = [
    'src/tld/bin/',
]
execs = []
for exec_dir in exec_dirs:
    execs += [os.path.join(exec_dir, f) for f in os.listdir(exec_dir)]

setup(
    name='tld',
    version=version,
    description="Extract the top level domain (TLD) from the URL given.",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet",
        "License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or "
        "later (LGPLv2+)",
    ],
    keywords='tld, top level domain names, python',
    author='Artur Barseghyan',
    author_email='artur.barseghyan@gmail.com',
    url='https://github.com/barseghyanartur/tld',
    package_dir={'': 'src'},
    packages=find_packages(where='./src'),
    package_data={'tld': execs},
    scripts=['src/tld/bin/update-tld-names',],
    include_package_data=True,
    license='MPL 1.1/GPL 2.0/LGPL 2.1',
    install_requires=[
        'six>=1.9'
    ],
    test_suite='src/tld/tests.py',
)
