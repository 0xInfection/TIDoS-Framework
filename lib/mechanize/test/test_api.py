import unittest


class ImportTests(unittest.TestCase):

    def test_import_all(self):
        # the following will raise an exception if __all__ contains undefined
        # classes
        from mechanize import *


if __name__ == "__main__":
    unittest.main()
