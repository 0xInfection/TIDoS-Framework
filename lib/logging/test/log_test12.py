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
A test harness for the logging module. Tests HTTPHandler.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""
import sys, string, logging, logging.handlers

def main():
    import pdb
    host = "localhost:%d" % logging.handlers.DEFAULT_HTTP_LOGGING_PORT
    gh = logging.handlers.HTTPHandler(host, '/log', 'GET')
    ph = logging.handlers.HTTPHandler(host, '/log', 'POST')
    logger = logging.getLogger("log_test12")
    logger.propagate = 0
    logger.addHandler(gh)
    logger.addHandler(ph)
    logging.getLogger("").setLevel(logging.DEBUG)
    logger.info("Jackdaws love my big %s of %s", "sphinx", "quartz")
    logger.debug("Pack my %s with twelve dozen %s", "box", "liquor jugs")
    gh.close()
    ph.close()
    logger.removeHandler(gh)
    logger.removeHandler(ph)

if __name__ == "__main__":
    main()
