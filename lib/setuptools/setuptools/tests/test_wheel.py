# -*- coding: utf-8 -*-

"""wheel tests
"""

from distutils.sysconfig import get_config_var
from distutils.util import get_platform
import contextlib
import glob
import inspect
import os
import shutil
import subprocess
import sys
import zipfile

import pytest

from pkg_resources import Distribution, PathMetadata, PY_MAJOR
from setuptools.extern.packaging.utils import canonicalize_name
from setuptools.wheel import Wheel

from .contexts import tempdir
from .files import build_files
from .textwrap import DALS


WHEEL_INFO_TESTS = (
    ('invalid.whl', ValueError),
    ('simplewheel-2.0-1-py2.py3-none-any.whl', {
        'project_name': 'simplewheel',
        'version': '2.0',
        'build': '1',
        'py_version': 'py2.py3',
        'abi': 'none',
        'platform': 'any',
    }),
    ('simple.dist-0.1-py2.py3-none-any.whl', {
        'project_name': 'simple.dist',
        'version': '0.1',
        'build': None,
        'py_version': 'py2.py3',
        'abi': 'none',
        'platform': 'any',
    }),
    ('example_pkg_a-1-py3-none-any.whl', {
        'project_name': 'example_pkg_a',
        'version': '1',
        'build': None,
        'py_version': 'py3',
        'abi': 'none',
        'platform': 'any',
    }),
    ('PyQt5-5.9-5.9.1-cp35.cp36.cp37-abi3-manylinux1_x86_64.whl', {
        'project_name': 'PyQt5',
        'version': '5.9',
        'build': '5.9.1',
        'py_version': 'cp35.cp36.cp37',
        'abi': 'abi3',
        'platform': 'manylinux1_x86_64',
    }),
)

@pytest.mark.parametrize(
    ('filename', 'info'), WHEEL_INFO_TESTS,
    ids=[t[0] for t in WHEEL_INFO_TESTS]
)
def test_wheel_info(filename, info):
    if inspect.isclass(info):
        with pytest.raises(info):
            Wheel(filename)
        return
    w = Wheel(filename)
    assert {k: getattr(w, k) for k in info.keys()} == info


@contextlib.contextmanager
def build_wheel(extra_file_defs=None, **kwargs):
    file_defs = {
        'setup.py': (DALS(
            '''
            # -*- coding: utf-8 -*-
            from setuptools import setup
            import setuptools
            setup(**%r)
            '''
        ) % kwargs).encode('utf-8'),
    }
    if extra_file_defs:
        file_defs.update(extra_file_defs)
    with tempdir() as source_dir:
        build_files(file_defs, source_dir)
        subprocess.check_call((sys.executable, 'setup.py',
                               '-q', 'bdist_wheel'), cwd=source_dir)
        yield glob.glob(os.path.join(source_dir, 'dist', '*.whl'))[0]


def tree_set(root):
    contents = set()
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            contents.add(os.path.join(os.path.relpath(dirpath, root),
                                      filename))
    return contents


def flatten_tree(tree):
    """Flatten nested dicts and lists into a full list of paths"""
    output = set()
    for node, contents in tree.items():
        if isinstance(contents, dict):
            contents = flatten_tree(contents)

        for elem in contents:
            if isinstance(elem, dict):
                output |= {os.path.join(node, val)
                           for val in flatten_tree(elem)}
            else:
                output.add(os.path.join(node, elem))
    return output


def format_install_tree(tree):
    return {x.format(
        py_version=PY_MAJOR,
        platform=get_platform(),
        shlib_ext=get_config_var('EXT_SUFFIX') or get_config_var('SO'))
            for x in tree}


def _check_wheel_install(filename, install_dir, install_tree_includes,
                         project_name, version, requires_txt):
    w = Wheel(filename)
    egg_path = os.path.join(install_dir, w.egg_name())
    w.install_as_egg(egg_path)
    if install_tree_includes is not None:
        install_tree = format_install_tree(install_tree_includes)
        exp = tree_set(install_dir)
        assert install_tree.issubset(exp), (install_tree - exp)

    metadata = PathMetadata(egg_path, os.path.join(egg_path, 'EGG-INFO'))
    dist = Distribution.from_filename(egg_path, metadata=metadata)
    assert dist.project_name == project_name
    assert dist.version == version
    if requires_txt is None:
        assert not dist.has_metadata('requires.txt')
    else:
        assert requires_txt == dist.get_metadata('requires.txt').lstrip()


