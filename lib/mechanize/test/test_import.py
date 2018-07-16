import unittest

import mechanize
from mechanize._testcase import TestCase


class ImportTests(TestCase):

    def test_import_all(self):
        for name in mechanize.__all__:
            exec "from mechanize import %s" % name


if __name__ == "__main__":
    unittest.main()
