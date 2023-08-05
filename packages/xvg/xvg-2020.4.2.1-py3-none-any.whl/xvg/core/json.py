from json import loads, dumps
from .object import Object


class JSON():

    @staticmethod
    def serialize(data):
        return dumps(data, default=lambda o: o.__dict__)

    @staticmethod
    def deserialize(data):
        return loads(data, object_hook=lambda d: Object(d))
