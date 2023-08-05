import math
from .vector import *


class Polygon():
    def __init__(self):
        pass


class RegularPolygon():
    def __init__(self, n):
        q1 = math.pi / 2
        q4 = math.pi * 2
        a = q4 / n
        self.vertices = [
            Vector(math.cos(i*a), math.sin(i*a))
            for i in range(n)
        ]
