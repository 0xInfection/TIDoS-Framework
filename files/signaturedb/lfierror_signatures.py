#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# This file is a part of TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Signatures used by the file inclusion / path traversal scanners.

FILE_SIGNATURES identify the *content* of well-known system files. A
scanner only reports a file as read when its signature matches the payload
response, does not match the baseline response, and does not match a
control response for a file that does not exist.

INCLUSION_ERRORS are error messages printed when a script fails to open or
include a file. They are hints only (the input reaches a file API), never
proof that a file could be read.
"""

# key: (path suffix the payload must end with, label, regex)
FILE_SIGNATURES = {
    "passwd": ("etc/passwd", "/etc/passwd",
               r"(?<![\w:])root:[^:\s]{0,40}:0:0:[^:\r\n]*:[^:\r\n]*:"),
    "win.ini": ("windows/win.ini", "C:\\Windows\\win.ini",
                r"; for 16-bit app support|\[fonts\][\s\S]{0,200}\[extensions\]"),
    "boot.ini": ("boot.ini", "C:\\boot.ini",
                 r"\[boot loader\][\s\S]{0,300}\[operating systems\]"),
    "environ": ("proc/self/environ", "/proc/self/environ",
                r"(?:^|\x00)(?:PATH|HOME|PWD|HOSTNAME|SERVER_SOFTWARE|DOCUMENT_ROOT)=[^\x00\r\n]*\x00"),
    "status": ("proc/self/status", "/proc/self/status",
               r"(?m)^TracerPid:\s+\d+\s*$[\s\S]{0,200}^Uid:\s+\d+\s+\d+\s+\d+\s+\d+"),
    "version": ("proc/version", "/proc/version",
                r"Linux version \d+\.\d+[^\s(]*\s+\([^)]*@[^)]*\)"),
}

INCLUSION_ERRORS = [
    r"[Ff]ailed to open stream",
    r"Failed opening '[^']*' for inclusion",
    r"open_basedir restriction in effect",
    r"(?:include|require)(?:_once)?\(\): (?:Failed|Unable|http:// wrapper|https:// wrapper|URL file-access)",
    r"allow_url_include",
    r"URL file-access is disabled",
    r"java\.io\.FileNotFoundException",
    r"System\.IO\.(?:FileNotFoundException|DirectoryNotFoundException)",
    r"No such file or directory",
]
