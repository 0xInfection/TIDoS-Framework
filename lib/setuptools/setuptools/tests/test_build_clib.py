import pytest
import os
import shutil

import mock
from distutils.errors import DistutilsSetupError
from setuptools.command.build_clib import build_clib
from setuptools.dist import Distribution


class TestBuildCLib:
    @mock.patch(
            'setuptools.command.build_clib.newer_pairwise_group'
            )
    def test_build_libraries(self, mock_newer):
        dist = Distribution()
        cmd = build_clib(dist)

        # this will be a long section, just making sure all
        # exceptions are properly raised
        libs = [('example', {'sources': 'broken.c'})]
        with pytest.raises(DistutilsSetupError):
            cmd.build_libraries(libs)

        obj_deps = 'some_string'
        libs = [('example', {'sources': ['source.c'], 'obj_deps': obj_deps})]
        with pytest.raises(DistutilsSetupError):
            cmd.build_libraries(libs)

        obj_deps = {'': ''}
        libs = [('example', {'sources': ['source.c'], 'obj_deps': obj_deps})]
        with pytest.raises(DistutilsSetupError):
            cmd.build_libraries(libs)

        obj_deps = {'source.c': ''}
        libs = [('example', {'sources': ['source.c'], 'obj_deps': obj_deps})]
        with pytest.raises(DistutilsSetupError):
            cmd.build_libraries(libs)

        # with that out of the way, let's see if the crude dependency
        # system works
        cmd.compiler = mock.MagicMock(spec=cmd.compiler)
        mock_newer.return_value = ([],[])

        obj_deps = {'': ('global.h',), 'example.c': ('example.h',)}
        libs = [('example', {'sources': ['example.c'] ,'obj_deps': obj_deps})]

        cmd.build_libraries(libs)
        assert [['example.c', 'global.h', 'example.h']] in mock_newer.call_args[0]
        assert not cmd.compiler.compile.called
        assert cmd.compiler.create_static_lib.call_count == 1

        # reset the call numbers so we can test again
        cmd.compiler.reset_mock()

        mock_newer.return_value = ''  # anything as long as it's not ([],[])
        cmd.build_libraries(libs)
        assert cmd.compiler.compile.call_count == 1
        assert cmd.compiler.create_static_lib.call_count == 1
