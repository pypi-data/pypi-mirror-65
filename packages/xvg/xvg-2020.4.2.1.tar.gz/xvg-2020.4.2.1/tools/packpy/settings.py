import os
import datetime
from .object import Object


class Settings():
    def __init__(self):
        self.settingsPath = 'settings.json'
        self.values = None

    def read(self):
        if not os.path.exists(self.settingsPath):
            raise Exception(f'Unable to read settings file: {self.settingsPath}')
        with open(self.settingsPath, 'r') as f:
            self.values = Object.fromJSON(f.read())

        return self

    def write(self):
        if not self.values:
            raise Exception(f'Unable to write settings file: {self.settingsPath}')
        with open(self.settingsPath, 'w') as f:
            f.write(Object.toJSON(self.values))

        return self

    def serializeVersion(self):
        return '.'.join([
            str(self.values.version.year),
            str(self.values.version.month),
            str(self.values.version.day),
            str(self.values.version.patch)
        ])

    def serializeNewVersion(self):
        date = datetime.date(
            self.values.version.year,
            self.values.version.month,
            self.values.version.day)
        patch = self.values.version.patch
        status = self.values.version.status

        newDate = datetime.date.today()
        newPatch = 0 if newDate > date else patch + 1

        self.values.version = Object({
            'year': newDate.year,
            'month': newDate.month,
            'day': newDate.day,
            'patch': newPatch,
            'status': status
        })
        return self.serializeVersion()
