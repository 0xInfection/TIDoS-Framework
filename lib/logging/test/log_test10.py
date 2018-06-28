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
"""Test harness for the logging module. Shows use of a user-defined Logger subclass.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""
import sys
import locale

locale.setlocale(locale.LC_ALL, '')

from logging import *

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(message)s"
DATE_FORMAT = "%x %X"

class MyLogger(Logger):
    """
    A simple example of a logger extension.
    """
    def debug(self, msg, *args, **kwargs):
        """
        This overridden method passes exception information for DEBUG level calls
        """
        if self.manager.disable >= DEBUG:
            return
        if DEBUG >= self.getEffectiveLevel():
            exc_info = kwargs.get("exc_info", 0)
            ei = None
            if exc_info:
                ei = sys.exc_info()
                if not ei[1]:
                    ei = None
            self._log(DEBUG, msg, args, ei)
            del ei

class NotALogger:
    pass

def config():
    try:
        setLoggerClass(NotALogger)
    except Exception, e:
        sys.stderr.write("%s\n" % e)
    setLoggerClass(MyLogger)
    if __name__ == "__main__":
        basicConfig()
    if __name__ == "__main__":
        getLogger("").handlers[0].setFormatter(Formatter(LOG_FORMAT, DATE_FORMAT))

def run():
    getLogger("").setLevel(DEBUG)
    logger = getLogger("mylogger")
    logger.info("Starting...")
    logger.debug("Debug message not in exception handler (no traceback)")
    logger.info("About to throw exception...")
    try:
        print "7" + 4
    except Exception, e:
        logger.debug("Debug message inside exception handler (traceback)",exc_info=1)
    logger.info("Done.")

def main():
    config()
    run()

if __name__ == "__main__":
    main()
