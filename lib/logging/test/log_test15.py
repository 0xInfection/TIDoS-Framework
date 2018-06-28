#!/usr/bin/env python
#
# Copyright 2001-2004 by Vinay Sajip. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# This file is part of the standalone Python logging distribution. See
# http://www.red-dove.com/python_logging.html
#
"""
A test harness for the logging module. Tests Filter.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""

import sys, logging

FILTER = "a.b"

def message(s):
    sys.stderr.write("%s\n" % s)

def doLog():
    logging.getLogger("a").info("Info 1")
    logging.getLogger("a.b").info("Info 2")
    logging.getLogger("a.c").info("Info 3")
    logging.getLogger("a.b.c").info("Info 4")
    logging.getLogger("a.b.c.d").info("Info 5")
    logging.getLogger("a.bb.c").info("Info 6")
    logging.getLogger("b").info("Info 7")
    logging.getLogger("b.a").info("Info 8")
    logging.getLogger("c.a.b").info("Info 9")
    logging.getLogger("a.bb").info("Info 10")

def test(fs):
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    if __name__ == "__main__":
        hand = logging.StreamHandler()
        hand.setFormatter(logging.Formatter("%(name)-10s %(message)s"))
        root.addHandler(hand)
    else:
        hand = root.handlers[0]
    message("Unfiltered...")
    doLog()
    message("Filtered with '%s'..." % fs)
    filt = logging.Filter(fs)
    hand.addFilter(filt)
    doLog()
    hand.removeFilter(filt)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        fs = sys.argv[1]
    else:
        fs = FILTER
    test(fs)
