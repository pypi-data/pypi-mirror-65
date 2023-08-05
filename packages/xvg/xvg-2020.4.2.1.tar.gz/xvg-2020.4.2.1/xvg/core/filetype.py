from .encoding import *


class FileType():
    def __init__(self, *, extension, encoding, isBinary):
        self.extension = extension
        self.encoding = encoding
        self.isBinary = isBinary

    @staticmethod
    def fromExtension(string):
        lower = string.lower()
        if lower == '.xvg':
            return XVGFileType()
        if lower == '.json':
            return JSONFileType()
        if lower == '.svg':
            return SVGFileType()
        if lower == '.png':
            return PNGFileType()


class XVGFileType(FileType):
    def __init__(self):
        FileType.__init__(self, extension='.xvg',
                          encoding=UTF8Encoding(), isBinary=False)


class JSONFileType(FileType):
    def __init__(self):
        FileType.__init__(self, extension='.json',
                          encoding=UTF8Encoding(), isBinary=False)


class SVGFileType(FileType):
    def __init__(self):
        FileType.__init__(self, extension='.svg',
                          encoding=UTF8Encoding(), isBinary=True)


class PNGFileType(FileType):
    def __init__(self):
        FileType.__init__(self, extension='.png',
                          encoding=None, isBinary=True)
