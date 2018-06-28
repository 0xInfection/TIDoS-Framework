This module is intended to provide error logging functionality for Python
programs. It is the reference implementation for Python Enhancement Proposal
(PEP) 282.

For more information on the package itself, see python_logging.html. In it,
there is a description of each file in the distribution.
You can also use pydoc to browse the interfaces.

Change History
--------------

Version   Date        Description
=============================================================================
0.4.9.6   02 Mar 2005 Improved error recovery for SysLogHandler
                      (thanks to Erik Forsberg for the patch).
                      Added optional encoding for file handlers, which
                      defaults to None. If specified, codecs.open() is used
                      for opening files.
                      Bugfixed stack frame detection logic error for 1.5.2.
-----------------------------------------------------------------------------
0.4.9.5   02 Oct 2004 Removed 1.5.2 incompatibility involving *=, +=
-----------------------------------------------------------------------------
0.4.9.4   22 Sep 2004 Added getLoggerClass() (thanks to Dave Wilson).
                      Added exception handling in shutdown().
                      Sort globbed files in doRollover() in
                      TimedRotatingFileHandler.
                      Date formatting for SMTPHandler now uses email package
                      where available.
                      fileConfig() exception handling added for handler
                      instantiation.
                      Minor documentation corrections.
-----------------------------------------------------------------------------
0.4.9.3   24 Aug 2004 Changed basicConfig() to add keyword arguments. Changes
                      are backward-compatible.
                      Refactored RotatingFileHandler to create a base class
                      for rotating handlers. Added TimedRotatingFileHandler
                      (thanks to Mark Davidson - minor changes have been made
                      to the patch he supplied).
                      Added error checking to log() to check that level is
                      an integer, and raise a TypeError if not (as long as
                      raiseExceptions is set).
                      Fixed a bug in DatagramHandler.send() (thanks to Mario
                      Aleppo and Enrico Sirola for pointing it out).
                      Minor documentation corrections.
-----------------------------------------------------------------------------
0.4.9.2   28 Feb 2004 Traceback text is now cached.
                      Tracebacks can be propagated across sockets as text.
                      Added makeLogRecord() to allow a LogRecord to be
                      created from a dictionary.
                      Closing a handler now removes it from the internal list
                      used by shutdown().
                      Made close() call flush() for handlers where this makes
                      sense (thanks to Jim Jewett).
                      The exc_info keyword parameter can be used to pass an
                      exception tuple as well as a flag indicating that the
                      current exception should be logged.
                      A shutdown hook is registered to call shutdown() on
                      application (Python) exit (thanks to Jim Jewett).
                      Removed redundant error check in setLoggerClass().
                      Added RESET_ERROR to logging.config.
                      SocketHandler now uses an exponential backoff strategy
                      (thanks to Robert Olson).
                      Minor documentation corrections.
-----------------------------------------------------------------------------
0.4.8     22 Apr 2003 Made _listener global in stopListening().
                      Made listen() correctly pass the specified port.
                      Removed some redundant imports in __init__.py.
                      Added the record being processed as a parameter to
                      handleError (thanks to Gordon den Otter for the idea).
                      Handler.handle returns the result of applying the
                      filter to the record (thanks to Gordon den Otter for
                      the idea).
                      Added a seek(0, 2) in RotatingFileHandler before the
                      tell() call. This is because under Windows, tell()
                      returns 0 until the first actual write (thanks to
                      Gordon den Otter for the patch).
                      Altered findCaller to not use inspect (thanks to
                      Jeremy Hylton for the patch).
                      Renamed warn and WARN to warning and WARNING. This may
                      break existing code, but the standard Python module
                      will use warning/WARNING rather than warn/WARN. The
                      fatal and FATAL synonyms for critical and CRITICAL
                      have also been removed.
                      Added defaultEncoding and some support for encoding
                      Unicode messages (thanks to Stéphane Bidoul for the
                      suggestion).
                      Added process ID to the list of LogRecord attributes.
                      Modified Logger.removeHandler so that it does not
                      close the handler on removal.
                      Modified SMTPHandler to treat a single "to address"
                      correctly (thanks to Anthony Baxter).
                      Modified SMTPHandler to add a date header to the SMTP
                      message (thanks to David Driver for the suggestion).
                      Modified HTTPHandler to factor out the mapping of
                      a LogRecord to a dictionary (thanks to Franz Glasner
                      for the patch).
-----------------------------------------------------------------------------
0.4.7     15 Nov 2002 Made into a package with three modules: __init__ (the
                      core code), handlers (all handlers other than
                      FileHandler and its bases) and config (all the config
                      stuff). Before doing this:
                      Updated docstrings to include a short line, then a
                      blank line, then more descriptive text.
                      Renamed 'lvl' to 'level' in various functions.
                      Changed FileHandler to use "a" and "w" instead of "a+"
                      and "w+".
                      Moved log file rotation functionality from FileHandler
                      to a new class RotatingFileHandler.
                      Improved docstring describing rollover.
                      Updated makePickle to use 4-byte length and struct
                      module, likewise logrecv.py. Also updated on-the-fly
                      config reader to use 4-byte length/struct module.
                      Altered ConfigParser test to look at 'readline' rather
                      than 'read'.
                      Added optional "defaults" argument to fileConfig, to
                      be passed to ConfigParser.
                      Renamed ALL to NOTSET to avoid confusion.
                      Commented out getRootLogger(), as obsolete.
                      To do regression testing, run log_test.py and compare
                      the created files stdout.log and stderr.log against
                      the files stdout.exp and stderr.exp. They should match
                      except fir a couple of exception messages which give
                      absolute file paths.
                      Updated python_logging.html to remove links to
                      logging_pydoc.html, which has been removed from the
                      distribution.
                      Changed default for raiseExceptions to 1.
