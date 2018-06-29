import os

from .conf import get_setting

__title__ = 'tld.helpers'
__author__ = 'Artur Barseghyan'
__copyright__ = '2013-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'project_dir',
    'PROJECT_DIR',
)


def project_dir(base):
    """Project dir."""
    tld_names_local_path_parent = get_setting('NAMES_LOCAL_PATH_PARENT')
    return os.path.abspath(
        os.path.join(tld_names_local_path_parent, base).replace('\\', '/')
    )


PROJECT_DIR = project_dir