class Record(object):

    def __init__(self, id, **kwargs):
        self._id = id
        self._fields = kwargs

    def __repr__(self):
        return '%s(**%r)' % (self._id, self._fields)


WHEEL_INSTALL_TESTS = (

    dict(
        id='basic',
        file_defs={
            'foo': {
                '__init__.py': ''
            }
        },
        setup_kwargs=dict(
            packages=['foo'],
        ),
        install_tree=flatten_tree({
            'foo-1.0-py{py_version}.egg': {
                'EGG-INFO': [
                    'PKG-INFO',
                    'RECORD',
                    'WHEEL',
                    'top_level.txt'
                ],
                'foo': ['__init__.py']
            }
        }),
    ),

    dict(
        id='utf-8',
        setup_kwargs=dict(
            description='Description accentuée',
        )
    ),

    dict(
        id='data',
        file_defs={
            'data.txt': DALS(
                '''
                Some data...
                '''
            ),
        },
        setup_kwargs=dict(
            data_files=[('data_dir', ['data.txt'])],
        ),
        install_tree=flatten_tree({
            'foo-1.0-py{py_version}.egg': {
                'EGG-INFO': [
                    'PKG-INFO',
                    'RECORD',
                    'WHEEL',
                    'top_level.txt'
                ],
                'data_dir': [
                    'data.txt'
                ]
            }
        }),
    ),

    dict(
        id='extension',
        file_defs={
            'extension.c': DALS(
                '''
                #include "Python.h"

                #if PY_MAJOR_VERSION >= 3

                static struct PyModuleDef moduledef = {
                        PyModuleDef_HEAD_INIT,
                        "extension",
                        NULL,
                        0,
                        NULL,
                        NULL,
                        NULL,
                        NULL,
                        NULL
                };

                #define INITERROR return NULL

                PyMODINIT_FUNC PyInit_extension(void)

                #else

                #define INITERROR return

                void initextension(void)

                #endif
                {
                #if PY_MAJOR_VERSION >= 3
                    PyObject *module = PyModule_Create(&moduledef);
                #else
                    PyObject *module = Py_InitModule("extension", NULL);
                #endif
                    if (module == NULL)
                        INITERROR;
                #if PY_MAJOR_VERSION >= 3
                    return module;
                #endif
                }
                '''
            ),
        },
        setup_kwargs=dict(
            ext_modules=[
                Record('setuptools.Extension',
                       name='extension',
                       sources=['extension.c'])
            ],
        ),
        install_tree=flatten_tree({
            'foo-1.0-py{py_version}-{platform}.egg': [
                'extension{shlib_ext}',
                {'EGG-INFO': [
                    'PKG-INFO',
                    'RECORD',
                    'WHEEL',
                    'top_level.txt',
                ]},
            ]
        }),
    ),

    dict(
        id='header',
        file_defs={
            'header.h': DALS(
                '''
                '''
            ),
        },
        setup_kwargs=dict(
            headers=['header.h'],
        ),
        install_tree=flatten_tree({
            'foo-1.0-py{py_version}.egg': [
                'header.h',
                {'EGG-INFO': [
                    'PKG-INFO',
                    'RECORD',
                    'WHEEL',
                    'top_level.txt',
                ]},
            ]
        }),
    ),

    dict(
        id='script',
        file_defs={
            'script.py': DALS(
                '''
                #/usr/bin/python
                print('hello world!')
                '''
            ),
            'script.sh': DALS(
                '''
                #/bin/sh
                echo 'hello world!'
                '''
            ),
        },
        setup_kwargs=dict(
            scripts=['script.py', 'script.sh'],
        ),
        install_tree=flatten_tree({
            'foo-1.0-py{py_version}.egg': {
                'EGG-INFO': [
                    'PKG-INFO',
                    'RECORD',
                    'WHEEL',
                    'top_level.txt',
                    {'scripts': [
                        'script.py',
                        'script.sh'
                    ]}

                ]
            }
        })
    ),

    dict(
        id='requires1',
        install_requires='foobar==2.0',
        install_tree=flatten_tree({
            'foo-1.0-py{py_version}.egg': {
                'EGG-INFO': [
                    'PKG-INFO',
                    'RECORD',
                    'WHEEL',
                    'requires.txt',
                    'top_level.txt',
                ]
            }
        }),
        requires_txt=DALS(
            '''
            foobar==2.0
            '''
        ),
    ),

    dict(
        id='requires2',
        install_requires='''
        bar
        foo<=2.0; %r in sys_platform
        ''' % sys.platform,
        requires_txt=DALS(
            '''
            bar
            foo<=2.0
            '''
        ),
    ),

    dict(
        id='requires3',
        install_requires='''
        bar; %r != sys_platform
        ''' % sys.platform,
    ),

    dict(
        id='requires4',
        install_requires='''
        foo
        ''',
        extras_require={
            'extra': 'foobar>3',
        },
        requires_txt=DALS(
            '''
            foo

            [extra]
            foobar>3
            '''
        ),
    ),

    dict(
        id='requires5',
        extras_require={
            'extra': 'foobar; %r != sys_platform' % sys.platform,
        },
        requires_txt=DALS(
            '''
            [extra]
            '''
        ),
    ),

    dict(
        id='namespace_package',
        file_defs={
            'foo': {
                'bar': {
                    '__init__.py': ''
                },
            },
        },
        setup_kwargs=dict(
            namespace_packages=['foo'],
            packages=['foo.bar'],
        ),
        install_tree=flatten_tree({
            'foo-1.0-py{py_version}.egg': [
                'foo-1.0-py{py_version}-nspkg.pth',
                {'EGG-INFO': [
                    'PKG-INFO',
                    'RECORD',
                    'WHEEL',
                    'namespace_packages.txt',
                    'top_level.txt',
                ]},
                {'foo': [
                    '__init__.py',
                    {'bar': ['__init__.py']},
                ]},
            ]
        }),
    ),

    dict(
        id='data_in_package',
        file_defs={
            'foo': {
                '__init__.py': '',
                'data_dir': {
                    'data.txt': DALS(
                        '''
                        Some data...
                        '''
                    ),
                }
            }
        },
        setup_kwargs=dict(
            packages=['foo'],
            data_files=[('foo/data_dir', ['foo/data_dir/data.txt'])],
        ),
        install_tree=flatten_tree({
            'foo-1.0-py{py_version}.egg': {
                'EGG-INFO': [
                    'PKG-INFO',
                    'RECORD',
                    'WHEEL',
                    'top_level.txt',
                ],
                'foo': [
                    '__init__.py',
                    {'data_dir': [
                        'data.txt',
                    ]}
                ]
            }
        }),
    ),

)

