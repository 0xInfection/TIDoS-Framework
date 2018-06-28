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
A test harness for the logging module. An example handler - DBHandler -
which writes to an Python DB API 2.0 data source. You'll need to set this
source up before you run the test.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""
import sys, string, time, logging

class DBHandler(logging.Handler):
    def __init__(self, dsn, uid='', pwd=''):
        logging.Handler.__init__(self)
        import mx.ODBC.Windows
        self.dsn = dsn
        self.uid = uid
        self.pwd = pwd
        self.conn = mx.ODBC.Windows.connect(self.dsn, self.uid, self.pwd)
        self.SQL = """INSERT INTO Events (
                        Created,
                        RelativeCreated,
                        Name,
                        LogLevel,
                        LevelText,
                        Message,
                        Filename,
                        Pathname,
                        Lineno,
                        Milliseconds,
                        Exception,
                        Thread
                   )
                   VALUES (
                        %(dbtime)s,
                        %(relativeCreated)d,
                        '%(name)s',
                        %(levelno)d,
                        '%(levelname)s',
                        '%(message)s',
                        '%(filename)s',
                        '%(pathname)s',
                        %(lineno)d,
                        %(msecs)d,
                        '%(exc_text)s',
                        '%(thread)s'
                   );
                   """
        self.cursor = self.conn.cursor()

    def formatDBTime(self, record):
        record.dbtime = time.strftime("#%m/%d/%Y#", time.localtime(record.created))

    def emit(self, record):
        try:
            #use default formatting
            self.format(record)
            #now set the database time up
            self.formatDBTime(record)
            if record.exc_info:
                record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
            else:
                record.exc_text = ""
            sql = self.SQL % record.__dict__
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            import traceback
            ei = sys.exc_info()
            traceback.print_exception(ei[0], ei[1], ei[2], None, sys.stderr)
            del ei

    def close(self):
        self.cursor.close()
        self.conn.close()
        logging.Handler.close(self)

dh = DBHandler('Logging')
logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
logger.addHandler(dh)
logger.info("Jackdaws love my big %s of %s", "sphinx", "quartz")
logger.debug("Pack my %s with five dozen %s", "box", "liquor jugs")
try:
    import math
    math.exp(1000)
except:
    logger.exception("Problem with %s", "math.exp")
logging.shutdown()
