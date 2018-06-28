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
A test harness for the logging module. Tests SMTPHandler.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""
import logging, logging.handlers

MAILHOST = 'beta'
FROM     = 'log_test5@yourdomain.com'
TO       = ['arkadi_renko']
SUBJECT  = 'Test Logging email from Python logging module (non-buffering)'

def main():
    log = logging.getLogger("")
    log.setLevel(logging.DEBUG)
    hdlr = logging.handlers.SMTPHandler(MAILHOST, FROM, TO, SUBJECT)
    hdlr.setFormatter(logging.Formatter("%(asctime)s %(levelname)-5s %(message)s"))
    log.addHandler(hdlr)
    log.info("Test email contents")
    log.removeHandler(hdlr)

if __name__ == "__main__":
    main()