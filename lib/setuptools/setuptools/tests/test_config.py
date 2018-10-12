import contextlib
import pytest
from distutils.errors import DistutilsOptionError, DistutilsFileError
from mock import patch
from setuptools.dist import Distribution, _Distribution
from setuptools.config import ConfigHandler, read_configuration
from . import py2_only, py3_only

class ErrConfigHandler(ConfigHandler):
    """Erroneous handler. Fails to implement required methods."""


def make_package_dir(name, base_dir, ns=False):
    dir_package = base_dir
    for dir_name in name.split('/'):
        dir_package = dir_package.mkdir(dir_name)
    init_file = None
    if not ns:
        init_file = dir_package.join('__init__.py')
        init_file.write('')
    return dir_package, init_file


def fake_env(tmpdir, setup_cfg, setup_py=None, package_path='fake_package'):

    if setup_py is None:
        setup_py = (
            'from setuptools import setup\n'
            'setup()\n'
        )

    tmpdir.join('setup.py').write(setup_py)
    config = tmpdir.join('setup.cfg')
    config.write(setup_cfg)

    package_dir, init_file = make_package_dir(package_path, tmpdir)

    init_file.write(
        'VERSION = (1, 2, 3)\n'
        '\n'
        'VERSION_MAJOR = 1'
        '\n'
        'def get_version():\n'
        '    return [3, 4, 5, "dev"]\n'
        '\n'
    )
    return package_dir, config


@contextlib.contextmanager
def get_dist(tmpdir, kwargs_initial=None, parse=True):
    kwargs_initial = kwargs_initial or {}

    with tmpdir.as_cwd():
        dist = Distribution(kwargs_initial)
        dist.script_name = 'setup.py'
        parse and dist.parse_config_files()

        yield dist


def test_parsers_implemented():

    with pytest.raises(NotImplementedError):
        handler = ErrConfigHandler(None, {})
        handler.parsers


class TestConfigurationReader:

    def test_basic(self, tmpdir):
        _, config = fake_env(
            tmpdir,
            '[metadata]\n'
            'version = 10.1.1\n'
            'keywords = one, two\n'
            '\n'
            '[options]\n'
            'scripts = bin/a.py, bin/b.py\n'
        )
        config_dict = read_configuration('%s' % config)
        assert config_dict['metadata']['version'] == '10.1.1'
        assert config_dict['metadata']['keywords'] == ['one', 'two']
        assert config_dict['options']['scripts'] == ['bin/a.py', 'bin/b.py']

    def test_no_config(self, tmpdir):
        with pytest.raises(DistutilsFileError):
            read_configuration('%s' % tmpdir.join('setup.cfg'))

    def test_ignore_errors(self, tmpdir):
        _, config = fake_env(
            tmpdir,
            '[metadata]\n'
            'version = attr: none.VERSION\n'
            'keywords = one, two\n'
        )
        with pytest.raises(ImportError):
            read_configuration('%s' % config)

        config_dict = read_configuration(
            '%s' % config, ignore_option_errors=True)

        assert config_dict['metadata']['keywords'] == ['one', 'two']
        assert 'version' not in config_dict['metadata']

        config.remove()


