class String(str):
    def __new__(cls, *args, **kw):
        return str.__new__(cls, *args, **kw)
