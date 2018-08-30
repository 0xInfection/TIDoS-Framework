# -*- coding: utf-8 -*-
"""sdist tests"""

import contextlib
import os
import shutil
import sys
import tempfile
import itertools
from distutils import log
from distutils.errors import DistutilsTemplateError

import pkg_resources.py31compat
from setuptools.command.egg_info import FileList, egg_info, translate_pattern
from setuptools.dist import Distribution
from setuptools.extern import six
from setuptools.tests.textwrap import DALS

import pytest

__metaclass__ = type

py3_only = pytest.mark.xfail(six.PY2, reason="Test runs on Python 3 only")


def make_local_path(s):
    """Converts '/' in a string to os.sep"""
    return s.replace('/', os.sep)


SETUP_ATTRS = {
    'name': 'app',
    'version': '0.0',
    'packages': ['app'],
}

SETUP_PY = """\
from setuptools import setup

setup(**%r)
""" % SETUP_ATTRS


@contextlib.contextmanager
def quiet():
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = six.StringIO(), six.StringIO()
    try:
        yield
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr


def touch(filename):
    open(filename, 'w').close()


# The set of files always in the manifest, including all files in the
# .egg-info directory
default_files = frozenset(map(make_local_path, [
    'README.rst',
    'MANIFEST.in',
    'setup.py',
    'app.egg-info/PKG-INFO',
    'app.egg-info/SOURCES.txt',
    'app.egg-info/dependency_links.txt',
    'app.egg-info/top_level.txt',
    'app/__init__.py',
]))


translate_specs = [
    ('foo', ['foo'], ['bar', 'foobar']),
    ('foo/bar', ['foo/bar'], ['foo/bar/baz', './foo/bar', 'foo']),

    # Glob matching
    ('*.txt', ['foo.txt', 'bar.txt'], ['foo/foo.txt']),
    ('dir/*.txt', ['dir/foo.txt', 'dir/bar.txt', 'dir/.txt'], ['notdir/foo.txt']),
    ('*/*.py', ['bin/start.py'], []),
    ('docs/page-?.txt', ['docs/page-9.txt'], ['docs/page-10.txt']),

    # Globstars change what they mean depending upon where they are
    (
        'foo/**/bar',
        ['foo/bing/bar', 'foo/bing/bang/bar', 'foo/bar'],
        ['foo/abar'],
    ),
    (
        'foo/**',
        ['foo/bar/bing.py', 'foo/x'],
        ['/foo/x'],
    ),
    (
        '**',
        ['x', 'abc/xyz', '@nything'],
        [],
    ),

    # Character classes
    (
        'pre[one]post',
        ['preopost', 'prenpost', 'preepost'],
        ['prepost', 'preonepost'],
    ),

    (
        'hello[!one]world',
        ['helloxworld', 'helloyworld'],
        ['hellooworld', 'helloworld', 'hellooneworld'],
    ),

    (
        '[]one].txt',
        ['o.txt', '].txt', 'e.txt'],
        ['one].txt'],
    ),

    (
        'foo[!]one]bar',
        ['fooybar'],
        ['foo]bar', 'fooobar', 'fooebar'],
    ),

]
"""
A spec of inputs for 'translate_pattern' and matches and mismatches
for that input.
"""

match_params = itertools.chain.from_iterable(
    zip(itertools.repeat(pattern), matches)
    for pattern, matches, mismatches in translate_specs
)


@pytest.fixture(params=match_params)
def pattern_match(request):
    return map(make_local_path, request.param)


mismatch_params = itertools.chain.from_iterable(
    zip(itertools.repeat(pattern), mismatches)
    for pattern, matches, mismatches in translate_specs
)


@pytest.fixture(params=mismatch_params)
def pattern_mismatch(request):
    return map(make_local_path, request.param)


def test_translated_pattern_match(pattern_match):
    pattern, target = pattern_match
    assert translate_pattern(pattern).match(target)


def test_translated_pattern_mismatch(pattern_mismatch):
    pattern, target = pattern_mismatch
    assert not translate_pattern(pattern).match(target)


class TempDirTestCase:
    def setup_method(self, method):
        self.temp_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self, method):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.temp_dir)


