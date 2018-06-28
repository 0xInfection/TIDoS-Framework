#! /usr/bin/env python
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

Simple socket-based logging event receiver for use with "logging.py" logging
module.

Should work under Python versions >= 1.5.2, except that source line information
is not available unless 'sys._getframe()' is.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""

from select import select
import sys, string, struct, types, cPickle, socket
import logging, logging.handlers, logging.config

TIMEOUT         = 10
if sys.platform == "win32":
    RESET_ERROR = 10054
else:
    RESET_ERROR = 0 #FIXME get correct value for Unix...

logging.raiseExceptions = 1

#
# TCP receiver
#

from SocketServer import ThreadingTCPServer, StreamRequestHandler

class LogRecordStreamHandler(StreamRequestHandler):
    """
    Handler for a streaming logging request. It basically logs the record
    using whatever logging policy is configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while 1:
            try:
                chunk = self.connection.recv(4)
                if len(chunk) < 4:
                    break
                slen = struct.unpack(">L", chunk)[0]
                chunk = self.connection.recv(slen)
                while len(chunk) < slen:
                    chunk = chunk + self.connection.recv(slen - len(chunk))
                obj = self.unPickle(chunk)
                record = logging.makeLogRecord(obj)
                self.handleLogRecord(record)
            except socket.error, e:
                if type(e.args) != types.TupleType:
                    raise
                else:
                    errcode = e.args[0]
                    if errcode != RESET_ERROR:
                        raise
                    break

    def unPickle(self, data):
        return cPickle.loads(data)

    def handleLogRecord(self, record):
        #if a name is specified, we use the named logger rather than the one
        #implied by the record. This is so test harnesses don't get into
        #endless loops (particularly log_test.py, which has this code and the
        #client code in the same Python instance)
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        logger.handle(record)

class LogRecordSocketReceiver(ThreadingTCPServer):
    """
    A simple-minded TCP socket-based logging receiver suitable for test
    purposes.
    """

    allow_reuse_address = 1

    def __init__(self, host='localhost', port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
            handler=LogRecordStreamHandler):
        ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

#
# UDP receiver
#

from SocketServer import ThreadingUDPServer, DatagramRequestHandler

class LogRecordDatagramHandler(DatagramRequestHandler):
    """
    Handler for a datagram logging request. It basically logs the record using
    whatever logging policy is configured locally.
    """
    def handle(self):
        chunk = self.packet
        slen = struct.unpack(">L", chunk[:4])[0]
        chunk = chunk[4:]
        assert len(chunk) == slen
        obj = self.unPickle(chunk)
        record = logging.LogRecord(None, None, "", 0, "", (), None)
        record.__dict__.update(obj)
        self.handleLogRecord(record)

    def unPickle(self, data):
        return cPickle.loads(data)

    def handleLogRecord(self, record):
        #if a name is specified, we use the named logger rather than the one
        #implied by the record. This is so test harnesses don't get into
        #endless loops (particularly log_test.py, which has this code and the
        #client code in the same Python instance)
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        logger.handle(record)

    def finish(self):
        pass

class LogRecordDatagramReceiver(ThreadingUDPServer):
    """
    A simple-minded UDP datagram-based logging receiver suitable for test
    purposes.
    """

    allow_reuse_address = 1

    def __init__(self, host='localhost', port=logging.handlers.DEFAULT_UDP_LOGGING_PORT,
            handler=LogRecordDatagramHandler):
        ThreadingUDPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

#
# HTTP receiver
#

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

import cgi

class LogRecordHTTPHandler(BaseHTTPRequestHandler):
    def makeDict(self, fs):
        dict = {}
        for mfs in fs.list:
            dict[mfs.name] = mfs.value
        for key in ["args", "exc_info", "exc_text", "lineno", "msecs", "created",
                    "thread", "levelno", "relativeCreated"]:
            if dict.has_key(key):
                dict[key] = eval(dict[key])
        return dict

    def do_GET(self):
        """Serve a GET request."""
        sts = "OK"
        env = { 'REQUEST_METHOD' : 'GET'}
        try:
            i = string.find(self.path, '?')
            if i >= 0:
                env['QUERY_STRING'] = self.path[i + 1:]
            fs = cgi.FieldStorage(environ=env)
            dict = self.makeDict(fs)
            record = logging.LogRecord(None, None, "", 0, "", (), None)
            record.__dict__.update(dict)
            self.handleLogRecord(record)
        except Exception, e:
            sts = "ERROR"
            raise
        self.send_head()
        self.wfile.write("GET %s" % sts)

    def handleLogRecord(self, record):
        #if a name is specified, we use the named logger rather than the one
        #implied by the record. This is so test harnesses don't get into
        #endless loops (particularly log_test.py, which has this code and the
        #client code in the same Python instance)
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        logger.handle(record)

    def do_HEAD(self):
        """Serve a HEAD request."""
        self.send_head()

    def do_POST(self):
        """Serve a POST request."""
        sts = "OK"
        env = { 'REQUEST_METHOD' : 'POST'}
        try:
            length = self.headers.getheader('content-length')
            if length:
                env['CONTENT_LENGTH'] = length
            #print self.headers
            i = string.find(self.path, '?')
            if i >= 0:
                env['QUERY_STRING'] = self.path[i + 1:]
            fs = cgi.FieldStorage(fp=self.rfile, environ=env)
            dict = self.makeDict(fs)
            record = logging.LogRecord(None, None, "", 0, "", (), None)
            record.__dict__.update(dict)
            self.handleLogRecord(record)
        except Exception, e:
            print e
            sys.stdout.flush()
            sts = "ERROR"
            raise
        self.send_head()
        self.wfile.write("POST %s" % sts)

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

    def log_message(self, *args):
        #comment out the following line if you don't want to show requests
        #apply(BaseHTTPRequestHandler.log_message, (self,) + args)
        pass

class LogRecordHTTPReceiver(HTTPServer):
    def __init__(self, host='localhost', port=logging.handlers.DEFAULT_HTTP_LOGGING_PORT,
            handler=LogRecordHTTPHandler):
        HTTPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort


#
# SOAP receiver
#

try:
    from ZSI import dispatch

    logname = None

    def log(args, created, exc_info, exc_text, filename, levelname, levelno, lineno, module, msecs, msg, name, pathname, process, relativeCreated, thread):
        record = logging.LogRecord(None, None, "", 0, "", (), None)
        record.args = eval(args)
        record.exc_info = eval(exc_info)
        record.exc_text = eval(exc_text)
        record.created = created
        record.filename = filename
        record.module = module
        record.levelname = levelname
        record.lineno = lineno
        record.levelno = levelno
        record.msecs = msecs
        record.msg = msg
        record.name = name
        record.pathname = pathname
        record.process = process
        record.relativeCreated = relativeCreated
        record.thread = thread
        #if a name is specified, we use the named logger rather than the one
        #implied by the record. This is so test harnesses don't get into
        #endless loops (particularly log_test.py, which has this code and the
        #client code in the same Python instance)
        if logname is not None:
            lname = logname
        else:
            lname = name
        logger = logging.getLogger(lname)
        logger.handle(record)

    class MySOAPRequestHandler(dispatch.SOAPRequestHandler):
        def log_message(self, *args):
            #comment out the following line if you don't want to show requests
            #apply(BaseHTTPRequestHandler.log_message, (self,) + args)
            pass

    class SOAPServer(HTTPServer):
        def __init__(self, port=logging.handlers.DEFAULT_SOAP_LOGGING_PORT):
            address = ('', port)
            HTTPServer.__init__(self, address, MySOAPRequestHandler)
            self.abort = 0
            self.timeout = 1
            self.logname = None
            self.docstyle = 0
            self.nsdict = {}
            self.typesmodule = None
            self.rpc = 1
            self.modules = (sys.modules["__main__"],)

        def serve_until_stopped(self):
            import select
            abort = 0
            while not abort:
                rd, wr, ex = select.select([self.socket.fileno()],
                                           [], [],
                                           self.timeout)
                if rd:
                    global logname
                    logname = self.logname
                    self.handle_request()
                abort = self.abort

except ImportError:
    "Import failed"
    SOAPServer = None

def runTCP(tcpserver=None):
    if not tcpserver:
        tcpserver = LogRecordSocketReceiver()
    print "About to start TCP server..."
    tcpserver.serve_until_stopped()

def runUDP(udpserver=None):
    if not udpserver:
        udpserver = LogRecordDatagramReceiver()
    print "About to start UDP server..."
    udpserver.serve_until_stopped()

def runHTTP(httpserver=None):
    if not httpserver:
        httpserver = LogRecordHTTPReceiver()
    print "About to start HTTP server..."
    httpserver.serve_until_stopped()

def runSOAP(soapserver=None):
    if not SOAPServer:
        print "Sorry, ZSI is not available. Install PyXML-0.6.6 and ZSI first."
        print "See README.txt and python_logging.html for more information."
    else:
        if not soapserver:
            soapserver = SOAPServer()
        print "About to start SOAP server..."
        soapserver.serve_until_stopped()

FORMAT_STR = "%(asctime)s %(name)-19s %(levelname)-5s - %(message)s"

if __name__ == "__main__":
    if (len(sys.argv) < 2) or not (string.lower(sys.argv[1]) in \
                                    ["udp", "tcp", "http", "soap"]):
        print "usage: logrecv.py [UDP|TCP|HTTP|SOAP]"
    else:
        #logging.basicConfig()
        logging.config.fileConfig("logrecv.ini")
#        both = string.lower(sys.argv[1]) == "both"
#        hdlr = logging.FileHandler("test.log")
#        hdlr.setFormatter(logging.Formatter(FORMAT_STR))
#        logging.getLogger("").addHandler(hdlr)
#        if both:
#            import threading
#            tcpthread = threading.Thread(target=runTCP)
#            udpthread = threading.Thread(target=runUDP)
#            tcpthread.start()
#            udpthread.start()
#            tcpthread.join()
#            udpthread.join()
#        else:
#            tcp = string.lower(sys.argv[1]) == "tcp"
#            if tcp:
#                runTCP()
#            else:
#                runUDP()
        arg = string.lower(sys.argv[1])
        if arg == "tcp":
            runTCP()
        elif arg == "udp":
            runUDP()
        elif arg == "http":
            runHTTP()
        elif arg == "soap":
            runSOAP()
