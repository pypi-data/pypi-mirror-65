class Encoding():
    def __init__(self, *, name):
        self.name = name

    @staticmethod
    def fromName(string):
        lower = string.lower()
        if lower == 'ascii':
            return ASCIIEncoding()
        if lower == 'utf-8':
            return UTF8Encoding()


class ASCIIEncoding(Encoding):
    def __init__(self):
        Encoding.__init__(self, name='ascii')


class UTF8Encoding(Encoding):
    def __init__(self):
        Encoding.__init__(self, name='utf-8')