class TestManifestTest(TempDirTestCase):
    def setup_method(self, method):
        super(TestManifestTest, self).setup_method(method)

        f = open(os.path.join(self.temp_dir, 'setup.py'), 'w')
        f.write(SETUP_PY)
        f.close()
        """
        Create a file tree like:
        - LICENSE
        - README.rst
        - testing.rst
        - .hidden.rst
        - app/
            - __init__.py
            - a.txt
            - b.txt
            - c.rst
            - static/
                - app.js
                - app.js.map
                - app.css
                - app.css.map
        """

        for fname in ['README.rst', '.hidden.rst', 'testing.rst', 'LICENSE']:
            touch(os.path.join(self.temp_dir, fname))

        # Set up the rest of the test package
        test_pkg = os.path.join(self.temp_dir, 'app')
        os.mkdir(test_pkg)
        for fname in ['__init__.py', 'a.txt', 'b.txt', 'c.rst']:
            touch(os.path.join(test_pkg, fname))

        # Some compiled front-end assets to include
        static = os.path.join(test_pkg, 'static')
        os.mkdir(static)
        for fname in ['app.js', 'app.js.map', 'app.css', 'app.css.map']:
            touch(os.path.join(static, fname))

    def make_manifest(self, contents):
        """Write a MANIFEST.in."""
        with open(os.path.join(self.temp_dir, 'MANIFEST.in'), 'w') as f:
            f.write(DALS(contents))

    def get_files(self):
        """Run egg_info and get all the files to include, as a set"""
        dist = Distribution(SETUP_ATTRS)
        dist.script_name = 'setup.py'
        cmd = egg_info(dist)
        cmd.ensure_finalized()

        cmd.run()

        return set(cmd.filelist.files)

    def test_no_manifest(self):
        """Check a missing MANIFEST.in includes only the standard files."""
        assert (default_files - set(['MANIFEST.in'])) == self.get_files()

    def test_empty_files(self):
        """Check an empty MANIFEST.in includes only the standard files."""
        self.make_manifest("")
        assert default_files == self.get_files()

    def test_include(self):
        """Include extra rst files in the project root."""
        self.make_manifest("include *.rst")
        files = default_files | set([
            'testing.rst', '.hidden.rst'])
        assert files == self.get_files()

    def test_exclude(self):
        """Include everything in app/ except the text files"""
        l = make_local_path
        self.make_manifest(
            """
            include app/*
            exclude app/*.txt
            """)
        files = default_files | set([l('app/c.rst')])
        assert files == self.get_files()

    def test_include_multiple(self):
        """Include with multiple patterns."""
        l = make_local_path
        self.make_manifest("include app/*.txt app/static/*")
        files = default_files | set([
            l('app/a.txt'), l('app/b.txt'),
            l('app/static/app.js'), l('app/static/app.js.map'),
            l('app/static/app.css'), l('app/static/app.css.map')])
        assert files == self.get_files()

    def test_graft(self):
        """Include the whole app/static/ directory."""
        l = make_local_path
        self.make_manifest("graft app/static")
        files = default_files | set([
            l('app/static/app.js'), l('app/static/app.js.map'),
            l('app/static/app.css'), l('app/static/app.css.map')])
        assert files == self.get_files()

    def test_graft_glob_syntax(self):
        """Include the whole app/static/ directory."""
        l = make_local_path
        self.make_manifest("graft */static")
        files = default_files | set([
            l('app/static/app.js'), l('app/static/app.js.map'),
            l('app/static/app.css'), l('app/static/app.css.map')])
        assert files == self.get_files()

    def test_graft_global_exclude(self):
        """Exclude all *.map files in the project."""
        l = make_local_path
        self.make_manifest(
            """
            graft app/static
            global-exclude *.map
            """)
        files = default_files | set([
            l('app/static/app.js'), l('app/static/app.css')])
        assert files == self.get_files()

    def test_global_include(self):
        """Include all *.rst, *.js, and *.css files in the whole tree."""
        l = make_local_path
        self.make_manifest(
            """
            global-include *.rst *.js *.css
            """)
        files = default_files | set([
            '.hidden.rst', 'testing.rst', l('app/c.rst'),
            l('app/static/app.js'), l('app/static/app.css')])
        assert files == self.get_files()

    def test_graft_prune(self):
        """Include all files in app/, except for the whole app/static/ dir."""
        l = make_local_path
        self.make_manifest(
            """
            graft app
            prune app/static
            """)
        files = default_files | set([
            l('app/a.txt'), l('app/b.txt'), l('app/c.rst')])
        assert files == self.get_files()


