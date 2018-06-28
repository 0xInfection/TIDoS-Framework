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
"""Test harness for the logging module. Demonstrates the use of custom class
instances for messages and filtering based on classes.

Copyright (C) 2001-2004 Vinay Sajip. All Rights Reserved.
"""

import logging

class MyClass:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        return "%s, %s" % (self.arg1, self.arg2)

class MyChildClass(MyClass):
    pass

class ClassFilter(logging.Filter):
    def __init__(self, klass):
        self.klass = klass

    def filter(self, record):
        return isinstance(record.msg, self.klass)

class MyClassFilter(ClassFilter):
    def __init__(self, arg):
        ClassFilter.__init__(self, MyClass)
        self.arg = arg

    def filter(self, record):
        return ClassFilter.filter(self, record) and (record.msg.arg2 == self.arg)

def main():
    handler = logging.StreamHandler()
    root = logging.getLogger("")
    root.setLevel(logging.DEBUG)
    root.addHandler(handler)
    root.addFilter(MyClassFilter("world"))
    #Not logged, as it's not a MyClass instance
    root.info("%s, %s", "Hello", "world")
    #Logged, as it's an appropriate instance which matches the filter criteria
    root.info(MyClass("Hello", "world"))
    #Not logged, as it's an appropriate class but doesn't match the filter criteria
    root.info(MyClass("Hello", "world!"))
    #Logged, as it's an appropriate instance which matches the filter criteria
    root.info(MyClass("Goodbye", "world"))
    #Logged, as it's an appropriate class which matches the filter criteria
    root.info(MyChildClass("Hello again", "world"))

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if "-profile" in args:
        import profile, pstats
        args.remove("-profile")
        statf = "log_test20.pro"
        profile.run("main()", statf)
        stats = pstats.Stats(statf)
        stats.strip_dirs().sort_stats('time').print_stats()
    else:
        main()
