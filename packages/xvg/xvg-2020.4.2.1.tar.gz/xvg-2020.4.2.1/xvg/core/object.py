from .reflection import *


class Object(object):
    def __init__(self, fields={}):
        self.__dict__ = fields

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def getFieldValue(self, key):
        return self.__dict__[key]

    def setFieldValue(self, key, value):
        self.__dict__[key] = value

    def getFieldKeys(self):
        return ClassReflection.getFieldKeys(self)

    def getFieldValues(self):
        return ClassReflection.getFieldValues(self)

    def getFields(self):
        return ClassReflection.getFields(self)

    def getPublicFields(self):
        return ClassReflection.getPublicFields(self)

    def getPrivateFields(self):
        return ClassReflection.getPrivateFields(self)

    def getMethods(self):
        return ClassReflection.getMethods(self)

    def getPublicMethods(self):
        return ClassReflection.getPublicMethods(self)

    def getPrivateMethods(self):
        return ClassReflection.getPrivateMethods(self)
