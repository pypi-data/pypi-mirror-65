import types
from .error import *
from inspect import *


class Reflection():

    @staticmethod
    def testModule(target):
        return ismodule(target)

    @staticmethod
    def testClass(target):
        return isclass(target)


class ModuleReflection():

    @staticmethod
    def getClasses(target):
        return (m for m in getmembers(target)
                if isclass(m))

    @staticmethod
    def getFunctions(target):
        return (m for m in getmembers(target)
                if isfunction(m) or isbuiltin(m))

    @staticmethod
    def getPublicFunctions(target):
        return (m for m in getFunctions(target)
                if m[0][0] != '_')

    @staticmethod
    def getPrivateFunctions(target):
        return (m for m in getFunctions(target)
                if m[0][0] == '_')


class ClassReflection():

    @staticmethod
    def getFieldKeys(target):
        return vars(target).keys()

    @staticmethod
    def getFieldValues(target):
        return vars(target).values()

    @staticmethod
    def getFields(target):
        return vars(target).items()

    @staticmethod
    def getPublicFields(target):
        return (m for m in getFields(target)
                if m[0][0] != '_')

    @staticmethod
    def getPrivateFields(target):
        return (m for m in getFields(target)
                if m[0][0] == '_')

    @staticmethod
    def getMethods(target):
        return (m for m in getmembers(target)
                if ismethod(m))

    @staticmethod
    def getPublicMethods(target):
        return (m for m in getMethods(target)
                if m[0][0] != '_')

    @staticmethod
    def getPrivateMethods(target):
        return (m for m in getMethods(target)
                if m[0][0] == '_')
