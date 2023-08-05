import os
import re
from .filetype import *


class FilePath():
    def __init__(self, *paths):
        path = FilePath.joinParts(*paths)
        self.root = FilePath.parseRoot(path)
        self.name = FilePath.parseName(path)
        self.type = FilePath.parseType(path)

    def join(self):
        return FilePath.joinParts(
            self.root, self.name + self.type.extension)

    def test(self):
        return os.path.exists(self.join())

    def read(self):
        mode = 'rb' if self.type.isBinary else 'r'
        encoding = None if self.type.isBinary\
            else self.type.encoding.name
        with open(self.join(), mode, encoding=encoding) as file:
            return file.read()

    def write(self, value):
        mode = 'wb' if self.type.isBinary else 'w'
        encoding = None if self.type.isBinary\
            else self.type.encoding.name
        with open(self.join(), mode, encoding=encoding) as file:
            file.write(value)

    @staticmethod
    def joinParts(*parts):
        return os.path.join(*parts)

    @staticmethod
    def parseRoot(path):
        return os.path.dirname(path)

    @staticmethod
    def parseStem(path):
        return os.path.basename(path)

    @staticmethod
    def parseName(path):
        basename = os.path.basename(path)
        return os.path.splitext(basename)[0]

    @staticmethod
    def parseType(path):
        extension = os.path.splitext(path)[1]
        return FileType.fromExtension(extension)

    @staticmethod
    def search(*, root='./', recursive=False,
               fileFilter=lambda f: True,
               rootFilter=lambda f: True):
        for root, dirs, files in os.walk(root):
            if rootFilter(root):
                for file in files:
                    if fileFilter(file):
                        yield os.path.join(root, file)
            if not recursive:
                break

    @staticmethod
    def match(*, root='./', recursive=False,
              filePattern='.*',
              rootPattern='.*'):
        fileRegex = re.compile(filePattern)
        rootRegex = re.compile(rootPattern)
        return FilePath.search(
            root=root,
            recursive=recursive,
            fileFilter=lambda f: bool(fileRegex.search(f)),
            rootFilter=lambda f: bool(rootRegex.search(f))
        )
