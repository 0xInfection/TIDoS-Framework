#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

import os
import os.path


class File(object):
    def __init__(self, *pathComponents):
        self._path = FileUtils.buildPath(*pathComponents)
        self.content = None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        raise NotImplemented

    def isValid(self):
        return FileUtils.isFile(self.path)

    def exists(self):
        return FileUtils.exists(self.path)

    def canRead(self):
        return FileUtils.canRead(self.path)

    def canWrite(self):
        return FileUtils.canWrite(self.path)

    def read(self):
        return FileUtils.read(self.path)

    def update(self):
        self.content = self.read()

    def content(self):
        if not self.content:
            self.content = FileUtils.read()
        return self.content()

    def getLines(self):
        for line in FileUtils.getLines(self.path):
            yield line

    def __cmp__(self, other):
        if not isinstance(other, File):
            raise NotImplemented
        return cmp(self.content(), other.content())

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass


class FileUtils(object):
    @staticmethod
    def buildPath(*pathComponents):
        if pathComponents:
            path = os.path.join(*pathComponents)
        else:
            path = ''
        return path

    @staticmethod
    def exists(fileName):
        return os.access(fileName, os.F_OK)

    @staticmethod
    def canRead(fileName):
        if not os.access(fileName, os.R_OK):
            return False
        try:
            with open(fileName):
                pass
        except IOError:
            return False
        return True

    @staticmethod
    def canWrite(fileName):
        return os.access(fileName, os.W_OK)

    @staticmethod
    def read(fileName):
        result = ''
        with open(fileName, 'r') as fd:
            for line in fd.readlines():
                result += line
        return result

    @staticmethod
    def getLines(fileName):
        with open(fileName, 'r', errors="replace") as fd:
            return fd.read().splitlines()

    @staticmethod
    def isDir(fileName):
        return os.path.isdir(fileName)

    @staticmethod
    def isFile(fileName):
        return os.path.isfile(fileName)

    @staticmethod
    def createDirectory(directory):
        if not FileUtils.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def sizeHuman(num):
        base = 1024
        for x in ['B ', 'KB', 'MB', 'GB']:
            if num < base and num > -base:
                return "%3.0f%s" % (num, x)
            num /= base
        return "%3.0f %s" % (num, 'TB')

    @staticmethod
    def writeLines(fileName, lines):
        content = None
        if type(lines) is list:
            content = "\n".join(lines)
        else:
            content = lines
        with open(fileName, "w") as f:
            f.writelines(content)
