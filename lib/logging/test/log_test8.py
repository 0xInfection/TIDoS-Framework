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
A test harness for the logging module. Tests RotatingFileHandler.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""
import logging, logging.handlers
import locale

locale.setlocale(locale.LC_ALL, '')

sequence = 0

def doLog(logger):
    global sequence
    sequence = sequence + 1
    logger.debug("%6d This message should be at level %d - %s", sequence,\
                logging.DEBUG, logging.getLevelName(logging.DEBUG))
    sequence = sequence + 1
    logger.info("%6d This message should be at level %d - %s", sequence,
                logging.INFO, logging.getLevelName(logging.INFO))
    sequence = sequence + 1
    logger.warning("%6d This message should be at level %d - %s", sequence,\
                logging.WARNING, logging.getLevelName(logging.WARNING))
    sequence = sequence + 1
    logger.error("%6d This message should be at level %d - %s", sequence,\
                logging.ERROR, logging.getLevelName(logging.ERROR))
    sequence = sequence + 1
    logger.critical("%6d This message should be at level %d - %s", sequence,\
                logging.CRITICAL, logging.getLevelName(logging.CRITICAL))

def main():
    logger = logging.getLogger("")  #root logger
    logger.setLevel(logging.DEBUG)
    logging.raiseExceptions = 0
    if __name__ == "__main__":
        logname = "rollover.log"
    else:
        logname = "log_test_rollover.log"
    hdlr = logging.handlers.RotatingFileHandler(logname, "a", 5000, 3)
    if __name__ == "__main__":
       fmt = logging.Formatter("%(asctime)s %(levelname)-5s %(message)s", "%x %X")
       hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)
    for i in xrange(100):
        doLog(logger)
    logger.removeHandler(hdlr)

if __name__ == "__main__":
    main()