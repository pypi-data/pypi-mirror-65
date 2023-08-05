import setuptools
from tools.packpy.settings import *

classifierStatus = [
    'Development Status :: 1 - Planning',
    'Development Status :: 2 - Pre-Alpha',
    'Development Status :: 3 - Alpha',
    'Development Status :: 4 - Beta',
    'Development Status :: 5 - Production/Stable',
    'Development Status :: 6 - Mature',
    'Development Status :: 7 - Inactive'
]

classifierPython = {
    '3': 'Programming Language :: Python :: 3 :: Only',
    '2': 'Programming Language :: Python :: 2 :: Only'
}

classifierSystem = {
    'any': 'Operating System :: OS Independent',
    'osx': 'Operating System :: MacOS :: MacOS X',
    'linux': 'Operating System :: POSIX :: Linux',
    'windows': 'Operating System :: Microsoft :: Windows',
}

classifierLicense = {
    'mit': 'License :: OSI Approved :: MIT License',
    'gpl2': 'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
}

# Read the settings
settings = Settings().read()

# Read the README
with open("README.md", "r") as fh:
    readme = fh.read()
    readmeType = "text/markdown"

# Build the package
setuptools.setup(
    name=settings.values.name,
    version=settings.serializeNewVersion(),
    author=settings.values.author,
    description=settings.values.description,
    long_description=readme,
    long_description_content_type=readmeType,
    url=settings.values.website,
    packages=setuptools.find_packages(),
    classifiers=[
        classifierStatus[settings.values.version.status],
        classifierPython[settings.values.python.split('.')[0].lower()],
        classifierSystem[settings.values.system.lower()],
        classifierLicense[settings.values.license.lower()]
    ],
    python_requires=f'~={settings.values.python}'
)

# Save the settings
settings.write()
