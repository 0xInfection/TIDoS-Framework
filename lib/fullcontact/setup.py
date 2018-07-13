"""
FullContact.py
--------------

Simple Python interface for FullContact, using Requests.

"""
from setuptools import setup


setup(
    name='FullContact.py',
    version='0.0.6',
    url='https://github.com/fullcontact/fullcontact.py',
    license='MIT',
    author=['FullContact'],
    author_email=['support@fullcontact.com'],
    description='Simple Python interface for FullContact, using Requests',
    long_description='Simple Python interface for FullContact, using Requests',
    packages=['fullcontact'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'requests',
    ],
    include_package_data=True,
    tests_require=[
        'nose>=1.0',
        'flake8<=2.6.2'  # Last version of flake8 to support Python 2.6
    ],
    test_suite='nose.collector',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
