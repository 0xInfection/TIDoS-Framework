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
"""Test harness for the logging module. A test showing exception handling and use of SysLogHandler.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""
import sys, logging
import syslog

class SLHandler(logging.Handler):
    def __init__(self, ident, logopt=0, facility=syslog.LOG_USER):
        logging.Handler.__init__(self)
        self.ident = ident
        self.logopt = logopt
        self.facility = facility
        self.mappings = {
            logging.DEBUG: syslog.LOG_DEBUG,
            logging.INFO: syslog.LOG_INFO,
            logging.WARNING: syslog.LOG_WARNING,
            logging.ERROR: syslog.LOG_ERR,
            logging.CRITICAL: syslog.LOG_CRIT,
            }

    def encodeLevel(self, level):
        return self.mappings.get(level, syslog.LOG_INFO)

    def emit(self, record):
        syslog.openlog(self.ident, self.logopt, self.facility)
        msg = self.format(record)
        prio = self.encodeLevel(record.levelno)
        syslog.syslog(prio, msg)
        syslog.closelog()

def config():
    logging.basicConfig()
    logging.getLogger("").setLevel(logging.DEBUG)
    if __name__ == "__main__":
        fmt = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(levelname)-5s - %(message)s")
        hdlr = logging.FileHandler("tmp.tmp")
        hdlr.setFormatter(fmt)
        logging.getLogger("").addHandler(hdlr)
    else:
        fmt = None
    hdlr = SLHandler("log_test1")
    if fmt:
        hdlr.setFormatter(fmt)
    logging.getLogger("").addHandler(hdlr)
    return hdlr

def run():
    logging.info("Starting...")
    try:
        print "7" + 4
    except Exception, e:
        logging.error("Problem %s (%d)", "ERROR", logging.ERROR, exc_info=1)
        logging.debug("Problem %s (%d)", "DEBUG", logging.DEBUG, exc_info=1)
    logging.info("Done.")


def main():
    hdlr = config()
    run()
    logging.getLogger("").removeHandler(hdlr)

if __name__ == "__main__":
    main()
