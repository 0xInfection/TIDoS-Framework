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
A test harness for the logging module. Tests TimedRotatingFileHandler.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""
import logging, logging.handlers
import locale, time

locale.setlocale(locale.LC_ALL, '')

sequence = 0

def doLog(logger):
    global sequence
    sequence = sequence + 1
    #logger.debug("%6d This message should be at level %d - %s", sequence,\
    #            logging.DEBUG, logging.getLevelName(logging.DEBUG))
    #sequence = sequence + 1
    #logger.info("%6d This message should be at level %d - %s", sequence,
    #            logging.INFO, logging.getLevelName(logging.INFO))
    #sequence = sequence + 1
    #logger.warning("%6d This message should be at level %d - %s", sequence,\
    #            logging.WARNING, logging.getLevelName(logging.WARNING))
    #sequence = sequence + 1
    #logger.error("%6d This message should be at level %d - %s", sequence,\
    #            logging.ERROR, logging.getLevelName(logging.ERROR))
    #sequence = sequence + 1
    logger.critical("%6d This message should be at level %d - %s", sequence,\
                logging.CRITICAL, logging.getLevelName(logging.CRITICAL))

def main():
    logger = logging.getLogger("")  #root logger
    logger.setLevel(logging.DEBUG)
    if __name__ == "__main__":
        prefix = ""
    else:
        prefix = "log_test_"
    h1 = logging.handlers.TimedRotatingFileHandler(prefix + "secs.log", "s", 1, 10)
    h2 = logging.handlers.TimedRotatingFileHandler(prefix + "mins.log", "m", 1, 10)
    h3 = logging.handlers.TimedRotatingFileHandler(prefix + "hours.log", "h", 1, 10)
    h4 = logging.handlers.TimedRotatingFileHandler(prefix + "days.log", "d", 1, 10)
    h5 = logging.handlers.TimedRotatingFileHandler(prefix + "midn.log", "midnight", 1, 3)
    if __name__ == "__main__":
       fmt = logging.Formatter("%(asctime)s %(levelname)-5s %(message)s", "%x %X")
       h1.setFormatter(fmt)
       h2.setFormatter(fmt)
       h3.setFormatter(fmt)
       h4.setFormatter(fmt)
       h5.setFormatter(fmt)
    logger.addHandler(h1)
    logger.addHandler(h2)
    logger.addHandler(h3)
    logger.addHandler(h4)
    logger.addHandler(h5)
    for i in xrange(100000):
        doLog(logger)
        time.sleep(10)
    logger.removeHandler(h1)

if __name__ == "__main__":
    main()