class TestMetadata:

    def test_basic(self, tmpdir):

        fake_env(
            tmpdir,
            '[metadata]\n'
            'version = 10.1.1\n'
            'description = Some description\n'
            'long_description_content_type = text/something\n'
            'long_description = file: README\n'
            'name = fake_name\n'
            'keywords = one, two\n'
            'provides = package, package.sub\n'
            'license = otherlic\n'
            'download_url = http://test.test.com/test/\n'
            'maintainer_email = test@test.com\n'
        )

        tmpdir.join('README').write('readme contents\nline2')

        meta_initial = {
            # This will be used so `otherlic` won't replace it.
            'license': 'BSD 3-Clause License',
        }

        with get_dist(tmpdir, meta_initial) as dist:
            metadata = dist.metadata

            assert metadata.version == '10.1.1'
            assert metadata.description == 'Some description'
            assert metadata.long_description_content_type == 'text/something'
            assert metadata.long_description == 'readme contents\nline2'
            assert metadata.provides == ['package', 'package.sub']
            assert metadata.license == 'BSD 3-Clause License'
            assert metadata.name == 'fake_name'
            assert metadata.keywords == ['one', 'two']
            assert metadata.download_url == 'http://test.test.com/test/'
            assert metadata.maintainer_email == 'test@test.com'

    def test_file_mixed(self, tmpdir):

        fake_env(
            tmpdir,
            '[metadata]\n'
            'long_description = file: README.rst, CHANGES.rst\n'
            '\n'
        )

        tmpdir.join('README.rst').write('readme contents\nline2')
        tmpdir.join('CHANGES.rst').write('changelog contents\nand stuff')

        with get_dist(tmpdir) as dist:
            assert dist.metadata.long_description == (
                'readme contents\nline2\n'
                'changelog contents\nand stuff'
            )

    def test_file_sandboxed(self, tmpdir):

        fake_env(
            tmpdir,
            '[metadata]\n'
            'long_description = file: ../../README\n'
        )

        with get_dist(tmpdir, parse=False) as dist:
            with pytest.raises(DistutilsOptionError):
                dist.parse_config_files()  # file: out of sandbox

    def test_aliases(self, tmpdir):

        fake_env(
            tmpdir,
            '[metadata]\n'
            'author-email = test@test.com\n'
            'home-page = http://test.test.com/test/\n'
            'summary = Short summary\n'
            'platform = a, b\n'
            'classifier =\n'
            '  Framework :: Django\n'
            '  Programming Language :: Python :: 3.5\n'
        )

        with get_dist(tmpdir) as dist:
            metadata = dist.metadata
            assert metadata.author_email == 'test@test.com'
            assert metadata.url == 'http://test.test.com/test/'
            assert metadata.description == 'Short summary'
            assert metadata.platforms == ['a', 'b']
            assert metadata.classifiers == [
                'Framework :: Django',
                'Programming Language :: Python :: 3.5',
            ]

    def test_multiline(self, tmpdir):

        fake_env(
            tmpdir,
            '[metadata]\n'
            'name = fake_name\n'
            'keywords =\n'
            '  one\n'
            '  two\n'
            'classifiers =\n'
            '  Framework :: Django\n'
            '  Programming Language :: Python :: 3.5\n'
        )
        with get_dist(tmpdir) as dist:
            metadata = dist.metadata
            assert metadata.keywords == ['one', 'two']
            assert metadata.classifiers == [
                'Framework :: Django',
                'Programming Language :: Python :: 3.5',
            ]

    def test_dict(self, tmpdir):

        fake_env(
            tmpdir,
            '[metadata]\n'
            'project_urls =\n'
            '  Link One = https://example.com/one/\n'
            '  Link Two = https://example.com/two/\n'
        )
        with get_dist(tmpdir) as dist:
            metadata = dist.metadata
            assert metadata.project_urls == {
                'Link One': 'https://example.com/one/',
                'Link Two': 'https://example.com/two/',
            }

    def test_version(self, tmpdir):

        _, config = fake_env(
            tmpdir,
            '[metadata]\n'
            'version = attr: fake_package.VERSION\n'
        )
        with get_dist(tmpdir) as dist:
            assert dist.metadata.version == '1.2.3'

        config.write(
            '[metadata]\n'
            'version = attr: fake_package.get_version\n'
        )
        with get_dist(tmpdir) as dist:
            assert dist.metadata.version == '3.4.5.dev'

        config.write(
            '[metadata]\n'
            'version = attr: fake_package.VERSION_MAJOR\n'
        )
        with get_dist(tmpdir) as dist:
            assert dist.metadata.version == '1'

        subpack = tmpdir.join('fake_package').mkdir('subpackage')
        subpack.join('__init__.py').write('')
        subpack.join('submodule.py').write('VERSION = (2016, 11, 26)')

        config.write(
            '[metadata]\n'
            'version = attr: fake_package.subpackage.submodule.VERSION\n'
        )
        with get_dist(tmpdir) as dist:
            assert dist.metadata.version == '2016.11.26'

    def test_version_file(self, tmpdir):

        _, config = fake_env(
            tmpdir,
            '[metadata]\n'
            'version = file: fake_package/version.txt\n'
        )
        tmpdir.join('fake_package', 'version.txt').write('1.2.3\n')

        with get_dist(tmpdir) as dist:
            assert dist.metadata.version == '1.2.3'

        tmpdir.join('fake_package', 'version.txt').write('1.2.3\n4.5.6\n')
        with pytest.raises(DistutilsOptionError):
            with get_dist(tmpdir) as dist:
                _ = dist.metadata.version

    def test_version_with_package_dir_simple(self, tmpdir):

        _, config = fake_env(
            tmpdir,
            '[metadata]\n'
            'version = attr: fake_package_simple.VERSION\n'
            '[options]\n'
            'package_dir =\n'
            '    = src\n',
            package_path='src/fake_package_simple'
        )

        with get_dist(tmpdir) as dist:
            assert dist.metadata.version == '1.2.3'

    def test_version_with_package_dir_rename(self, tmpdir):

        _, config = fake_env(
            tmpdir,
            '[metadata]\n'
            'version = attr: fake_package_rename.VERSION\n'
            '[options]\n'
            'package_dir =\n'
            '    fake_package_rename = fake_dir\n',
            package_path='fake_dir'
        )

        with get_dist(tmpdir) as dist:
            assert dist.metadata.version == '1.2.3'

    def test_version_with_package_dir_complex(self, tmpdir):

        _, config = fake_env(
            tmpdir,
            '[metadata]\n'
            'version = attr: fake_package_complex.VERSION\n'
            '[options]\n'
            'package_dir =\n'
            '    fake_package_complex = src/fake_dir\n',
            package_path='src/fake_dir'
        )

        with get_dist(tmpdir) as dist:
            assert dist.metadata.version == '1.2.3'

    def test_unknown_meta_item(self, tmpdir):

        fake_env(
            tmpdir,
            '[metadata]\n'
            'name = fake_name\n'
            'unknown = some\n'
        )
        with get_dist(tmpdir, parse=False) as dist:
            dist.parse_config_files()  # Skip unknown.

    def test_usupported_section(self, tmpdir):

        fake_env(
            tmpdir,
            '[metadata.some]\n'
            'key = val\n'
        )
        with get_dist(tmpdir, parse=False) as dist:
            with pytest.raises(DistutilsOptionError):
                dist.parse_config_files()

    def test_classifiers(self, tmpdir):
        expected = set([
            'Framework :: Django',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
        ])

        # From file.
        _, config = fake_env(
            tmpdir,
            '[metadata]\n'
            'classifiers = file: classifiers\n'
        )

        tmpdir.join('classifiers').write(
            'Framework :: Django\n'
            'Programming Language :: Python :: 3\n'
            'Programming Language :: Python :: 3.5\n'
        )

        with get_dist(tmpdir) as dist:
            assert set(dist.metadata.classifiers) == expected

        # From list notation
        config.write(
            '[metadata]\n'
            'classifiers =\n'
            '    Framework :: Django\n'
            '    Programming Language :: Python :: 3\n'
            '    Programming Language :: Python :: 3.5\n'
        )
        with get_dist(tmpdir) as dist:
            assert set(dist.metadata.classifiers) == expected