-----------------------------------------------------------------------------
0.4.6     08 Jul 2002 Added raiseExceptions to allow conditional propagation
                      of exceptions which occur during handling.
                      Added converter to Formatter to allow use of any
                      function to convert time from seconds to a tuple. It
                      still defaults to time.localtime but now you can also
                      use time.gmtime.
                      Added log_test22.py to test the conversion feature.
                      Changed rootlogger default level to WARN - was DEBUG.
                      Updated some docstrings.
                      Moved import of threading to where thread is imported.
                      If either is unavailable, threading support is off.
                      Updated minor defects in python_logging.html.
                      Check to see if ConfigParser has readfp method; if it
                      does and an object with a 'read' method is passed in,
                      assumes a file-like object and uses readfp to read it
                      in.
-----------------------------------------------------------------------------
0.4.5     04 Jun 2002 Fixed bug which caused problem if no args to message
                      (suggested by Hye-Shik Chang).
                      Fixed bug in _fixupParents (thanks to Nicholas Veeser)
                      and added log_test19.py as a test case for this bug.
                      Added getMessage to LogRecord (code was moved here from
                      Formatter.format)
                      Applied str() to record.msg to allow arbitrary classes
                      to determine the formatting (as msg can now be a class
                      instance).
                      Table of Contents added to python_logging.html, the
                      section on Loggers updated, and the logconf.ini file
                      section annotated.
                      Added log_test20.py which demonstrates how to use
                      class instances to provide alternatives to numeric
                      severities as mechanisms for control of logging.
                      Added log_test21.py which builds on log_test20.py to
                      show how you can use a regular expression-based Filter
                      for flexible matching similar to e.g. Protomatter
                      Syslog, where you can filter on e.g. "a.*" or "*.b" or
                      "a.*.c".
                      _levelNames changed to contain reverse mappings as well
                      as forward mappings (leveltext->level as well as level
                      -> leveltext). The reverse mappings are used by
                      fileConfig().
                      fileConfig() now more forgiving of missing options in
                      .ini file - sensible defaults now used when some
                      options are absent. Also, eval() is used less when
                      interpreting .ini file contents - int() and dict lookup
                      are used in more places.
-----------------------------------------------------------------------------
0.4.4     02 May 2002 getEffectiveLevel() returns ALL instead of None when
                      nothing found. Modified references to level=0 to
                      level=ALL in a couple of places.
                      SocketHandler now inherits from Handler (it used to
                      inherit from StreamHandler, for no good reason).
                      getLock() renamed to createLock().
                      Docstring tidy-ups, and some tidying up of
                      DatagramHandler.
                      Factored out unpickling in logrecv.py.
                      Added log_test18.py to illustrate MatchFilter, which is
                      a general matching filter.
                      Improved FileHandler.doRollover() so that the base
                      file name is always the most recent, then .1, then .2
                      etc. up to the maximum backup count. Renamed formal
                      args and attributes used in rollover.
                      Changed LogRecord attributes lvl -> levelno, level ->
                      levelname (less ambiguity)
                      Formatter.format searches for "%(asctime)" rather than
                      "(asctime)"
                      Renamed _start_time to _startTime
                      Formatter.formatTime now returns the time
                      Altered logrecv.py to support stopping servers
                      programmatically
                      Added log_test.py as overall test harness
                      basicConfig() can now be safely called more than once
                      Modified test scripts to make it easier to call them
                      from log_test.py
                      Moved SOAPHandler from core to log_test13.py. It's not
                      general enough to be in the core; most production use
                      will have differing RPC signatures.
-----------------------------------------------------------------------------
0.4.3     14 Apr 2002 Bug fix one-off error message to go to sys.stderr
                      rather than sys.stdout.
                      logrecv.py fix TCP for busy network.
                      Thread safety - added locking to Handler and for shared
                      data in module, and log_test16.py to test it.
                      Added socket listener to allow on-the-fly configuration
                      and added log_test17.py to test it.
