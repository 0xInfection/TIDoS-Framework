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
A test harness for the logging module. Tests MatchFilter.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""

import logging, types, string

class MatchFilter(logging.Filter):
    def __init__(self, **kwargs):
        self.dict = kwargs

    def matchOne(self, key, value, record):
        rv = getattr(record, key)
        if key != "name":
            if key not in ["message", "msg"]:
                return rv == value
            else:
                return string.find(str(rv), value) >= 0
        else:
            if rv == value:
                return 1
            nlen = len(value)
            if string.find(rv, value, 0, nlen) != 0:
                return 0
            if rv[nlen] == ".":
                return 1

    def matchValue(self, key, record):
        vl = self.dict [key]
        if type(vl) != types.ListType:
            rv = self.matchOne(key, vl, record)
        else:
            for v in vl:
                rv = self.matchOne(key, v, record)
                if rv:
                    break
        return rv

    def filter(self, record):
        rv = 1
        for k in self.dict.keys():
            if self.matchValue(k, record):
                rv = 0
                break
        return rv

def doLog(logger, n):
    logger.debug("Debug %d" % n)
    logger.info("Info %d" % n)
    logger.warning("Warning %d" % n)
    logger.error("Error %d" % n)
    logger.critical("Critical %d" % n)

def test():
    fmt = logging.Formatter("%(name)-10s %(levelname)-9s %(message)s")
    hand = logging.StreamHandler()
    hand.setFormatter(fmt)
    root = logging.getLogger("")
    root.setLevel(logging.DEBUG)
    root.addHandler(hand)
    loggers = ['A',
               'A.B',
               'A.BB',
               'A.C',
               'AA.B',
               'A.B.C',
               'A.B.C.D',
               'A.B.C.D.E',
               'Z.A.B',
              ]
    filt = MatchFilter(name = ['A.C', 'A.B.C'],                 #reject these loggers and their children
                       levelno = [logging.WARNING, logging.CRITICAL],  #reject these levels,
                       msg = 'bug 2'                            #reject if this in message
                      )
    hand.addFilter(filt)
    for log in loggers:
        doLog(logging.getLogger(log), loggers.index(log))

if __name__ == "__main__":
    test()
