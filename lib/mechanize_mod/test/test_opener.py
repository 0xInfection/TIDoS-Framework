#!/usr/bin/env python

import os
import math
import stat
import unittest

import mechanize
import mechanize._response as _response
import mechanize._sockettimeout as _sockettimeout


def killfile(filename):
    try:
        os.remove(filename)
    except OSError:
        if os.name == 'nt':
            try:
                os.chmod(filename, stat.S_IWRITE)
                os.remove(filename)
            except OSError:
                pass


class CloseVerifier(object):

    def __init__(self):
        self.count = 0

    def opened(self):
        self.count += 1

    def closed(self):
        self.count -= 1

    def verify(self, assert_equals):
        assert_equals(self.count, 0)


class ResponseCloseWrapper(object):

    def __init__(self, response, closed_callback, read):
        self._response = response
        self._closed_callback = closed_callback
        if read is None:
            self.read = response.read
        else:
            self.read = read

    def __getattr__(self, name):
        return getattr(self._response, name)

    def close(self):
        self._closed_callback()


class ResponseCloseVerifier(CloseVerifier):

    def __init__(self, read=None):
        CloseVerifier.__init__(self)
        self._read = read

    def open(self):
        self.opened()
        response = _response.test_response("spam")
        return ResponseCloseWrapper(response, self.closed, self._read)


class URLOpener(mechanize.OpenerDirector):

    def __init__(self, urlopen):
        self._urlopen = urlopen

    def open(self, *args, **kwds):
        return self._urlopen()


class FakeFile(object):

    def __init__(self, closed_callback):
        self._closed_callback = closed_callback

    def write(self, *args, **kwds):
        pass

    def close(self):
        self._closed_callback()


class FakeFilesystem(CloseVerifier):

    def open(self, path, mode="r"):
        self.opened()
        return FakeFile(self.closed)


