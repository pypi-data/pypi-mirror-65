import os
import json
import glob
import shutil
from .secrets import *


class Uploader():

    @staticmethod
    def upload():
        # Read secrets
        secrets = Secrets().read()

        python = secrets.values.python
        username = secrets.values.username
        password = secrets.values.password

        # Clean artifacts
        shutil.rmtree('build', ignore_errors=True)
        shutil.rmtree('dist', ignore_errors=True)
        for dir in glob.glob('*.egg-info'):
            shutil.rmtree(dir, ignore_errors=True)

        # Build artifacts
        os.system(f"{python} -m pip install --user --upgrade setuptools wheel")
        os.system(f"{python} setup.py sdist bdist_wheel")

        # Publish artifacts
        auth = f"-u {username} -p {password}"
        os.system(f"{python} -m pip install --user --upgrade twine")
        os.system(f"{python} -m twine upload dist/* {auth}")


if __name__ == '__main__':
    Uploader().upload()
