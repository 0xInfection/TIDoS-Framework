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
A test harness for the logging module. Tests arbitrary logging levels, filtering, and
use of strftime formatting.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""

import logging
import locale, sys

locale.setlocale(locale.LC_ALL, '')

def message(s):
    sys.stderr.write("%s\n" % s)

#
#   First, we define our levels. There can be as many as you want - the only limitations are that
#   they should be integers, the lowest should be > 0 and larger values mean less information being
#   logged. If you need specific level values which do not fit into these limitations, you can use
#   a mapping dictionary to convert between your application levels and the logging system.
#
SILENT      = 10
TACITURN    = 9
TERSE       = 8
EFFUSIVE    = 7
SOCIABLE    = 6
VERBOSE     = 5
TALKATIVE   = 4
GARRULOUS   = 3
CHATTERBOX  = 2
BORING      = 1

LEVEL_RANGE = range(BORING, SILENT + 1)

#
#   Next, we define names for our levels. You don't need to do this - in which case the system will
#   use "Level n" to denote the text for the level.
#
my_logging_levels = {
    SILENT      : 'Silent',
    TACITURN    : 'Taciturn',
    TERSE           : 'Terse',
    EFFUSIVE    : 'Effusive',
    SOCIABLE    : 'Sociable',
    VERBOSE     :   'Verbose',
    TALKATIVE   :   'Talkative',
    GARRULOUS   :   'Garrulous',
    CHATTERBOX: 'Chatterbox',
    BORING      :   'Boring',
}

#
#   Now, tell the logging system to associate names with our levels.
#
for lvl in my_logging_levels.keys():
    logging.addLevelName(lvl, my_logging_levels[lvl])

#
#   Now, define a test function which logs an event at each of our levels.
#
def doLog(log):
    for lvl in LEVEL_RANGE:
        log.log(lvl, "This should only be seen at the '%s' logging level (or lower)", logging.getLevelName(lvl))

#
#   Get the root logger and add a console hander to it, when run as a script.
#
log = logging.getLogger("")

if __name__ == "__main__":
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%X")) #date format is as per the locale
    log.addHandler(hdlr)
else:
    hdlr = log.handlers[0]
#
#   Set the logging level to each different value and call the utility function to log events.
#   In the output, you should see that each time round the loop, the logging events actually output
#   decreases.
#
for lvl in LEVEL_RANGE:
    message("-- setting logging level to '%s' -----" % logging.getLevelName(lvl))
    log.setLevel(lvl)
    doLog(log)
#
#   Now, we demonstrate level filtering at the handler level. Tell the handler defined above
#   to filter at level 'SOCIABLE', and repeat the above loop. Compare the output from the two runs.
#
hdlr.setLevel(SOCIABLE)
message("-- Filtering at handler level to SOCIABLE --")
for lvl in LEVEL_RANGE:
    message("-- setting logging level to '%s' -----" % logging.getLevelName(lvl))
    log.setLevel(lvl)
    doLog(log)

hdlr.setLevel(0)    #turn off level filtering at the handler

#
#   Now, let's demonstrate filtering. Suppose for some perverse reason we only want to print out
#   all except GARRULOUS messages. Let's create a filter for this purpose...
#
class SpecificLevelFilter(logging.Filter):
    def __init__(self, lvl):
        self.level = lvl

    def filter(self, record):
        return self.level != record.levelno

class GarrulousFilter(SpecificLevelFilter):
    def __init__(self):
        SpecificLevelFilter.__init__(self, GARRULOUS)

garr = GarrulousFilter()
hdlr.addFilter(garr)
message("-- Filtering using GARRULOUS filter --")
for lvl in LEVEL_RANGE:
    message("-- setting logging level to '%s' -----" % logging.getLevelName(lvl))
    log.setLevel(lvl)
    doLog(log)
#
#   Now, let's demonstrate filtering at the logger. This time, use a filter which excludes SOCIABLE
#   and TACITURN messages. Note that GARRULOUS events are still excluded.
#
class VerySpecificFilter(logging.Filter):
    def filter(self, record):
        return record.levelno not in [SOCIABLE, TACITURN]

spec = VerySpecificFilter()
log.addFilter(spec)
message("-- Filtering using specific filter for SOCIABLE, TACITURN --")
for lvl in LEVEL_RANGE:
    message("-- setting logging level to '%s' -----" % logging.getLevelName(lvl))
    log.setLevel(lvl)
    doLog(log)

log.removeFilter(spec)
hdlr.removeFilter(garr)
#Undo the one level which clashes...for regression tests
logging.addLevelName(logging.DEBUG, "DEBUG")

#
#   Er...that's it for now
#
if __name__ == "__main__":
    print "All done."
    logging.shutdown()

