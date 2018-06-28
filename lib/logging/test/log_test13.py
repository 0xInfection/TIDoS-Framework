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
A test harness for the logging module. Implements a SOAPHandler class which
can be used to form the basis of extended SOAP functionality.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""
import string, logging, logging.handlers, types

SOAP_MESSAGE = """<SOAP-ENV:Envelope
    xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:logging="http://www.red-dove.com/logging"
    SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"
>
    <SOAP-ENV:Body>
        <logging:log>
%s
        </logging:log>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

class SOAPHandler(logging.Handler):
    """
    A class which sends records to a SOAP server.
    """
    def __init__(self, host, url):
        """
        Initialize the instance with the host and the request URL
        """
        logging.Handler.__init__(self)
        self.host = host
        self.url = url

    def emit(self, record):
        """
        Send the record to the Web server as a SOAP message
        """
        try:
            import httplib
            h = httplib.HTTP(self.host)
            h.putrequest("POST", self.url)
            keys = record.__dict__.keys()
            keys.sort()
            args = ""
            for key in keys:
                v = record.__dict__[key]
                if type(v) == types.StringType:
                    t = "string"
                elif (type(v) == types.IntType) or (type(v) == types.LongType):
                    t = "integer"
                elif type(v) == types.FloatType:
                    t = "float"
                else:
                    t = "string"
                args = args + "%12s<logging:%s xsi:type=\"xsd:%s\">%s</logging:%s>\n" % ("",
                               key, t, str(v), key)
            data = SOAP_MESSAGE % args[:-1]
            h.putheader("Content-type", "text/plain; charset=\"utf-8\"")
            h.putheader("Content-length", str(len(data)))
            h.endheaders()
            #print data
            h.send(data)
            r = h.getreply()    #can't do anything with the result
            f = h.getfile()
            if f:
                #print f.read()
                f.close()
        except:
            self.handleError(record)

def main():
    sh = SOAPHandler('localhost:%d' % logging.handlers.DEFAULT_SOAP_LOGGING_PORT, '/log')
    logger = logging.getLogger("log_test13")
    logging.getLogger("").setLevel(logging.DEBUG)
    logger.propagate = 0
    logger.addHandler(sh)
    logger.info("Jackdaws love my big %s of %s", "sphinx", "quartz")
    logger.debug("Pack my %s with five dozen %s", "box", "liquor jugs")
    logger.removeHandler(sh)

if __name__ == "__main__":
    main()

