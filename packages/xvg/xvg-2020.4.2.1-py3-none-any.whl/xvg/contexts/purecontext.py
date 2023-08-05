from .context import Context
from xvg.core import Object
from xvg.math import Vector

import math
import xvg.core
import xvg.math
import xvg.models


class PureContext(Context):

    def __init__(self):
        self.name = 'untitled'
        self.size = Vector()
        self.scale = Vector()

    def exportGlobals(self):
        return {
            "__builtins__": {
                "locals": locals, "globals": globals
            }
        }

    def exportLocals(self):
        exports = Object()

        exports.Math = math

        return exports

        # localsMap.update(xvg.core.getModuleClasses(xvg.core))
        # localsMap.update(xvg.core.getPublicModuleFunctions(xvg.core))

        # localsMap.update(xvg.core.getModuleClasses(xvg.math))
        # localsMap.update(xvg.core.getPublicModuleFunctions(xvg.math))

        # localsMap.update(xvg.core.getModuleClasses(xvg.models))
        # localsMap.update(xvg.core.getPublicModuleFunctions(xvg.models))

        # localsMap.update(self.getPublicFields())
        # localsMap.update(self.getPublicMethods())

        # return localsMap

    def setNode(self, id, model):
        pass

    def getNode(self, id):
        pass

    def useNode(self, id):
        pass
