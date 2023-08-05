import xml.etree.ElementTree as ET
from xvg.core import *


class SVGRenderer():
    """
    A Scalable Vector Graphics (SVG) renderer.
        Tutorial: https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial
        Elements: https://developer.mozilla.org/en-US/docs/Web/SVG/Element
        Attributes: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute
    """

    def __init__(self):
        pass

    def render(self, context):
        """ Renders the image and returns the result """

        headXML = '<?xml version="1.0" standalone="no"?>'
        headDOC = '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'

        root = ET.Element('svg')
        root.set('xmlns', 'http://www.w3.org/2000/svg')
        root.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        root.set('version', '1.1')

        root.set('width', str(context.size.x))
        root.set('height', str(context.size.y))

        viewX = context.scale.x / 2
        viewY = context.scale.y / 2
        viewW = context.scale.x
        viewH = context.scale.y
        root.set('viewBox', f'{viewX} {viewY} {viewW} {viewH}')

        encoding = 'utf-8'  # TODO use class
        result = headXML.encode(encoding)\
            + headDOC.encode(encoding)\
            + ET.tostring(root, encoding)

        return FileData(
            value=result,
            type=SVGFileType(),
            name=context.name
        )
