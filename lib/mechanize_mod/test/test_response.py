"""Tests for mechanize._response.seek_wrapper and friends."""

import copy
import cStringIO
from unittest import TestCase


class TestUnSeekable:

    def __init__(self, text):
        self._file = cStringIO.StringIO(text)
        self.log = []

    def tell(self): return self._file.tell()

    def seek(self, offset, whence=0): assert False

    def read(self, size=-1):
        self.log.append(("read", size))
        return self._file.read(size)

    def readline(self, size=-1):
        self.log.append(("readline", size))
        return self._file.readline(size)

    def readlines(self, sizehint=-1):
        self.log.append(("readlines", sizehint))
        return self._file.readlines(sizehint)


class TestUnSeekableResponse(TestUnSeekable):

    def __init__(self, text, headers):
        TestUnSeekable.__init__(self, text)
        self.code = 200
        self.msg = "OK"
        self.headers = headers
        self.url = "http://example.com/"

    def geturl(self):
        return self.url

    def info(self):
        return self.headers

    def close(self):
        pass


class SeekableTests(TestCase):

    text = """\
The quick brown fox
jumps over the lazy

dog.

"""
    text_lines = map(lambda l: l + "\n", text.split("\n")[:-1])

    def testSeekable(self):
        from mechanize._response import seek_wrapper
        text = self.text
        for ii in range(1, 6):
            fh = TestUnSeekable(text)
            sfh = seek_wrapper(fh)
            test = getattr(self, "_test%d" % ii)
            test(sfh)

        # copies have independent seek positions
        fh = TestUnSeekable(text)
        sfh = seek_wrapper(fh)
        self._testCopy(sfh)

    def _testCopy(self, sfh):
        sfh2 = copy.copy(sfh)
        sfh.read(10)
        text = self.text
        self.assertEqual(sfh2.read(10), text[:10])
        sfh2.seek(5)
        self.assertEqual(sfh.read(10), text[10:20])
        self.assertEqual(sfh2.read(10), text[5:15])
        sfh.seek(0)
        sfh2.seek(0)
        return sfh2

    def _test1(self, sfh):
        text = self.text
        text_lines = self.text_lines
        assert sfh.read(10) == text[:10]  # calls fh.read
        assert sfh.log[-1] == ("read", 10)  # .log delegated to fh
        sfh.seek(0)  # doesn't call fh.seek
        assert sfh.read(10) == text[:10]  # doesn't call fh.read
        assert len(sfh.log) == 1
        sfh.seek(0)
        assert sfh.read(5) == text[:5]  # read only part of cached data
        assert len(sfh.log) == 1
        sfh.seek(0)
        assert sfh.read(25) == text[:25]  # calls fh.read
        assert sfh.log[1] == ("read", 15)
        lines = []
        sfh.seek(-1, 1)
        while 1:
            l = sfh.readline()
            if l == "":
                break
            lines.append(l)
        assert lines == ["s over the lazy\n"] + text_lines[2:]
        assert sfh.log[2:] == [("readline", -1)] * 5
        sfh.seek(0)
        lines = []
        while 1:
            l = sfh.readline()
            if l == "":
                break
            lines.append(l)
        assert lines == text_lines

    def _test2(self, sfh):
        text = self.text
        sfh.read(5)
        sfh.seek(0)
        assert sfh.read() == text
        assert sfh.read() == ""
        sfh.seek(0)
        assert sfh.read() == text
        sfh.seek(0)
        assert sfh.readline(5) == "The q"
        assert sfh.read() == text[5:]
        sfh.seek(0)
        assert sfh.readline(5) == "The q"
        assert sfh.readline() == "uick brown fox\n"

    def _test3(self, sfh):
        text_lines = self.text_lines
        sfh.read(25)
        sfh.seek(-1, 1)
        self.assertEqual(sfh.readlines(), [
                         "s over the lazy\n"] + text_lines[2:])
        sfh.seek(0)
        assert sfh.readlines() == text_lines

    def _test4(self, sfh):
        text_lines = self.text_lines
        count = 0
        limit = 10
        while count < limit:
            if count == 5:
                self.assertRaises(StopIteration, sfh.next)
                break
            else:
                sfh.next() == text_lines[count]
            count = count + 1
        else:
            assert False, "StopIteration not raised"

    def _test5(self, sfh):
        text = self.text
        sfh.read(10)
        sfh.seek(5)
        self.assert_(sfh.invariant())
        sfh.seek(0, 2)
        self.assert_(sfh.invariant())
        sfh.seek(0)
        self.assertEqual(sfh.read(), text)

    def testResponseSeekWrapper(self):
        from mechanize import response_seek_wrapper
        hdrs = {"Content-type": "text/html"}
        r = TestUnSeekableResponse(self.text, hdrs)
        rsw = response_seek_wrapper(r)
        rsw2 = self._testCopy(rsw)
        self.assert_(rsw is not rsw2)
        self.assertEqual(rsw.info(), rsw2.info())
        self.assert_(rsw.info() is not rsw2.info())

        # should be able to close already-closed object
        rsw2.close()
        rsw2.close()

    def testSetResponseData(self):
        from mechanize import response_seek_wrapper
        r = TestUnSeekableResponse(self.text, {'blah': 'yawn'})
        rsw = response_seek_wrapper(r)
        rsw.set_data("""\
A Seeming somwhat more than View;
  That doth instruct the Mind
  In Things that ly behind,
""")
        self.assertEqual(rsw.read(9), "A Seeming")
        self.assertEqual(rsw.read(13), " somwhat more")
        rsw.seek(0)
        self.assertEqual(rsw.read(9), "A Seeming")
        self.assertEqual(rsw.readline(), " somwhat more than View;\n")
        rsw.seek(0)
        self.assertEqual(rsw.readline(), "A Seeming somwhat more than View;\n")
        rsw.seek(-1, 1)
        self.assertEqual(rsw.read(7), "\n  That")

        r = TestUnSeekableResponse(self.text, {'blah': 'yawn'})
        rsw = response_seek_wrapper(r)
        rsw.set_data(self.text)
        self._test2(rsw)
        rsw.seek(0)
        self._test4(rsw)

    def testGetResponseData(self):
        from mechanize import response_seek_wrapper
        r = TestUnSeekableResponse(self.text, {'blah': 'yawn'})
        rsw = response_seek_wrapper(r)

        self.assertEqual(rsw.get_data(), self.text)
        self._test2(rsw)
        rsw.seek(0)
        self._test4(rsw)


if __name__ == "__main__":
    import unittest
    unittest.main()