class TestFileListTest(TempDirTestCase):
    """
    A copy of the relevant bits of distutils/tests/test_filelist.py,
    to ensure setuptools' version of FileList keeps parity with distutils.
    """

    def setup_method(self, method):
        super(TestFileListTest, self).setup_method(method)
        self.threshold = log.set_threshold(log.FATAL)
        self._old_log = log.Log._log
        log.Log._log = self._log
        self.logs = []

    def teardown_method(self, method):
        log.set_threshold(self.threshold)
        log.Log._log = self._old_log
        super(TestFileListTest, self).teardown_method(method)

    def _log(self, level, msg, args):
        if level not in (log.DEBUG, log.INFO, log.WARN, log.ERROR, log.FATAL):
            raise ValueError('%s wrong log level' % str(level))
        self.logs.append((level, msg, args))

    def get_logs(self, *levels):
        def _format(msg, args):
            if len(args) == 0:
                return msg
            return msg % args
        return [_format(msg, args) for level, msg, args
                in self.logs if level in levels]

    def clear_logs(self):
        self.logs = []

    def assertNoWarnings(self):
        assert self.get_logs(log.WARN) == []
        self.clear_logs()

    def assertWarnings(self):
        assert len(self.get_logs(log.WARN)) > 0
        self.clear_logs()

    def make_files(self, files):
        for file in files:
            file = os.path.join(self.temp_dir, file)
            dirname, basename = os.path.split(file)
            pkg_resources.py31compat.makedirs(dirname, exist_ok=True)
            open(file, 'w').close()

    def test_process_template_line(self):
        # testing  all MANIFEST.in template patterns
        file_list = FileList()
        l = make_local_path

        # simulated file list
        self.make_files([
            'foo.tmp', 'ok', 'xo', 'four.txt',
            'buildout.cfg',
            # filelist does not filter out VCS directories,
            # it's sdist that does
            l('.hg/last-message.txt'),
            l('global/one.txt'),
            l('global/two.txt'),
            l('global/files.x'),
            l('global/here.tmp'),
            l('f/o/f.oo'),
            l('dir/graft-one'),
            l('dir/dir2/graft2'),
            l('dir3/ok'),
            l('dir3/sub/ok.txt'),
        ])

        MANIFEST_IN = DALS("""\
        include ok
        include xo
        exclude xo
        include foo.tmp
        include buildout.cfg
        global-include *.x
        global-include *.txt
        global-exclude *.tmp
        recursive-include f *.oo
        recursive-exclude global *.x
        graft dir
        prune dir3
        """)

        for line in MANIFEST_IN.split('\n'):
            if not line:
                continue
            file_list.process_template_line(line)

        wanted = [
            'buildout.cfg',
            'four.txt',
            'ok',
            l('.hg/last-message.txt'),
            l('dir/graft-one'),
            l('dir/dir2/graft2'),
            l('f/o/f.oo'),
            l('global/one.txt'),
            l('global/two.txt'),
        ]

        file_list.sort()
        assert file_list.files == wanted

    def test_exclude_pattern(self):
        # return False if no match
        file_list = FileList()
        assert not file_list.exclude_pattern('*.py')

        # return True if files match
        file_list = FileList()
        file_list.files = ['a.py', 'b.py']
        assert file_list.exclude_pattern('*.py')

        # test excludes
        file_list = FileList()
        file_list.files = ['a.py', 'a.txt']
        file_list.exclude_pattern('*.py')
        file_list.sort()
        assert file_list.files == ['a.txt']

    def test_include_pattern(self):
        # return False if no match
        file_list = FileList()
        self.make_files([])
        assert not file_list.include_pattern('*.py')

        # return True if files match
        file_list = FileList()
        self.make_files(['a.py', 'b.txt'])
        assert file_list.include_pattern('*.py')

        # test * matches all files
        file_list = FileList()
        self.make_files(['a.py', 'b.txt'])
        file_list.include_pattern('*')
        file_list.sort()
        assert file_list.files == ['a.py', 'b.txt']

    def test_process_template_line_invalid(self):
        # invalid lines
        file_list = FileList()
        for action in ('include', 'exclude', 'global-include',
                       'global-exclude', 'recursive-include',
                       'recursive-exclude', 'graft', 'prune', 'blarg'):
            try:
                file_list.process_template_line(action)
            except DistutilsTemplateError:
                pass
            except Exception:
                assert False, "Incorrect error thrown"
            else:
                assert False, "Should have thrown an error"

    def test_include(self):
        l = make_local_path
        # include
        file_list = FileList()
        self.make_files(['a.py', 'b.txt', l('d/c.py')])

        file_list.process_template_line('include *.py')
        file_list.sort()
        assert file_list.files == ['a.py']
        self.assertNoWarnings()

        file_list.process_template_line('include *.rb')
        file_list.sort()
        assert file_list.files == ['a.py']
        self.assertWarnings()

    def test_exclude(self):
        l = make_local_path
        # exclude
        file_list = FileList()
        file_list.files = ['a.py', 'b.txt', l('d/c.py')]

        file_list.process_template_line('exclude *.py')
        file_list.sort()
        assert file_list.files == ['b.txt', l('d/c.py')]
        self.assertNoWarnings()

        file_list.process_template_line('exclude *.rb')
        file_list.sort()
        assert file_list.files == ['b.txt', l('d/c.py')]
        self.assertWarnings()

    def test_global_include(self):
        l = make_local_path
        # global-include
        file_list = FileList()
        self.make_files(['a.py', 'b.txt', l('d/c.py')])

        file_list.process_template_line('global-include *.py')
        file_list.sort()
        assert file_list.files == ['a.py', l('d/c.py')]
        self.assertNoWarnings()

        file_list.process_template_line('global-include *.rb')
        file_list.sort()
        assert file_list.files == ['a.py', l('d/c.py')]
        self.assertWarnings()

    def test_global_exclude(self):
        l = make_local_path
        # global-exclude
        file_list = FileList()
        file_list.files = ['a.py', 'b.txt', l('d/c.py')]

        file_list.process_template_line('global-exclude *.py')
        file_list.sort()
        assert file_list.files == ['b.txt']
        self.assertNoWarnings()

        file_list.process_template_line('global-exclude *.rb')
        file_list.sort()
        assert file_list.files == ['b.txt']
        self.assertWarnings()

    def test_recursive_include(self):
        l = make_local_path
        # recursive-include
        file_list = FileList()
        self.make_files(['a.py', l('d/b.py'), l('d/c.txt'), l('d/d/e.py')])

        file_list.process_template_line('recursive-include d *.py')
        file_list.sort()
        assert file_list.files == [l('d/b.py'), l('d/d/e.py')]
        self.assertNoWarnings()

        file_list.process_template_line('recursive-include e *.py')
        file_list.sort()
        assert file_list.files == [l('d/b.py'), l('d/d/e.py')]
        self.assertWarnings()

    def test_recursive_exclude(self):
        l = make_local_path
        # recursive-exclude
        file_list = FileList()
        file_list.files = ['a.py', l('d/b.py'), l('d/c.txt'), l('d/d/e.py')]

        file_list.process_template_line('recursive-exclude d *.py')
        file_list.sort()
        assert file_list.files == ['a.py', l('d/c.txt')]
        self.assertNoWarnings()

        file_list.process_template_line('recursive-exclude e *.py')
        file_list.sort()
        assert file_list.files == ['a.py', l('d/c.txt')]
        self.assertWarnings()

    def test_graft(self):
        l = make_local_path
        # graft
        file_list = FileList()
        self.make_files(['a.py', l('d/b.py'), l('d/d/e.py'), l('f/f.py')])

        file_list.process_template_line('graft d')
        file_list.sort()
        assert file_list.files == [l('d/b.py'), l('d/d/e.py')]
        self.assertNoWarnings()

        file_list.process_template_line('graft e')
        file_list.sort()
        assert file_list.files == [l('d/b.py'), l('d/d/e.py')]
        self.assertWarnings()

    def test_prune(self):
        l = make_local_path
        # prune
        file_list = FileList()
        file_list.files = ['a.py', l('d/b.py'), l('d/d/e.py'), l('f/f.py')]

        file_list.process_template_line('prune d')
        file_list.sort()
        assert file_list.files == ['a.py', l('f/f.py')]
        self.assertNoWarnings()

        file_list.process_template_line('prune e')
        file_list.sort()
        assert file_list.files == ['a.py', l('f/f.py')]
        self.assertWarnings()
