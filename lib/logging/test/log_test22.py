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
"""Test harness for the logging module. Demonstrates the use of different
converters for time(secs) -> time(tuple).

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""

import logging, time

def main():
    handler = logging.StreamHandler()
    f1 = logging.Formatter("%(asctime)s %(message)s", "%m/%d %H:%M:%S")
    f2 = logging.Formatter("%(asctime)s %(message)s", "%m/%d %H:%M:%S")
    f2.converter = time.gmtime
    handler.setFormatter(f1)
    root = logging.getLogger("")
    root.setLevel(logging.DEBUG)
    root.addHandler(handler)
    root.info("Something happened! [should be in local time]")
    handler.setFormatter(f2)
    root.info("Something else happened! [should be in GMT]")
    handler.setFormatter(f1)
    root.info("Something happened again! [should be in local time]")
    logging.Formatter.converter = time.gmtime
    root.info("Something else happened again! [should be in GMT]")
    logging.Formatter.converter = time.localtime
    root.info("Something else happened yet again! [should be in local time]")

if __name__ == "__main__":
    main()
