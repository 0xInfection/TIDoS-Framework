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
A test harness for the logging module. Tests BufferingHandler, BufferingFormatter.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""
import logging, logging.handlers

class XMLFormatter(logging.BufferingFormatter):
        """
        A formatter which formats a set of records using XML, using an example DTD called "logging.dtd".
        """
        def __init__(self):
            fmtstr = """
    <event name="%(name)s" level="%(levelno)d" filename="%(filename)s" lineno="%(lineno)d">
    <message>%(message)s</message>
    </event>"""
            logging.BufferingFormatter.__init__(self, logging.Formatter(fmtstr))

#   def formatHeader(self, records):
#       return """
#<?xml version="1.0" ?><!DOCTYPE eventSet SYSTEM "logging.dtd">
#<eventSet xmlns="http://www.red-dove.com/logging">"""
#
#   def formatFooter(self, records):
#       return "</eventSet>"

class XMLHandler(logging.handlers.BufferingHandler):
    def __init__(self, capacity):
        logging.handlers.BufferingHandler.__init__(self, capacity)
        self.setFormatter(XMLFormatter())

    def flush(self):
        if len(self.buffer) > 0:
            file = open("events.xml","w")
            file.write(self.formatter.format(self.buffer))
            file.close()
            self.buffer = []

def main():
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    xh = XMLHandler(10)
    logger.addHandler(xh)
    for i in xrange(100):
        logger.info("Info index = %d", i)
    xh.close()
    logger.removeHandler(xh)

if __name__ == "__main__":
    main()