-----------------------------------------------------------------------------
0.4.2     11 Apr 2002 Bug fix fileConfig() - setup of MemoryHandler target
                      and errors when loggers have no handlers set or
                      handlers have no formatters set
                      logconf.py - seems to hang if window closed when combo
                      dropdown is showing - added code to close popup on exit
                      Some tweaks to _srcfile computation (normpath added)
                      findCaller() optimized, now a lot faster!
                      Logger.removeHandler now closes the handler before
                      removing it
                      fileConfig() removes existing handlers before adding
                      the new set, to avoid memory leakage when repeated
                      calls are made
                      Fixed logrecv.py bug which hogged CPU time when TCP
                      connection was closed from the client
                      Added log_test14.py to demonstrate/test a DBHandler
                      which writes logging records into an RDBMS using the
                      Python Database API 2.0 (to run, you need something
                      which supports this already installed - I tested with
                      mxODBC)
                      Made getLogger name argument optional - returns root
                      logger if omitted
                      Altered Filter to take a string initializer, filtering
                      a sub-hierarchy rooted at a particular point (idea from
                      Denis S. Otkidach).
                      Added log_test15.py to test Filter initializer
                      Minor docstring changes
-----------------------------------------------------------------------------
0.4.1     03 Apr 2002 Bug fix SMTPHandler - extra \r\n needed (Oleg Orlov)
                      Added BufferingHandler, BufferingFormatter
                      Renamed getChainedPriority to getEffectiveLevel
                      Removed Logger.getRoot as it is redundant
                      Added log_test9.py to test Buffering classes and
                      to show an XMLFormatter example.
                      Added setLoggerClass.
                      Added log_test10.py to test setLoggerClass, using an
                      example Logger-derived class which outputs exception
                      info even for DEBUG level logging calls
                      Added log_test11.py to test a buffering implementation
                      of SMTPHandler
                      Changed logging call implementation to allow keyword
                      arguments (Kevin Butler and others)
                      Changed default SysLogHandler implementation.
                      Renamed "additive" to "propagate" as it better
                      describes the attribute.
                      Added HTTPHandler.
                      Modified logrecv.py to remove "both" option and to add
                      "HTTP" and "SOAP" options (SOAP option needs you to
                      have PyXML-0.6.6 and ZSI installed - for logrecv.py
                      only, and not for the core logging module itself).
                      Added log_test12.py to test HTTPHandler.
                      Added log_test13.py to test SOAPHandler.
                      Formatted to Python source guidelines (spaces, indent
                      of 4, within 80 columns).
                      More method renamings (result of feedback) - _handle()
                      renamed to emit(), _logRecord() renamed to handle().
                      Renamed FATAL to CRITICAL (David Goodger), but left
                      fatal() and FATAL in (until PEP is changed)
                      Changed configuration file format to ConfigParser
                      format.
                      Factored filter application functionality out to a new
                      Filterer class. The isLoggable() method is renamed to
                      filter() in both Filter and Filterer classes.
                      Altered SMTPHandler __init__ to accept (host, port)
                      for the mail internet address.
                      Added GUI configurator which uses Tkinter and the new
                      configuration file format. (See logconf.py and an
                      example configuration file in logconf.ini)
                      Altered log_test3.py to test with the new file format.
-----------------------------------------------------------------------------
0.4       21 Mar 2002 Incorporated comments/patches from Ollie Rutherfurd:
                      -Added level filtering for handlers.
                      -Return root logger if no name specified in getLogger.
                      Incorporated comments from Greg Ward:
                      -Added distutils setup.py script.
                      Added formatter initialization in Handler.__init__.
                      Tidied up docstrings.
                      Added removeHandler to Logger.
                      Added removeFilter to Logger and Handler.
                      logrecv.py modified to keep connection alive until
                      client closes it.
                      SocketHandler modified to not reset connection after
                      each logging event.
                      Added shutdown function which closes open sockets
                      Renamed DEFAULT_LOGGING_PORT->DEFAULT_TCP_LOGGING_PORT
                      Added DEFAULT_UDP_LOGGING_PORT
                      Added log_test4.py (example of arbitrary levels)
                      Added addLevelName, changed behaviour of getLevelName
                      Fixed bugs in DatagramHandler
                      Added SMTPHandler implementation
                      Added log_test5.py to test SMTPHandler
                      Added SysLogHandler (contribution from Nicolas Untz
                      based on Sam Rushing's syslog.py)
                      Modified log_test1.py to add a SysLogHandler
                      Added rollover functionality to FileHandler
                      Added NTEventLogHandler (based on Win32 extensions)
                      Added MemoryHandler implementation
                      Added log_test7.py to test MemoryHandler
                      Added log_test8.py to test FileHandler rollover
                      Added logException method to Logger
                      Added formatException method to Formatter
                      Added log_test6.py to test NTEventHandler and
                      logException
                      Numerous internal method renamings (sorry - but better
                      to do this now, rather than when we enter beta status).
-----------------------------------------------------------------------------
0.3       14 Mar 2002 First public release, for early feedback
-----------------------------------------------------------------------------
0.2                   Consolidated into single file (for internal use only)
-----------------------------------------------------------------------------
0.1                   Initial implementation (for internal use only)
-----------------------------------------------------------------------------

-----------------------------------------------------------------------------
COPYRIGHT
-----------------------------------------------------------------------------
Copyright 2001-2002 by Vinay Sajip. All Rights Reserved.

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name of Vinay Sajip
not be used in advertising or publicity pertaining to distribution
of the software without specific, written prior permission.
VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
