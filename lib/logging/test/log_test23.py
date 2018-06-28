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
"""Test harness for the logging module. Demonstrates the use of basicConfig()

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""

import logging, tempfile, os

def do_logging(logger):
    logger.debug("We have a thorny problem")
    logger.info("We have an interesting problem")
    logger.warning("We have a bit of a problem")
    logger.error("We have a major problem")
    logger.critical("We have an unmitigated disaster")
    print "=" * 70

def main():
    td = tempfile.gettempdir()
    logger = logging.getLogger()
    logging.basicConfig()
    do_logging(logger)
    logger.removeHandler(logger.handlers[0])
    logging.basicConfig(level=logging.DEBUG)
    do_logging(logger)
    logger.removeHandler(logger.handlers[0])
    logging.basicConfig(level=logging.CRITICAL)
    do_logging(logger)
    logger.removeHandler(logger.handlers[0])
    logging.basicConfig(level=logging.WARNING, filename=os.path.join(td, "test.log"), filemode="w")
    do_logging(logger)
    h = logger.handlers[0]
    h.close()
    logger.removeHandler(h)
    logging.basicConfig(level=logging.INFO, stream=open(os.path.join(td, "test.log"), "a"), format="%(asctime)s %(name)s %(levelname)-8s %(message)s")
    do_logging(logger)

if __name__ == "__main__":
    main()