class OpenerTests(unittest.TestCase):

    def _check_retrieve(self, urlopen):
        opener = URLOpener(urlopen=urlopen)
        fs = FakeFilesystem()
        try:
            filename, headers = opener.retrieve("http://example.com",
                                                "dummy filename",
                                                open=fs.open)
        except mechanize.URLError:
            pass
        fs.verify(self.assertEquals)

    def test_retrieve_closes_on_success(self):
        response_verifier = ResponseCloseVerifier()
        self._check_retrieve(urlopen=response_verifier.open)
        response_verifier.verify(self.assertEquals)

    def test_retrieve_closes_on_failure(self):
        def fail_to_open():
            raise mechanize.URLError("dummy reason")
        self._check_retrieve(fail_to_open)

    def test_retrieve_closes_on_read_failure(self):
        def fail_to_read(*args, **kwds):
            raise mechanize.URLError("dummy reason")
        response_verifier = ResponseCloseVerifier(read=fail_to_read)
        self._check_retrieve(urlopen=response_verifier.open)
        response_verifier.verify(self.assertEquals)

    def test_retrieve(self):
        # The .retrieve() method deals with a number of different cases.  In
        # each case, .read() should be called the expected number of times, the
        # progress callback should be called as expected, and we should end up
        # with a filename and some headers.

        class Opener(mechanize.OpenerDirector):

            def __init__(self, content_length=None):
                mechanize.OpenerDirector.__init__(self)
                self.calls = []
                self.block_size = mechanize.OpenerDirector.BLOCK_SIZE
                self.nr_blocks = 2.5
                self.data = int((self.block_size / 8) *
                                self.nr_blocks) * "01234567"
                self.total_size = len(self.data)
                self._content_length = content_length
            def open(self, fullurl, data=None,
                     timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
                self.calls.append((fullurl, data, timeout))
                headers = [("Foo", "Bar")]
                if self._content_length is not None:
                    if self._content_length is True:
                        content_length = str(len(self.data))
                    else:
                        content_length = str(self._content_length)
                    headers.append(("content-length", content_length))
                return _response.test_response(self.data, headers)

        class CallbackVerifier:

            def __init__(self, testcase, total_size, block_size):
                self.count = 0
                self._testcase = testcase
                self._total_size = total_size
                self._block_size = block_size
            def callback(self, block_nr, block_size, total_size):
                self._testcase.assertEqual(block_nr, self.count)
                self._testcase.assertEqual(block_size, self._block_size)
                self._testcase.assertEqual(total_size, self._total_size)
                self.count += 1

        # ensure we start without the test file present
        tfn = "mechanize_test_73940ukewrl.txt"
        killfile(tfn)

        # case 1: filename supplied
        op = Opener()
        verif = CallbackVerifier(self, -1, op.block_size)
        url = "http://example.com/"
        filename, headers = op.retrieve(
            url, tfn, reporthook=verif.callback)
        try:
            self.assertEqual(filename, tfn)
            self.assertEqual(headers["foo"], 'Bar')
            self.assertEqual(open(filename, "rb").read(), op.data)
            self.assertEqual(len(op.calls), 1)
            self.assertEqual(verif.count, math.ceil(op.nr_blocks) + 1)
            op.close()
            # .close()ing the opener does NOT remove non-temporary files
            self.assert_(os.path.isfile(filename))
        finally:
            killfile(filename)

        # case 2: no filename supplied, use a temporary file
        op = Opener(content_length=True)
        # We asked the Opener to add a content-length header to the response
        # this time.  Verify the total size passed to the callback is that case
        # is according to the content-length (rather than -1).
        verif = CallbackVerifier(self, op.total_size, op.block_size)
        url = "http://example.com/"
        filename, headers = op.retrieve(url, reporthook=verif.callback)
        self.assertNotEqual(filename, tfn)  # (some temp filename instead)
        self.assertEqual(headers["foo"], 'Bar')
        self.assertEqual(open(filename, "rb").read(), op.data)
        self.assertEqual(len(op.calls), 1)
        # .close()ing the opener removes temporary files
        self.assert_(os.path.exists(filename))
        op.close()
        self.failIf(os.path.exists(filename))
        self.assertEqual(verif.count, math.ceil(op.nr_blocks) + 1)

        # case 3: "file:" URL with no filename supplied
        # we DON'T create a temporary file, since there's a file there already
        op = Opener()
        verif = CallbackVerifier(self, -1, op.block_size)
        tifn = "input_for_" + tfn
        try:
            f = open(tifn, 'wb')
            try:
                f.write(op.data)
            finally:
                f.close()
            url = "file://" + tifn
            filename, headers = op.retrieve(url, reporthook=verif.callback)
            self.assertEqual(filename, None)  # this may change
            self.assertEqual(headers["foo"], 'Bar')
            self.assertEqual(open(tifn, "rb").read(), op.data)
            # no .read()s took place, since we already have the disk file,
            # and we weren't asked to write it to another filename
            self.assertEqual(verif.count, 0)
            op.close()
            # .close()ing the opener does NOT remove the file!
            self.assert_(os.path.isfile(tifn))
        finally:
            killfile(tifn)

        # case 4: "file:" URL and filename supplied
        # we DO create a new file in this case
        op = Opener()
        verif = CallbackVerifier(self, -1, op.block_size)
        tifn = "input_for_" + tfn
        try:
            f = open(tifn, 'wb')
            try:
                f.write(op.data)
            finally:
                f.close()
            url = "file://" + tifn
            try:
                filename, headers = op.retrieve(
                    url, tfn, reporthook=verif.callback)
                self.assertEqual(filename, tfn)
                self.assertEqual(headers["foo"], 'Bar')
                self.assertEqual(open(tifn, "rb").read(), op.data)
                self.assertEqual(verif.count, math.ceil(op.nr_blocks) + 1)
                op.close()
                # .close()ing the opener does NOT remove non-temporary files
                self.assert_(os.path.isfile(tfn))
            finally:
                killfile(tfn)
        finally:
            killfile(tifn)

        # Content-Length mismatch with real file length gives URLError
        big = 1024 * 32
        op = Opener(content_length=big)
        verif = CallbackVerifier(self, big, op.block_size)
        url = "http://example.com/"
        try:
            try:
                op.retrieve(url, reporthook=verif.callback)
            except mechanize.ContentTooShortError as exc:
                filename, headers = exc.result
                self.assertNotEqual(filename, tfn)
                self.assertEqual(headers["foo"], 'Bar')
                # We still read and wrote to disk everything available, despite
                # the exception.
                self.assertEqual(open(filename, "rb").read(), op.data)
                self.assertEqual(len(op.calls), 1)
                self.assertEqual(verif.count, math.ceil(op.nr_blocks) + 1)
                # cleanup should still take place
                self.assert_(os.path.isfile(filename))
                op.close()
                self.failIf(os.path.isfile(filename))
            else:
                self.fail()
        finally:
            killfile(filename)
