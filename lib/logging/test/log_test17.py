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

To use as a server, run with no arguments in one process.
To use as a client, run with arguments "-client <filename>" where <filename>
is the name of a file containing a logging configuration.
The example files debug.ini, warn.ini, error.ini and critical.ini are
provided to use in the test. They each have a customized message format
(prefixed with their name) and the loggers have their levels set to the
value implied by their name.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""

import sys, logging, logging.config, thread, threading, random, time, struct

NUM_THREADS = 10
LOOP_COUNT = 10

CONFIG_PORT = 9077

logging.raiseExceptions = 1

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
    logger.setLevel(logging.DEBUG)
    logger.info("*** thread %s started (%d)", thread.get_ident(), num)
    for i in xrange(LOOP_COUNT):
        logger = logging.getLogger(random.choice(LOG_NAMES))
        a = random.choice(LOG_MESSAGES)
        args = a[0:2] + (num,) + a[2:]
        time.sleep(random.random() * 3)
        apply(logger.log, args)

def runserver():
    f = logging.Formatter("%(asctime)s %(levelname)-9s %(name)-8s %(thread)5s %(message)s")
    root = logging.getLogger('')
    h = logging.StreamHandler()
    root.addHandler(h)
    h.setFormatter(f)
    threads = []
    for i in xrange(NUM_THREADS):
        threads.append(threading.Thread(target=doLog, args=(len(threads),)))
    threads.append(logging.config.listen(CONFIG_PORT))    #don't use default port
    for t in threads:
        t.start()
    for t in threads[:-1]:
        t.join()
    logging.config.stopListening()
    threads[-1].join()

def runclient(fname):
    import socket

    print "configuring with '%s'" % fname
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', CONFIG_PORT))
    f = open(fname, "r")
    s = f.read()
    f.close()
    slen = struct.pack(">L", len(s))
    s = slen + s
    sentsofar = 0
    left = len(s)
    while left > 0:
        sent = sock.send(s[sentsofar:])
        sentsofar = sentsofar + sent
        left = left - sent
    sock.close()

if __name__ == "__main__":
    if "-client" not in sys.argv:
        runserver()
    else:
        sys.argv.remove("-client")
        if len(sys.argv) > 1:
            fname = sys.argv[1]
        else:
            fname = "warn.ini"
        runclient(fname)