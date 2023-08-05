from abc import *


class Interpreter(ABC):

    @abstractmethod
    def interpret(self, script, context):
        pass
