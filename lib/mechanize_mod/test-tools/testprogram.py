import doctest
import errno
import glob
import logging
import optparse
import os
import socket
import subprocess
import sys
import time
import unittest
import urllib

import mechanize
import mechanize._rfc3986
import mechanize._testcase as _testcase


"""Test runner.

Local test HTTP server support and a few other bits and pieces.
"""

USAGE = """
%prog [OPTIONS...] [ARGUMENTS...]
%prog [discover [OPTIONS...]] [ARGUMENTS...]

Examples:

python test.py  # all tests
python test.py test_api  # run test/test_api.py
python test.py test_functional # run test/test_functional.py
python test.py mechanize/_headersutil  # run the doctests from this module
python test.py test_functional.CookieJarTests  # just this class
# just this test method
python test.py test_functional.CookieJarTests.test_mozilla_cookiejar

python test.py discover --pattern test_browser.doctest  # doctest file
# run test/test_functional.py
python test.py discover --pattern test_functional.py

python test.py --tag internet  # include tests that use the internet
"""

# TODO: resurrect cgitb support


class ServerStartupError(Exception):

    pass


class ServerProcess:

    def __init__(self, filename, name=None):
        if filename is None:
            raise ValueError('filename arg must be a string')
        if name is None:
            name = filename
        self.name = os.path.basename(name)
        self.port = None
        self.report_hook = lambda msg: None
        self._filename = filename
        self._args = None
        self._process = None

    def _get_args(self):
        """Return list of command line arguments.

        Override me.
        """
        return []

    def _start(self):
        self._args = [sys.executable, self._filename] + self._get_args()
        self.report_hook("starting (%s)" % (self._args,))
        self._process = subprocess.Popen(self._args)
        self.report_hook("waiting for startup")
        self._wait_for_startup()
        self.report_hook("running")

    def _wait_for_startup(self):
        def connect():
            self._process.poll()
            if self._process.returncode is not None:
                message = ("server exited on startup with status %d: %r" %
                           (self._process.returncode, self._args))
                raise ServerStartupError(message)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(1.0)
            try:
                sock.connect(('127.0.0.1', self.port))
            finally:
                sock.close()
        backoff(connect, (socket.error,))

    def stop(self):
        """Kill process (forcefully if necessary)."""
        if os.name == 'nt':
            self._process.kill()
        else:
            kill_posix(self._process.pid, self.report_hook)


def backoff(func, errors,
            initial_timeout=1., hard_timeout=60., factor=1.2):
    starttime = time.time()
    timeout = initial_timeout
    while time.time() < starttime + hard_timeout - 0.01:
        try:
            func()
        except errors:
            time.sleep(timeout)
            timeout *= factor
            hard_limit = hard_timeout - (time.time() - starttime)
            timeout = min(timeout, hard_limit)
        else:
            break
    else:
        raise


def kill_posix(pid, report_hook):
    import signal
    os.kill(pid, signal.SIGTERM)

    timeout = 10.
    starttime = time.time()
    report_hook("waiting for exit")
    def do_nothing(*args):
        pass
    old_handler = signal.signal(signal.SIGCHLD, do_nothing)
    try:
        while time.time() < starttime + timeout - 0.01:
            pid, sts = os.waitpid(pid, os.WNOHANG)
            if pid != 0:
                # exited, or error
                break
            newtimeout = timeout - (time.time() - starttime) - 1.
            time.sleep(newtimeout)  # wait for signal
        else:
            report_hook("forcefully killing")
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError as exc:
                if exc.errno != errno.ECHILD:
                    raise
    finally:
        signal.signal(signal.SIGCHLD, old_handler)


class TwistedServerProcess(ServerProcess):

    def __init__(self, uri, name, log=False):
        this_dir = os.path.dirname(__file__)
        path = os.path.join(this_dir, "twisted-localserver.py")
        ServerProcess.__init__(self, path, name)
        self.uri = uri
        authority = mechanize._rfc3986.urlsplit(uri)[1]
        host, port = urllib.splitport(authority)
        if port is None:
            port = "80"
        self.port = int(port)
        # def report(msg):
        #     print "%s: %s" % (name, msg)
        report = lambda msg: None
        self.report_hook = report
        self._log = log
        self._start()

    def _get_args(self):
        args = [str(self.port)]
        if self._log:
            args.append("--log")
        return args


