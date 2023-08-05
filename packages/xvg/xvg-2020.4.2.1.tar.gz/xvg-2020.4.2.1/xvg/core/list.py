class List(list):
    def __new__(cls, *args, **kw):
        return list.__new__(cls, *args, **kw)
