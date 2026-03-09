#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NuupXe Amateur Radio Voice Services
Setup configuration for package installation.

Dependencies and metadata are declared in pyproject.toml (PEP 517/518).
This file handles things pyproject.toml cannot yet express: py_modules and
package_data for a flat-layout project.
"""

import sys
from setuptools import setup, find_packages

# Ensure Python 3.8+
if sys.version_info < (3, 8):
    sys.exit('NuupXe requires Python 3.8 or higher')

setup(
    # Top-level modules not inside a package directory
    py_modules=['nuupxe', 'serviceManager'],

    # Sub-packages (core/, modules/, learning/)
    packages=find_packages(exclude=['tests', 'tests.*', 'documentation']),

    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': [
            'nuupxe=nuupxe:main',
        ],
    },

    package_data={
        '': [
            'configuration/*.config.example',
            'morsefiles/*',
            'learning/*',
        ],
    },
)
