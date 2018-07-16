import os
import time
import sys
import unittest

import mechanize
from mechanize._testcase import TestCase, TempDirMaker
from mechanize._rfc3986 import urljoin
from mechanize._mechanize import sanepathname2url

KB = 1024
MB = 1024**2
GB = 1024**3


def time_it(operation):
    t = time.time()
    operation()
    return time.time() - t


def write_data(filename, nr_bytes):
    block_size = 4096
    block = "01234567" * (block_size // 8)
    fh = open(filename, "w")
    try:
        for i in range(nr_bytes // block_size):
            fh.write(block)
    finally:
        fh.close()


def time_retrieve_local_file(temp_maker, size, retrieve_fn):
    temp_dir = temp_maker.make_temp_dir()
    filename = os.path.join(temp_dir, "data")
    write_data(filename, size)

    def operation():
        retrieve_fn(
            urljoin('file://', sanepathname2url(filename)),
            os.path.join(temp_dir, "retrieved"))

    return time_it(operation)


class PerformanceTests(TestCase):
    def test_retrieve_local_file(self):
        def retrieve(url, filename):
            br = mechanize.Browser()
            br.retrieve(url, filename)

        size = 100 * MB
        #         size = 1 * KB
        desired_rate = 2 * MB  # per second
        desired_time = size / float(desired_rate)
        fudge_factor = 2.
        self.assert_less_than(
            time_retrieve_local_file(self, size, retrieve),
            desired_time * fudge_factor)


def show_plot(rows):
    import matplotlib.pyplot
    figure = matplotlib.pyplot.figure()
    axes = figure.add_subplot(111)
    axes.plot([row[0] for row in rows], [row[1] for row in rows])
    matplotlib.pyplot.show()


def power_2_range(start, stop):
    n = start
    while n <= stop:
        yield n
        n *= 2


def performance_plot():
    def retrieve(url, filename):
        br = mechanize.Browser()
        br.retrieve(url, filename)

#     import urllib2
#     def retrieve(url, filename):
#         urllib2.urlopen(url).read()

#     from mechanize import _useragent
#     ua = _useragent.UserAgent()
#     ua.set_seekable_responses(True)
#     ua.set_handle_equiv(False)
#     def retrieve(url, filename):
#         ua.retrieve(url, filename)

    rows = []
    for size in power_2_range(256 * KB, 256 * MB):
        temp_maker = TempDirMaker()
        try:
            elapsed = time_retrieve_local_file(temp_maker, size, retrieve)
        finally:
            temp_maker.tear_down()
        rows.append((size // float(MB), elapsed))
    show_plot(rows)

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--plot" in args:
        performance_plot()
    else:
        unittest.main()
