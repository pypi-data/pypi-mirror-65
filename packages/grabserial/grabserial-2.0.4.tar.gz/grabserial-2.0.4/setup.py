#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

VERSION = '2.0.4'

setup(
    name='grabserial',
    version=VERSION,
    scripts=['grabserial',],
    #packages=['grabserial',],
    author='Tim Bird',
    author_email='tbird20d@yahoo.com',

    maintainer='Tim Bird',
    maintainer_email='tbird20d@yahoo.com',

    description='Serial dump and timing program',
    long_description='''
https://github.com/tbird20d/grabserial

grabserial is a small program which reads a serial port and writes the data
to standard output. The main purpose of this tool is to collect messages
written to the serial console from a target board running Linux, and save
the messages on a host machine.
''',
    url='https://github.com/straend/grabserial',
    license='GPL v2',
    keywords='grabserial serial boot time optimization tool',
    classifiers=[
        "Topic :: Utilities",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Embedded Systems",
    ],

    install_requires=[
        "pyserial>=2.6"
    ],
)
