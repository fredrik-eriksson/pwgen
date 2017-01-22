#!/usr/bin/env python
from os import environ

try:
    from setuptools import setup
except ImportError:
    from distutils import setup

import pwgen

version = '0.1'

setup(
        name='pwgen',
        version=str(version),
        description="Passphrase generator",
        author="Fredrik Eriksson",
        author_email="pwgen@wb9.se",
        url="https://github.com/fredrik-eriksson/pwgen",
        platforms=['any'],
        license='BSD',
        packages=['pwgen'],
        classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Console',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Topic :: Utilities',
            ],
        keywords='password passphrase',
        scripts=['bin/pwgen']
        )
