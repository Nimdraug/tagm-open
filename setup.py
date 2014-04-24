#!/usr/bin/env python2
from setuptools import setup

setup(
    name = 'tagm-open',
    version = '0.1-dev',

    maintainer = u'Martin Hult\xe9n-Ashauer',
    maintainer_email = 'tagm@nimdraug.com',
    url = 'http://github.com/Nimdraug/tagm-open',
    license = 'MIT',
    description = 'Command tool to open files based on it\'s tagm tags.',

    install_requires = [
        'tagm'
    ],

    py_modules = [
        'tagm_open'
    ],
    entry_points = {
        'console_scripts': [
            'tagm-open = tagm_open:main'
        ]
    }
)