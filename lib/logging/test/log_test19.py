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
"""Test harness for the logging module. A basic test of parents.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""

import logging

def main():
    logging.basicConfig()
    root = logging.getLogger("")
    ab = logging.getLogger("a.b")
    abc = logging.getLogger("a.b.c")
    root.setLevel(logging.ERROR)
    ab.setLevel(logging.INFO)
    abc.info("Info")
    abc.warning("Warning")
    abc.error("Error")
    print "abc = %s" % abc
    print "abc.parent = %s" % abc.parent
    print "ab = %s" % ab
    print "ab.parent = %s" % ab.parent
    print "root = %s" % root

if __name__ == "__main__":
    import sys
    print sys.argv[0]
    args = sys.argv[1:]
    if "-profile" in args:
        import profile, pstats
        args.remove("-profile")
        statf = "log_test19.pro"
        profile.run("main()", statf)
        stats = pstats.Stats(statf)
        stats.strip_dirs().sort_stats('time').print_stats()
    else:
        main()
