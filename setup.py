import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

import sheet2db

HERE = os.path.abspath(os.path.dirname(__file__))

# Package meta-data.
NAME = 'sheet2db'
DESCRIPTION = 'A tiny library for one-way syncing the Google spreadsheet to database'
URL = 'https://github.com/mingrammer/sheet2db'
EMAIL = 'mingrammer@gmail.com'

# What packages are required for this module to be executed?
REQUIRED = []
with io.open(os.path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        REQUIRED.append(line)

# Import the README and use it as the long-description.
with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name=NAME,
    version=sheet2db.__version__,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=sheet2db.__author__,
    author_email=EMAIL,
    url=URL,
    keywords='spreadsheet sync',
    packages=find_packages(),
    install_requires=REQUIRED,
    include_package_data=True,
    license=sheet2db.__license__,
    python_requires='>=3',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries'

    ],
    # $ setup.py publish support.
    cmdclass={
        'publish': PublishCommand,
    },
)
