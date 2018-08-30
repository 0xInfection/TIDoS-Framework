import sys

from mock import patch

from setuptools import pep425tags

__metaclass__ = type


class TestPEP425Tags:

    def mock_get_config_var(self, **kwd):
        """
        Patch sysconfig.get_config_var for arbitrary keys.
        """
        get_config_var = pep425tags.sysconfig.get_config_var

        def _mock_get_config_var(var):
            if var in kwd:
                return kwd[var]
            return get_config_var(var)
        return _mock_get_config_var

    def abi_tag_unicode(self, flags, config_vars):
        """
        Used to test ABI tags, verify correct use of the `u` flag
        """
        config_vars.update({'SOABI': None})
        base = pep425tags.get_abbr_impl() + pep425tags.get_impl_ver()

        if sys.version_info < (3, 3):
            config_vars.update({'Py_UNICODE_SIZE': 2})
            mock_gcf = self.mock_get_config_var(**config_vars)
            with patch('setuptools.pep425tags.sysconfig.get_config_var', mock_gcf):
                abi_tag = pep425tags.get_abi_tag()
                assert abi_tag == base + flags

            config_vars.update({'Py_UNICODE_SIZE': 4})
            mock_gcf = self.mock_get_config_var(**config_vars)
            with patch('setuptools.pep425tags.sysconfig.get_config_var',
                       mock_gcf):
                abi_tag = pep425tags.get_abi_tag()
                assert abi_tag == base + flags + 'u'

        else:
            # On Python >= 3.3, UCS-4 is essentially permanently enabled, and
            # Py_UNICODE_SIZE is None. SOABI on these builds does not include
            # the 'u' so manual SOABI detection should not do so either.
            config_vars.update({'Py_UNICODE_SIZE': None})
            mock_gcf = self.mock_get_config_var(**config_vars)
            with patch('setuptools.pep425tags.sysconfig.get_config_var',
                       mock_gcf):
                abi_tag = pep425tags.get_abi_tag()
                assert abi_tag == base + flags

    def test_broken_sysconfig(self):
        """
        Test that pep425tags still works when sysconfig is broken.
        Can be a problem on Python 2.7
        Issue #1074.
        """
        def raises_ioerror(var):
            raise IOError("I have the wrong path!")

        with patch('setuptools.pep425tags.sysconfig.get_config_var',
                   raises_ioerror):
            assert len(pep425tags.get_supported())

    def test_no_hyphen_tag(self):
        """
        Test that no tag contains a hyphen.
        """
        mock_gcf = self.mock_get_config_var(SOABI='cpython-35m-darwin')

        with patch('setuptools.pep425tags.sysconfig.get_config_var',
                   mock_gcf):
            supported = pep425tags.get_supported()

        for (py, abi, plat) in supported:
            assert '-' not in py
            assert '-' not in abi
            assert '-' not in plat

    def test_manual_abi_noflags(self):
        """
        Test that no flags are set on a non-PyDebug, non-Pymalloc ABI tag.
        """
        self.abi_tag_unicode('', {'Py_DEBUG': False, 'WITH_PYMALLOC': False})

    def test_manual_abi_d_flag(self):
        """
        Test that the `d` flag is set on a PyDebug, non-Pymalloc ABI tag.
        """
        self.abi_tag_unicode('d', {'Py_DEBUG': True, 'WITH_PYMALLOC': False})

    def test_manual_abi_m_flag(self):
        """
        Test that the `m` flag is set on a non-PyDebug, Pymalloc ABI tag.
        """
        self.abi_tag_unicode('m', {'Py_DEBUG': False, 'WITH_PYMALLOC': True})

    def test_manual_abi_dm_flags(self):
        """
        Test that the `dm` flags are set on a PyDebug, Pymalloc ABI tag.
        """
        self.abi_tag_unicode('dm', {'Py_DEBUG': True, 'WITH_PYMALLOC': True})


class TestManylinux1Tags:

    @patch('setuptools.pep425tags.get_platform', lambda: 'linux_x86_64')
    @patch('setuptools.glibc.have_compatible_glibc',
           lambda major, minor: True)
    def test_manylinux1_compatible_on_linux_x86_64(self):
        """
        Test that manylinux1 is enabled on linux_x86_64
        """
        assert pep425tags.is_manylinux1_compatible()

    @patch('setuptools.pep425tags.get_platform', lambda: 'linux_i686')
    @patch('setuptools.glibc.have_compatible_glibc',
           lambda major, minor: True)
    def test_manylinux1_compatible_on_linux_i686(self):
        """
        Test that manylinux1 is enabled on linux_i686
        """
        assert pep425tags.is_manylinux1_compatible()

    @patch('setuptools.pep425tags.get_platform', lambda: 'linux_x86_64')
    @patch('setuptools.glibc.have_compatible_glibc',
           lambda major, minor: False)
    def test_manylinux1_2(self):
        """
        Test that manylinux1 is disabled with incompatible glibc
        """
        assert not pep425tags.is_manylinux1_compatible()

    @patch('setuptools.pep425tags.get_platform', lambda: 'arm6vl')
    @patch('setuptools.glibc.have_compatible_glibc',
           lambda major, minor: True)
    def test_manylinux1_3(self):
        """
        Test that manylinux1 is disabled on arm6vl
        """
        assert not pep425tags.is_manylinux1_compatible()

    @patch('setuptools.pep425tags.get_platform', lambda: 'linux_x86_64')
    @patch('setuptools.glibc.have_compatible_glibc',
           lambda major, minor: True)
    @patch('sys.platform', 'linux2')
    def test_manylinux1_tag_is_first(self):
        """
        Test that the more specific tag manylinux1 comes first.
        """
        groups = {}
        for pyimpl, abi, arch in pep425tags.get_supported():
            groups.setdefault((pyimpl, abi), []).append(arch)

        for arches in groups.values():
            if arches == ['any']:
                continue
            # Expect the most specific arch first:
            if len(arches) == 3:
                assert arches == ['manylinux1_x86_64', 'linux_x86_64', 'any']
            else:
                assert arches == ['manylinux1_x86_64', 'linux_x86_64']
