from xvg.math import Vector


class Point(Vector):
    def __init__(self, x=0, y=0):
        Vector.__init__(self, x, y)
