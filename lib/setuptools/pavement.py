import re

from paver.easy import task, path as Path
import pip


def remove_all(paths):
    for path in paths:
        path.rmtree() if path.isdir() else path.remove()


@task
def update_vendored():
    update_pkg_resources()
    update_setuptools()


def rewrite_packaging(pkg_files, new_root):
    """
    Rewrite imports in packaging to redirect to vendored copies.
    """
    for file in pkg_files.glob('*.py'):
        text = file.text()
        text = re.sub(r' (pyparsing|six)', rf' {new_root}.\1', text)
        file.write_text(text)


def clean(vendor):
    """
    Remove all files out of the vendor directory except the meta
    data (as pip uninstall doesn't support -t).
    """
    remove_all(
        path
        for path in vendor.glob('*')
        if path.basename() != 'vendored.txt'
    )


def install(vendor):
    clean(vendor)
    install_args = [
        'install',
        '-r', str(vendor / 'vendored.txt'),
        '-t', str(vendor),
    ]
    pip.main(install_args)
    remove_all(vendor.glob('*.dist-info'))
    remove_all(vendor.glob('*.egg-info'))
    (vendor / '__init__.py').write_text('')


def update_pkg_resources():
    vendor = Path('pkg_resources/_vendor')
    install(vendor)
    rewrite_packaging(vendor / 'packaging', 'pkg_resources.extern')


def update_setuptools():
    vendor = Path('setuptools/_vendor')
    install(vendor)
    rewrite_packaging(vendor / 'packaging', 'setuptools.extern')
