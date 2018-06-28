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
A test harness for the logging module. Tests NTEventLogHandler.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""
import logging, logging.handlers

def main():
    ntl = logging.handlers.NTEventLogHandler("Python Logging Test")
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ntl)
    logger.debug("This is a '%s' message", "Debug")
    logger.info("This is a '%s' message", "Info")
    logger.warning("This is a '%s' message", "Warning")
    logger.error("This is a '%s' message", "Error")
    logger.critical("This is a '%s' message", "Critical")
    try:
        x = 4 / 0
    except:
        logger.info("This is an %s (or should that be %s?)", "informational exception", "exceptional information", exc_info=1)
        logger.exception("This is the same stuff, via a %s", "exception() call")
    logger.removeHandler(ntl)

if __name__ == "__main__":
    main()