class TestOptions:

    def test_basic(self, tmpdir):

        fake_env(
            tmpdir,
            '[options]\n'
            'zip_safe = True\n'
            'use_2to3 = 1\n'
            'include_package_data = yes\n'
            'package_dir = b=c, =src\n'
            'packages = pack_a, pack_b.subpack\n'
            'namespace_packages = pack1, pack2\n'
            'use_2to3_fixers = your.fixers, or.here\n'
            'use_2to3_exclude_fixers = one.here, two.there\n'
            'convert_2to3_doctests = src/tests/one.txt, src/two.txt\n'
            'scripts = bin/one.py, bin/two.py\n'
            'eager_resources = bin/one.py, bin/two.py\n'
            'install_requires = docutils>=0.3; pack ==1.1, ==1.3; hey\n'
            'tests_require = mock==0.7.2; pytest\n'
            'setup_requires = docutils>=0.3; spack ==1.1, ==1.3; there\n'
            'dependency_links = http://some.com/here/1, '
                'http://some.com/there/2\n'
            'python_requires = >=1.0, !=2.8\n'
            'py_modules = module1, module2\n'
        )
        with get_dist(tmpdir) as dist:
            assert dist.zip_safe
            assert dist.use_2to3
            assert dist.include_package_data
            assert dist.package_dir == {'': 'src', 'b': 'c'}
            assert dist.packages == ['pack_a', 'pack_b.subpack']
            assert dist.namespace_packages == ['pack1', 'pack2']
            assert dist.use_2to3_fixers == ['your.fixers', 'or.here']
            assert dist.use_2to3_exclude_fixers == ['one.here', 'two.there']
            assert dist.convert_2to3_doctests == ([
                'src/tests/one.txt', 'src/two.txt'])
            assert dist.scripts == ['bin/one.py', 'bin/two.py']
            assert dist.dependency_links == ([
                'http://some.com/here/1',
                'http://some.com/there/2'
            ])
            assert dist.install_requires == ([
                'docutils>=0.3',
                'pack==1.1,==1.3',
                'hey'
            ])
            assert dist.setup_requires == ([
                'docutils>=0.3',
                'spack ==1.1, ==1.3',
                'there'
            ])
            assert dist.tests_require == ['mock==0.7.2', 'pytest']
            assert dist.python_requires == '>=1.0, !=2.8'
            assert dist.py_modules == ['module1', 'module2']

    def test_multiline(self, tmpdir):
        fake_env(
            tmpdir,
            '[options]\n'
            'package_dir = \n'
            '  b=c\n'
            '  =src\n'
            'packages = \n'
            '  pack_a\n'
            '  pack_b.subpack\n'
            'namespace_packages = \n'
            '  pack1\n'
            '  pack2\n'
            'use_2to3_fixers = \n'
            '  your.fixers\n'
            '  or.here\n'
            'use_2to3_exclude_fixers = \n'
            '  one.here\n'
            '  two.there\n'
            'convert_2to3_doctests = \n'
            '  src/tests/one.txt\n'
            '  src/two.txt\n'
            'scripts = \n'
            '  bin/one.py\n'
            '  bin/two.py\n'
            'eager_resources = \n'
            '  bin/one.py\n'
            '  bin/two.py\n'
            'install_requires = \n'
            '  docutils>=0.3\n'
            '  pack ==1.1, ==1.3\n'
            '  hey\n'
            'tests_require = \n'
            '  mock==0.7.2\n'
            '  pytest\n'
            'setup_requires = \n'
            '  docutils>=0.3\n'
            '  spack ==1.1, ==1.3\n'
            '  there\n'
            'dependency_links = \n'
            '  http://some.com/here/1\n'
            '  http://some.com/there/2\n'
        )
        with get_dist(tmpdir) as dist:
            assert dist.package_dir == {'': 'src', 'b': 'c'}
            assert dist.packages == ['pack_a', 'pack_b.subpack']
            assert dist.namespace_packages == ['pack1', 'pack2']
            assert dist.use_2to3_fixers == ['your.fixers', 'or.here']
            assert dist.use_2to3_exclude_fixers == ['one.here', 'two.there']
            assert dist.convert_2to3_doctests == (
                ['src/tests/one.txt', 'src/two.txt'])
            assert dist.scripts == ['bin/one.py', 'bin/two.py']
            assert dist.dependency_links == ([
                'http://some.com/here/1',
                'http://some.com/there/2'
            ])
            assert dist.install_requires == ([
                'docutils>=0.3',
                'pack==1.1,==1.3',
                'hey'
            ])
            assert dist.setup_requires == ([
                'docutils>=0.3',
                'spack ==1.1, ==1.3',
                'there'
            ])
            assert dist.tests_require == ['mock==0.7.2', 'pytest']

    def test_package_dir_fail(self, tmpdir):
        fake_env(
            tmpdir,
            '[options]\n'
            'package_dir = a b\n'
        )
        with get_dist(tmpdir, parse=False) as dist:
            with pytest.raises(DistutilsOptionError):
                dist.parse_config_files()

    def test_package_data(self, tmpdir):
        fake_env(
            tmpdir,
            '[options.package_data]\n'
            '* = *.txt, *.rst\n'
            'hello = *.msg\n'
            '\n'
            '[options.exclude_package_data]\n'
            '* = fake1.txt, fake2.txt\n'
            'hello = *.dat\n'
        )

        with get_dist(tmpdir) as dist:
            assert dist.package_data == {
                '': ['*.txt', '*.rst'],
                'hello': ['*.msg'],
            }
            assert dist.exclude_package_data == {
                '': ['fake1.txt', 'fake2.txt'],
                'hello': ['*.dat'],
            }

    def test_packages(self, tmpdir):
        fake_env(
            tmpdir,
            '[options]\n'
            'packages = find:\n'
        )

        with get_dist(tmpdir) as dist:
            assert dist.packages == ['fake_package']

    def test_find_directive(self, tmpdir):
        dir_package, config = fake_env(
            tmpdir,
            '[options]\n'
            'packages = find:\n'
        )

        dir_sub_one, _ = make_package_dir('sub_one', dir_package)
        dir_sub_two, _ = make_package_dir('sub_two', dir_package)

        with get_dist(tmpdir) as dist:
            assert set(dist.packages) == set([
                'fake_package', 'fake_package.sub_two', 'fake_package.sub_one'
            ])

        config.write(
            '[options]\n'
            'packages = find:\n'
            '\n'
            '[options.packages.find]\n'
            'where = .\n'
            'include =\n'
            '    fake_package.sub_one\n'
            '    two\n'
        )
        with get_dist(tmpdir) as dist:
            assert dist.packages == ['fake_package.sub_one']

        config.write(
            '[options]\n'
            'packages = find:\n'
            '\n'
            '[options.packages.find]\n'
            'exclude =\n'
            '    fake_package.sub_one\n'
        )
        with get_dist(tmpdir) as dist:
            assert set(dist.packages) == set(
                ['fake_package',  'fake_package.sub_two'])

    @py2_only
    def test_find_namespace_directive_fails_on_py2(self, tmpdir):
        dir_package, config = fake_env(
            tmpdir,
            '[options]\n'
            'packages = find_namespace:\n'
        )

        with pytest.raises(DistutilsOptionError):
            with get_dist(tmpdir) as dist:
                dist.parse_config_files()

    @py3_only
    def test_find_namespace_directive(self, tmpdir):
        dir_package, config = fake_env(
            tmpdir,
            '[options]\n'
            'packages = find_namespace:\n'
        )

        dir_sub_one, _ = make_package_dir('sub_one', dir_package)
        dir_sub_two, _ = make_package_dir('sub_two', dir_package, ns=True)

        with get_dist(tmpdir) as dist:
            assert set(dist.packages) == {
                'fake_package', 'fake_package.sub_two', 'fake_package.sub_one'
            }

        config.write(
            '[options]\n'
            'packages = find_namespace:\n'
            '\n'
            '[options.packages.find]\n'
            'where = .\n'
            'include =\n'
            '    fake_package.sub_one\n'
            '    two\n'
        )
        with get_dist(tmpdir) as dist:
            assert dist.packages == ['fake_package.sub_one']

        config.write(
            '[options]\n'
            'packages = find_namespace:\n'
            '\n'
            '[options.packages.find]\n'
            'exclude =\n'
            '    fake_package.sub_one\n'
        )
        with get_dist(tmpdir) as dist:
            assert set(dist.packages) == {
                'fake_package',  'fake_package.sub_two'
            }

    def test_extras_require(self, tmpdir):
        fake_env(
            tmpdir,
            '[options.extras_require]\n'
            'pdf = ReportLab>=1.2; RXP\n'
            'rest = \n'
            '  docutils>=0.3\n'
            '  pack ==1.1, ==1.3\n'
        )

        with get_dist(tmpdir) as dist:
            assert dist.extras_require == {
                'pdf': ['ReportLab>=1.2', 'RXP'],
                'rest': ['docutils>=0.3', 'pack==1.1,==1.3']
            }
            assert dist.metadata.provides_extras == set(['pdf', 'rest'])

    def test_entry_points(self, tmpdir):
        _, config = fake_env(
            tmpdir,
            '[options.entry_points]\n'
            'group1 = point1 = pack.module:func, '
                '.point2 = pack.module2:func_rest [rest]\n'
            'group2 = point3 = pack.module:func2\n'
        )

        with get_dist(tmpdir) as dist:
            assert dist.entry_points == {
                'group1': [
                    'point1 = pack.module:func',
                    '.point2 = pack.module2:func_rest [rest]',
                ],
                'group2': ['point3 = pack.module:func2']
            }

        expected = (
            '[blogtool.parsers]\n'
            '.rst = some.nested.module:SomeClass.some_classmethod[reST]\n'
        )

        tmpdir.join('entry_points').write(expected)

        # From file.
        config.write(
            '[options]\n'
            'entry_points = file: entry_points\n'
        )

        with get_dist(tmpdir) as dist:
            assert dist.entry_points == expected

