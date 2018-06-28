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
A test harness for the logging module. Tests new fileConfig (not yet a complete test).

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""
import logging, logging.config

def doLog(logger):
    logger.debug("Debug")
    logger.info("Info")
    logger.warning("Warning")
    logger.error("Error")
    logger.critical("Critical")

def main():
    logging.config.fileConfig("log_test3.ini")
    logger = logging.getLogger(None)
    print "---------------------------------------------------"
    print "-- Logging to root; messages appear on console only"
    print "---------------------------------------------------"
    doLog(logger)
    print "----------------------------------------------------------------------"
    print "-- Logging to log02; messages appear on console and in file python.log"
    print "----------------------------------------------------------------------"
    logger = logging.getLogger("log02")
    doLog(logger)
    print "--------------------------------------------------------------------------"
    print "-- Logging to log02.log03; messages appear on console, in file python.log,"
    print "-- and at logrecv.py tcp (if running. <= DEBUG messages will not appear)."
    print "--------------------------------------------------------------------------"
    logger = logging.getLogger("log02.log03")
    doLog(logger)
    print "-----------------------------------------------------------------------"
    print "-- Logging to log02.log03.log04; messages appear only at logrecv.py udp"
    print "-- (if running. <= INFO messages will not appear)."
    print "-----------------------------------------------------------------------"
    logger = logging.getLogger("log02.log03.log04")
    doLog(logger)
    print "--------------------------------------------------------------------"
    print "-- Logging to log02.log03.log04.log05.log06; messages appear at"
    print "-- logrecv.py udp (if running. < CRITICAL messages will not appear)."
    print "--------------------------------------------------------------------"
    logger = logging.getLogger("log02.log03.log04.log05.log06")
    doLog(logger)
    print "-- All done."
    logging.shutdown()

if __name__ == "__main__":
    main()