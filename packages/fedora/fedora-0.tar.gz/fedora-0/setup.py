# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
from setuptools import setup
from setuptools.command.build_py import build_py


with open('README.md') as f:
    long_description = ''.join(f.readlines())


class NoBuild(build_py):
    """Raise an exception instead of building this package."""
    def run(self):
        print('-' * 72, file=sys.stderr)
        print(long_description, file=sys.stderr)
        print('-' * 72, file=sys.stderr)
        raise ValueError(
            '"fedora" is not installable. You probably want python-fedora.'
        )


setup(
    name='fedora',
    version='0',
    description='Placeholder for the fedora name',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Miro Hrončok',
    author_email='miro@hroncok.cz',
    url='https://github.com/fedora-python/fedora-pypi-placeholder',
    py_modules=['nonexisting'],
    classifiers=[
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    ],
    cmdclass={'build_py': NoBuild},
    zip_safe=False,
)
