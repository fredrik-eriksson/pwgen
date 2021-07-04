#!/usr/bin/env python
from os import environ

try:
    from setuptools import setup
except ImportError:
    from distutils import setup

import pwgen

version = '1.0'

setup(
        name='pwgen',
        version=str(version),
        description="Passphrase generator",
        author="Fredrik Eriksson",
        author_email="feffe@fulh.ax",
        url="https://gitea.fulh.ax/feffe/pwgen",
        platforms=['any'],
        license='BSD',
        packages=['pwgen'],
        classifiers=[
            'Development Status :: 5 - Production/Stable'
            'Environment :: Console',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3',
            'Topic :: Utilities',
            ],
        keywords='password passphrase',
        scripts=['bin/pwgen']
        )
