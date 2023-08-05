import os
from .object import Object


class Secrets():
    def __init__(self):
        self.secretsPath = 'secrets.json'
        self.values = None

    def read(self):
        if not os.path.exists(self.secretsPath):
            raise Exception(f'Unable to read secrets file: {self.secretsPath}')
        with open(self.secretsPath, 'r') as f:
            self.values = Object.fromJSON(f.read())

        return self

    def write(self):
        if not self.values:
            raise Exception(f'Unable to write secrets file: {self.secretsPath}')
        with open(self.secretsPath, 'w') as f:
            f.write(Object.toJSON(self.values))

        return self
