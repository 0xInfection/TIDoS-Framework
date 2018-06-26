import codecs
import os
import re
import sys

from distutils.core import setup, Extension

if (sys.version_info >= (2, 6, 0)):
    raise ValueError("This extension should not be used with "
                     + "Python 2.6 or later (already built in), "
                     + "and has not been tested with Python 2.3.4 "
                     + "or earlier.")
elif (sys.version_info < (2, 3, 5)):
    sys.stderr.write("Warning:  This code has not been tested "
                     + "with versions of Python less than 2.3.5.\n")


def find_file(filename, std_dirs, paths):
    """Searches for the directory where a given file is located,
    and returns a possibly-empty list of additional directories, or None
    if the file couldn't be found at all.

    'filename' is the name of a file, such as readline.h or libcrypto.a.
    'std_dirs' is the list of standard system directories; if the
        file is found in one of them, no additional directives are needed.
    'paths' is a list of additional locations to check; if the file is
        found in one of them, the resulting list will contain the directory.
    """

    # Check the standard locations
    for dir in std_dirs:
        f = os.path.join(dir, filename)
        print 'looking for', f
        if os.path.exists(f):
            return []

    # Check the additional directories
    for dir in paths:
        f = os.path.join(dir, filename)
        print 'looking for', f
        if os.path.exists(f):
            return [dir]

    # Not found anywhere
    return None


def find_library_file(compiler, libname, std_dirs, paths):
    result = compiler.find_library_file(std_dirs + paths, libname)
    if result is None:
        return None

    # Check whether the found file is in one of the standard directories
    dirname = os.path.dirname(result)
    for p in std_dirs:
        # Ensure path doesn't end with path separator
        p = p.rstrip(os.sep)
        if p == dirname:
            return []

    # Otherwise, it must have been in one of the additional directories,
    # so we have to figure out which one.
    for p in paths:
        # Ensure path doesn't end with path separator
        p = p.rstrip(os.sep)
        if p == dirname:
            return [p]
    else:
        assert False, "Internal error: Path not found in std_dirs or paths"


def find_ssl():

    # Detect SSL support for the socket module (via _ssl)
    from distutils.ccompiler import new_compiler

    compiler = new_compiler()
    inc_dirs = compiler.include_dirs + ['/usr/include']

    search_for_ssl_incs_in = [
        '/usr/local/ssl/include',
        '/usr/contrib/ssl/include/',
    ]
    ssl_incs = find_file('openssl/ssl.h', inc_dirs, search_for_ssl_incs_in)
    if ssl_incs is not None:
        krb5_h = find_file('krb5.h', inc_dirs,
                           ['/usr/kerberos/include'])
        if krb5_h:
            ssl_incs += krb5_h

    ssl_libs = find_library_file(compiler, 'ssl',
        ['/usr/lib', '/usr/lib/i386-linux-gnu', '/usr/lib/x86_64-linux-gnu'],
        ['/usr/local/lib', '/usr/local/ssl/lib', '/usr/contrib/ssl/lib/'])

    if (ssl_incs is not None and ssl_libs is not None):
        return ssl_incs, ssl_libs, ['ssl', 'crypto']

    raise Exception("No SSL support found")

if (sys.version_info >= (2, 5, 1)):
    socket_inc = "./ssl/2.5.1"
else:
    socket_inc = "./ssl/2.3.6"

link_args = []
if sys.platform == 'win32':

    # Assume the openssl libraries from GnuWin32 are installed in the
    # following location:
    gnuwin32_dir = os.environ.get("GNUWIN32_DIR", r"C:\Utils\GnuWin32")

    # Set this to 1 for a dynamic build (depends on openssl DLLs)
    # Dynamic build is about 26k, static is 670k
    dynamic = int(os.environ.get("SSL_DYNAMIC", 0))

    ssl_incs = [os.environ.get("C_INCLUDE_DIR") or os.path.join(gnuwin32_dir, "include")]
    ssl_libs = [os.environ.get("C_LIB_DIR") or os.path.join(gnuwin32_dir, "lib")]
    libs = ['ssl', 'crypto', 'wsock32']
    if not dynamic:
        libs = libs + ['gdi32', 'gw32c', 'ole32', 'uuid']
        link_args = ['-static']
else:
    ssl_incs, ssl_libs, libs = find_ssl()


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='ssl',
      version=find_version('ssl', '__init__.py'),
      description='SSL wrapper for socket objects (2.3, 2.4, 2.5 compatible)',
      long_description=read('README.rst'),
      license='Python (MIT-like)',
      author='See long_description for details',
      author_email='pypa-dev@googlegroups.com',
      url='https://github.com/pypa/ssl',
      packages=['ssl'],
      ext_modules=[Extension('ssl._ssl2', ['ssl/_ssl2.c'],
                             include_dirs=ssl_incs + [socket_inc],
                             library_dirs=ssl_libs,
                             libraries=libs,
                             extra_link_args=link_args)]
      )
