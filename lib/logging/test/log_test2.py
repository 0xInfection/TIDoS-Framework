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
A test harness for the logging module. Tests logger levels and basic Formatter, and logging to
sockets.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""

import logging, logging.handlers, socket

msgcount = 0

def nextmessage():
    global msgcount
    rv = "Message %d" % msgcount
    msgcount = msgcount + 1
    return rv

def main():
    logging.basicConfig()
    logging.getLogger("").setLevel(logging.DEBUG)
    hdlr = logging.handlers.SocketHandler('localhost', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    if __name__ == "__main__":
        hdlr.setFormatter(logging.Formatter("%(asctime)s %(name)-19s %(levelname)-5s - %(message)s"))
    logging.getLogger("").addHandler(hdlr)
    ERR = logging.getLogger("ERR")
    ERR.setLevel(logging.ERROR)
    INF = logging.getLogger("INF")
    INF.setLevel(logging.INFO)
    INF_ERR  = logging.getLogger("INF.ERR")
    INF_ERR.setLevel(logging.ERROR)
    DEB = logging.getLogger("DEB")
    DEB.setLevel(logging.DEBUG)

    INF_UNDEF = logging.getLogger("INF.UNDEF")
    INF_ERR_UNDEF = logging.getLogger("INF.ERR.UNDEF")
    UNDEF = logging.getLogger("UNDEF")

    GRANDCHILD = logging.getLogger("INF.BADPARENT.UNDEF")
    CHILD = logging.getLogger("INF.BADPARENT")

    #These should log
    ERR.log(logging.CRITICAL, nextmessage())
    ERR.error(nextmessage())

    INF.log(logging.CRITICAL, nextmessage())
    INF.error(nextmessage())
    INF.warning(nextmessage())
    INF.info(nextmessage())

    INF_UNDEF.log(logging.CRITICAL, nextmessage())
    INF_UNDEF.error(nextmessage())
    INF_UNDEF.warning(nextmessage())
    INF_UNDEF.info(nextmessage())

    INF_ERR.log(logging.CRITICAL, nextmessage())
    INF_ERR.error(nextmessage())

    INF_ERR_UNDEF.log(logging.CRITICAL, nextmessage())
    INF_ERR_UNDEF.error(nextmessage())

    DEB.log(logging.CRITICAL, nextmessage())
    DEB.error(nextmessage())
    DEB.warning(nextmessage())
    DEB.info(nextmessage())
    DEB.debug(nextmessage())

    UNDEF.log(logging.CRITICAL, nextmessage())
    UNDEF.error(nextmessage())
    UNDEF.warning(nextmessage())
    UNDEF.info(nextmessage())

    GRANDCHILD.log(logging.CRITICAL, nextmessage())
    CHILD.log(logging.CRITICAL, nextmessage())

    #These should not log
    ERR.warning(nextmessage())
    ERR.info(nextmessage())
    ERR.debug(nextmessage())

    INF.debug(nextmessage())
    INF_UNDEF.debug(nextmessage())

    INF_ERR.warning(nextmessage())
    INF_ERR.info(nextmessage())
    INF_ERR.debug(nextmessage())
    INF_ERR_UNDEF.warning(nextmessage())
    INF_ERR_UNDEF.info(nextmessage())
    INF_ERR_UNDEF.debug(nextmessage())

    INF.info("Messages should bear numbers 0 through 24.")
    hdlr.close()
    logging.getLogger("").removeHandler(hdlr)

if __name__ == "__main__":
    try:
        main()
    except socket.error:
        print "\nA socket error occurred. Ensure that logrecv.py is running to receive logging requests from this script."
