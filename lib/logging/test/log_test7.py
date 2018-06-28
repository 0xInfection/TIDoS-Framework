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
A test harness for the logging module. Tests MemoryHandler.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""
import sys, logging, logging.handlers

def message(s):
    sys.stderr.write("%s\n" % s)

sh = logging.StreamHandler()
mh = logging.handlers.MemoryHandler(10,logging.WARNING, sh)
logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
logger.addHandler(mh)
message("-- logging at DEBUG, nothing should be seen yet --")
logger.debug("Debug message")
message("-- logging at INFO, nothing should be seen yet --")
logger.info("Info message")
message("-- logging at WARNING, 3 messages should be seen --")
logger.warning("Warning message")
for i in xrange(102):
    message("-- logging %d at level INFO, messages should be seen every 10 events --" % i)
    logger.info("Info index = %d", i)
sh.close()
mh.close()
logger.removeHandler(mh)