saved_dist_init = _Distribution.__init__
class TestExternalSetters:
    # During creation of the setuptools Distribution() object, we call
    # the init of the parent distutils Distribution object via
    # _Distribution.__init__ ().
    #
    # It's possible distutils calls out to various keyword
    # implementations (i.e. distutils.setup_keywords entry points)
    # that may set a range of variables.
    #
    # This wraps distutil's Distribution.__init__ and simulates
    # pbr or something else setting these values.
    def _fake_distribution_init(self, dist, attrs):
        saved_dist_init(dist, attrs)
        # see self._DISTUTUILS_UNSUPPORTED_METADATA
        setattr(dist.metadata, 'long_description_content_type',
                'text/something')
        # Test overwrite setup() args
        setattr(dist.metadata, 'project_urls', {
            'Link One': 'https://example.com/one/',
            'Link Two': 'https://example.com/two/',
        })
        return None

    @patch.object(_Distribution, '__init__', autospec=True)
    def test_external_setters(self,  mock_parent_init, tmpdir):
        mock_parent_init.side_effect = self._fake_distribution_init

        dist = Distribution(attrs={
            'project_urls': {
                'will_be': 'ignored'
            }
        })

        assert dist.metadata.long_description_content_type == 'text/something'
        assert dist.metadata.project_urls == {
            'Link One': 'https://example.com/one/',
            'Link Two': 'https://example.com/two/',
        }
