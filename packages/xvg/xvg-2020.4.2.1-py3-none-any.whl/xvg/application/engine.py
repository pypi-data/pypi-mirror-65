from xvg.contexts import *
from xvg.core import *
from xvg.interpreters import *
from xvg.renderers import *


class Engine():

    def __init__(self, renderer=None, context=None, interpreter=None):
        self.context = context or PureContext()
        self.renderer = renderer or JSONRenderer()
        self.interpreter = interpreter or ExecInterpreter()

    def process(self, script):
        self.interpreter.interpret(script, self.context)
        return self.renderer.render(self.context)

    def processFile(self, pathIn, pathOut=None):
        filePathIn = FilePath(pathIn)
        filePathOut = FilePath(pathOut) if pathOut else FilePath(pathIn)

        script = filePathIn.read()
        result = self.process(script)

        filePathOut.type = result.type
        filePathOut.write(result.value)

    def processFiles(self, pathRoot, recursive=False):
        for filePathIn in FilePath.match(
                root=pathRoot,
                recursive=recursive,
                filePattern='xvg$'):
            self.processFile(filePathIn)