class TwistedFtpServerProcess(ServerProcess):

    def __init__(self, name, port=2121, log=False):
        this_dir = os.path.dirname(__file__)
        path = os.path.join(this_dir, "twisted-ftpserver.py")
        ServerProcess.__init__(self, path, name)
        self._temp_maker = mechanize._testcase.TempDirMaker()
        self.root_path = self._temp_maker.make_temp_dir()
        self.port = port
        report = lambda msg: None
        self.report_hook = report
        self._log = log
        self._start()

    def _get_args(self):
        args = ["--port", str(self.port), self.root_path]
        # if self._log:
        #     args.append("--log")
        return args

    def stop(self):
        ServerProcess.stop(self)
        self._temp_maker.tear_down()


class ServerCM(object):

    def __init__(self, make_server):
        self._server = None
        self._make_server = make_server

    def __enter__(self):
        assert self._server is None
        server = self._make_server()
        self._server = server
        return self._server

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._server.stop()
        self._server = None


class NullServer(object):

    def __init__(self, uri, name=None):
        self.uri = uri


class TrivialCM(object):

    def __init__(self, obj):
        self._obj = obj

    def __enter__(self):
        return self._obj

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass


def add_attributes_to_test_cases(suite, attributes):
    for test in suite:
        if isinstance(test, unittest.TestCase):
            for name, value in attributes.iteritems():
                setattr(test, name, value)
        else:
            try:
                add_attributes_to_test_cases(test, attributes)
            except AttributeError:
                pass


class FixtureCacheSuite(unittest.TestSuite):

    def __init__(self, fixture_factory, *args, **kwds):
        unittest.TestSuite.__init__(self, *args, **kwds)
        self._fixture_factory = fixture_factory

    def run(self, result):
        try:
            super(FixtureCacheSuite, self).run(result)
        finally:
            self._fixture_factory.tear_down()


def toplevel_test(suite, test_attributes):
    suite = FixtureCacheSuite(test_attributes["fixture_factory"], suite)
    add_attributes_to_test_cases(suite, test_attributes)
    return suite


def make_http_server_cm(uri, log):
    import warnings
    # http://code.google.com/p/rdflib/issues/detail?id=101
    warnings.filterwarnings(
        action="ignore",
        message=(".*Module test was already imported from "
                 ".*test/__init__.pyc?, but .* is being added to "
                 "sys.path"),
        category=UserWarning,
        module="zope")
    try:
        import twisted.web
        import zope.interface
        twisted.web, zope.interface
    except ImportError:
        warnings.warn("Skipping functional tests: Failed to import "
                      "twisted.web and/or zope.interface")
        def skip():
            raise unittest.SkipTest
        cm = ServerCM(skip)
    else:
        cm = ServerCM(lambda: TwistedServerProcess(
            uri, "local twisted server", log))
    return cm


def make_ftp_server_cm(log):
    import warnings
    try:
        import twisted.protocols.ftp
        import zope.interface
        twisted.protocols.ftp, zope.interface
    except ImportError:
        warnings.warn("Skipping functional tests: Failed to import "
                      "twisted.protocols.ftp and/or zope.interface")
        def skip():
            raise unittest.SkipTest
        cm = ServerCM(skip)
    else:
        cm = ServerCM(lambda: TwistedFtpServerProcess(
            "local twisted server", 2121, log))
    return cm


