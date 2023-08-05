class ExecInterpreter():

    def interpret(self, script, context):
        exec(script, context.exportGlobals(), context.exportLocals())
