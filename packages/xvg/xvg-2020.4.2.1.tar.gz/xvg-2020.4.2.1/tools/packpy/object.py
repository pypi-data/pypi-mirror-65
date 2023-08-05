import json


class Object(object):
    def __init__(self, items={}):
        self.__dict__ = items

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    @staticmethod
    def toJSON(data):
        return json.dumps(data, default=lambda o: o.__dict__, indent=4)

    @staticmethod
    def fromJSON(data):
        return json.loads(data, object_hook=lambda d: Object(d))