@pytest.mark.parametrize(
    'params', WHEEL_INSTALL_TESTS,
    ids=list(params['id'] for params in WHEEL_INSTALL_TESTS),
)
def test_wheel_install(params):
    project_name = params.get('name', 'foo')
    version = params.get('version', '1.0')
    install_requires = params.get('install_requires', [])
    extras_require = params.get('extras_require', {})
    requires_txt = params.get('requires_txt', None)
    install_tree = params.get('install_tree')
    file_defs = params.get('file_defs', {})
    setup_kwargs = params.get('setup_kwargs', {})
    with build_wheel(
        name=project_name,
        version=version,
        install_requires=install_requires,
        extras_require=extras_require,
        extra_file_defs=file_defs,
        **setup_kwargs
    ) as filename, tempdir() as install_dir:
        _check_wheel_install(filename, install_dir,
                             install_tree, project_name,
                             version, requires_txt)


def test_wheel_install_pep_503():
    project_name = 'Foo_Bar'    # PEP 503 canonicalized name is "foo-bar"
    version = '1.0'
    with build_wheel(
        name=project_name,
        version=version,
    ) as filename, tempdir() as install_dir:
        new_filename = filename.replace(project_name,
                                        canonicalize_name(project_name))
        shutil.move(filename, new_filename)
        _check_wheel_install(new_filename, install_dir, None,
                             canonicalize_name(project_name),
                             version, None)


def test_wheel_no_dist_dir():
    project_name = 'nodistinfo'
    version = '1.0'
    wheel_name = '{0}-{1}-py2.py3-none-any.whl'.format(project_name, version)
    with tempdir() as source_dir:
        wheel_path = os.path.join(source_dir, wheel_name)
        # create an empty zip file
        zipfile.ZipFile(wheel_path, 'w').close()
        with tempdir() as install_dir:
            with pytest.raises(ValueError):
                _check_wheel_install(wheel_path, install_dir, None,
                                     project_name,
                                     version, None)
