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
"""Test harness for the logging module. Demonstrates the use of a wildcard
name-space filter with and without custom message classes.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""

import logging, re, string, types

class TaggedEvent:
    def __init__(self, tag, msg):
        self.tag = tag
        self.msg = msg

    def __str__(self):
        return "%s: %s" % (self.tag, self.msg)

class WildcardFilter(logging.Filter):
    def __init__(self, wildcards):
        self.setWildcards(wildcards)

    def setWildcard(self, wildcard):
        arr = string.split(wildcard, ".")
        for i in xrange(len(arr)):
            s = arr[i]
            if s == "*":
                arr[i] = r'[\w.]*'
            elif string.find(s, "*") > 0:
                arr[i] = string.replace(s, "*", r'[\w]*')
        s = "^%s$" % string.join(arr, r'\.')
        self.patterns.append(re.compile(s))

    def setWildcards(self, wildcards):
        if type(wildcards) != types.ListType:
            wildcards = [wildcards]
        self.patterns = []
        for wildcard in wildcards:
            self.setWildcard(wildcard)

    def filter(self, record):
        rv = 0
        for pat in self.patterns:
            m = pat.match(record.name)
            if m is not None:
                rv = 1
                break
        return rv

class TagFilter(WildcardFilter):
    def filter(self, record):
        rv = 0
        if isinstance(record.msg, TaggedEvent):
            tag = record.msg.tag
        else:
            tag = record.name
        for pat in self.patterns:
            m = pat.match(tag)
            if m is not None:
                rv = 1
                break
        return rv

def main():
    handler = logging.StreamHandler()
    root = logging.getLogger("")
    root.setLevel(logging.DEBUG)
    ab = logging.getLogger("a.b")
    abc = logging.getLogger("a.b.c")

    root.addHandler(handler)
    filter = WildcardFilter("*.b")
    handler.addFilter(filter)

    ab.info("#1 from a.b")       #logged
    abc.info("#1 from a.b.c")    #not logged
    filter.setWildcards("*.b.c")
    ab.info("#2 from a.b")       #not logged
    abc.info("#2 from a.b.c")    #logged
    filter.setWildcards("*.b*")
    ab.info("#3 from a.b")       #logged
    abc.info("#3 from a.b.c")    #not logged
    filter.setWildcards("*")
    ab.info("#4 from a.b")       #logged
    abc.info("#4 from a.b.c")    #logged
    filter.setWildcards("a*")
    ab.info("#5 from a.b")       #not logged
    abc.info("#5 from a.b.c")    #not logged
    filter.setWildcards("a.*")
    ab.info("#6 from a.b")       #logged
    abc.info("#6 from a.b.c")    #logged
    filter.setWildcards("*.b.*")
    ab.info("#7 from a.b")       #not logged
    abc.info("#7 from a.b.c")    #logged
    filter.setWildcards(["*.b", "*.b.*"])
    ab.info("#8 from a.b")       #logged
    abc.info("#8 from a.b.c")    #logged
    filter.setWildcards(["a.*.c"])
    ab.info("#9 from a.b")       #not logged
    abc.info("#9 from a.b.c")    #logged

    #Now test filtering with a tagged class
    handler.removeFilter(filter)
    tagfilter = TagFilter(["*.b", "*.b.*"])
    root.addFilter(tagfilter)
    root.info(TaggedEvent("a.b", "#10"))     #logged
    root.info(TaggedEvent("a.c", "#10"))     #not logged
    root.info(TaggedEvent("a.b.c", "#10"))   #logged
    root.info(TaggedEvent("a.b.d", "#10"))   #logged

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if "-profile" in args:
        import profile, pstats
        args.remove("-profile")
        statf = "log_test21.pro"
        profile.run("main()", statf)
        stats = pstats.Stats(statf)
        stats.strip_dirs().sort_stats('time').print_stats()
    else:
        main()
