from abc import *


class Context(ABC):

    @abstractmethod
    def exportGlobals(self):
        return {}

    @abstractmethod
    def exportLocals(self):
        return {}