class TestProgram(unittest.TestProgram):

    def __init__(self, default_discovery_args=None,
                 *args, **kwds):
        self._default_discovery_args = default_discovery_args
        unittest.TestProgram.__init__(self, *args, **kwds)

    def _parse_options(self, argv):
        parser = optparse.OptionParser(usage=USAGE)
        # plain old unittest
        parser.add_option("-v", "--verbose", action="store_true",
                          help="Verbose output")
        parser.add_option("-q", "--quiet", action="store_true",
                          help="No output")
        # from bundled Python 2.7 stdlib test discovery
        parser.add_option("-s", "--start-directory", dest="start", default=".",
                          help='Directory to start discovery ("." default)')
        parser.add_option("-p", "--pattern", dest="pattern",
                          default="test*.py",
                          help='Pattern to match tests ("test*.py" default)')
        parser.add_option("-t", "--top-level-directory", dest="top",
                          default=None,
                          help=("Top level directory of project (defaults to "
                                "start directory)"))
        # mechanize additions
        # TODO: test_urllib2_localnet ignores --uri and --no-local-server
        note = ("Note that there are two local servers in use, and this "
                "option only affects the twisted server, not the server used "
                "by test_urllib2_localnet (which originates from standard "
                "library).")
        parser.add_option(
            "--uri", metavar="URI",
            help="Run functional tests against base URI.  " + note)
        parser.add_option(
            "--no-local-server", action="store_false",
            dest="run_local_server", default=True,
            help=("Don't run local test server.  By default, this runs the "
                  "functional tests against mechanize sourceforge site, use "
                  "--uri to override that.  " + note))
        # TODO: probably not everything respects this (test_urllib2_localnet?)
        parser.add_option("--no-proxies", action="store_true")
        parser.add_option("--log", action="store_true",
                          help=('Turn on logging for logger "mechanize" at '
                                'level logging.DEBUG'))
        parser.add_option("--log-server", action="store_true",
                          help=("Turn on logging for twisted.web local HTTP "
                                " server"))

        options, remaining_args = parser.parse_args(argv)
        if len(remaining_args) > 3:
            self.usageExit()

        options.do_discovery = ((len(remaining_args) == 0 and
                                 self._default_discovery_args is not None) or
                                (len(remaining_args) >= 1 and
                                 remaining_args[0].lower() == "discover"))
        if options.do_discovery:
            if len(remaining_args) == 0:
                discovery_args = self._default_discovery_args
            else:
                discovery_args = remaining_args[1:]
            for name, value in zip(("start", "pattern", "top"),
                                   discovery_args):
                setattr(options, name, value)
        else:
            options.test_names = remaining_args
        if options.uri is None:
            if options.run_local_server:
                options.uri = "http://127.0.0.1:8000"
            else:
                options.uri = "http://wwwsearch.sourceforge.net/"
        return options

    def _do_discovery(self, options):
        start_dir = options.start
        pattern = options.pattern
        top_level_dir = options.top
        loader = unittest.TestLoader()
        self.test = loader.discover(start_dir, pattern, top_level_dir)

        finder = doctest.DocTestFinder(exclude_empty=False)
        for name in glob.glob('mechanize/*.py'):
            name = os.path.basename(name).rpartition('.')[0]
            self.test.addTest(
                doctest.DocTestSuite('mechanize.' + name, test_finder=finder))
        self.test.addTest(doctest.DocFileSuite(
            *glob.glob('test/*.doctest'), module_relative=False))

    def _vanilla_unittest_main(self, options):
        if len(options.test_names) == 0 and self.defaultTest is None:
            # createTests will load tests from self.module
            self.testNames = None
        elif len(options.test_names) > 0:
            self.testNames = options.test_names
        else:
            self.testNames = (self.defaultTest,)
        self.createTests()

    def parseArgs(self, argv):
        options = self._parse_options(argv[1:])
        if options.verbose:
            self.verbosity = 2
        if options.quiet:
            self.verbosity = 0
        if options.do_discovery:
            self._do_discovery(options)
        else:
            self._vanilla_unittest_main(options)

        if options.log:
            level = logging.DEBUG
            # level = logging.INFO
            # level = logging.WARNING
            # level = logging.NOTSET
            logger = logging.getLogger("mechanize")
            logger.setLevel(level)
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level)
            logger.addHandler(handler)

        fixture_factory = _testcase.FixtureFactory()
        if options.run_local_server:
            cm = make_http_server_cm(options.uri, options.log_server)
        else:
            cm = TrivialCM(NullServer(options.uri))
        fixture_factory.register_context_manager("server", cm)
        fixture_factory.register_context_manager(
            "ftp_server", make_ftp_server_cm(options.log_server))
        test_attributes = dict(uri=options.uri, no_proxies=options.no_proxies,
                               fixture_factory=fixture_factory)
        self.test = toplevel_test(self.test, test_attributes)


main = TestProgram
