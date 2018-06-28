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
A test harness for the logging module. Tests thread safety.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""

import logging, logging.handlers, thread, threading, random

logging.raiseExceptions = 1

NUM_THREADS = 10
LOOP_COUNT = 10000

LOG_MESSAGES = [
    (logging.DEBUG, "%3d This is a %s message", "debug"),
    (logging.INFO, "%3d This is an %s message", "informational"),
    (logging.WARNING, "%3d This is a %s message", "warning"),
    (logging.ERROR, "%3d This is an %s message", "error"),
    (logging.CRITICAL, "%3d This is a %s message", "critical"),
]

LOG_NAMES = ["A", "A.B", "A.B.C", "A.B.C.D"]

def doLog(num):
    logger = logging.getLogger('')
    logger.info("*** thread %s started (%d)", thread.get_ident(), num)
    for i in xrange(LOOP_COUNT):
        logger = logging.getLogger(random.choice(LOG_NAMES))
        a = random.choice(LOG_MESSAGES)
        args = a[0:2] + (num,) + a[2:]
        apply(logger.log, args)

def test():
    f = logging.Formatter("%(asctime)s %(levelname)-9s %(name)-8s %(thread)5s %(message)s")
    root = logging.getLogger('')
    root.setLevel(logging.DEBUG)
    h = logging.FileHandler('thread.log', 'w')
    root.addHandler(h)
    h.setFormatter(f)
    h = logging.handlers.SocketHandler('localhost', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    #h = logging.handlers.DatagramHandler('localhost', logging.handlers.DEFAULT_UDP_LOGGING_PORT)
    root.addHandler(h)
    threads = []
    for i in xrange(NUM_THREADS):
        threads.append(threading.Thread(target=doLog, args=(len(threads),)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    test()
