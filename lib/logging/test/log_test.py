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
"""Test harness for the logging module. Run all tests.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""

import os, sys, logging, threading, time

BANNER = "-- %-10s %-6s --------------------------------------------------------\n"

def banner(nm, typ):
    sep = BANNER % (nm, typ)
    sys.stdout.write(sep)
    sys.stdout.flush()
    sys.stderr.write(sep)
    sys.stderr.flush()

def main():
    oldout = sys.stdout
    olderr = sys.stderr
    sys.stdout = open("stdout.log", "w")
    sys.stderr = open("stderr.log", "w")
    logging.basicConfig()
    root = logging.getLogger("")
    hdlr0 = root.handlers[0]
    #Set up servers
    import logrecv
    threads = []
    tcpserver = logrecv.LogRecordSocketReceiver()
    tcpserver.logname = ""
    threads.append(threading.Thread(target=logrecv.runTCP, args=(tcpserver,)))
    udpserver = logrecv.LogRecordDatagramReceiver()
    udpserver.logname = ""
    threads.append(threading.Thread(target=logrecv.runUDP, args=(udpserver,)))
    httpserver = logrecv.LogRecordHTTPReceiver()
    httpserver.logname = ""
    threads.append(threading.Thread(target=logrecv.runHTTP, args=(httpserver,)))
    soapserver = None
    if logrecv.SOAPServer:
        soapserver = logrecv.SOAPServer()
        soapserver.modules = (sys.modules["logrecv"],)
        soapserver.logname = ""
        threads.append(threading.Thread(target=logrecv.runSOAP, args=(soapserver,)))

    for thread in threads:
        thread.start()
    try:
        import log_test0
        banner("log_test0", "begin")
        log_test0.main()
        banner("log_test0", "end")
        try:
            import log_test1
            banner("log_test1", "begin")
            log_test1.main()
            banner("log_test1", "end")
        except ImportError:
            pass

        import log_test2
        banner("log_test2", "begin")
        log_test2.main()
        banner("log_test2", "end")
        time.sleep(3)

        #Skip 3 as it tests fileConfig

        banner("log_test4", "begin")
        import log_test4
        banner("log_test4", "end")

        #Skip 5 as it tests SMTPHandler, can't easily check results automatically

        #Skip 6 as it tests NTEventLogHandler, can't easily check results automatically

        banner("log_test7", "begin")
        root.removeHandler(hdlr0)
        import log_test7
        root.addHandler(hdlr0)
        banner("log_test7", "end")

        banner("log_test8", "begin")
        import log_test8
        root.removeHandler(hdlr0)
        log_test8.main()
        root.addHandler(hdlr0)
        banner("log_test8", "end")

        banner("log_test9", "begin")
        import log_test9
        root.removeHandler(hdlr0)
        log_test9.main()
        root.addHandler(hdlr0)
        banner("log_test9", "end")

        banner("log_test10", "begin")
        import log_test10
        log_test10.main()
        banner("log_test10", "end")

        #Skip 11 as it tests SMTPHandler, can't easily check results automatically

        import log_test12
        banner("log_test12", "begin")
        log_test12.main()
        banner("log_test12", "end")

        import log_test13
        banner("log_test13", "begin")
        log_test13.main()
        banner("log_test13", "end")

        import log_test15
        banner("log_test15", "begin")
        log_test15.test(log_test15.FILTER)
        banner("log_test15", "end")

        time.sleep(3)

    finally:
        #shut down servers
        olderr.write("Tidying up...")
        tcpserver.abort = 1
        udpserver.abort = 1
        httpserver.abort = 1
        if soapserver:
            soapserver.abort = 1
        for thread in threads:
            thread.join()
        sys.stdout.close()
        sys.stdout = oldout
        #don't close this, as hdlr0 references it. hdlr0 will be closed at application exit
        #sys.stderr.close()
        sys.stderr = olderr
        print "Test run completed."

if __name__ == "__main__":
    main()
