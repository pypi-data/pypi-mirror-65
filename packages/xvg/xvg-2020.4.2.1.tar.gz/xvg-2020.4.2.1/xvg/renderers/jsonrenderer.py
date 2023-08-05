from xvg.core import *


class JSONRenderer():

    def render(self, context):
        result = JSON.serialize(context)
        return FileData(
            value=result,
            type=JSONFileType(),
            name=context.name
        )
