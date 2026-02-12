#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NuupXe Amateur Radio Voice Services
Setup configuration for package installation
"""

import os
import sys
from setuptools import setup, find_packages

# Ensure Python 3.8+
if sys.version_info < (3, 8):
    sys.exit('NuupXe requires Python 3.8 or higher')

# Read long description from README
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f 
                   if line.strip() and not line.startswith('#')]

setup(
    name='nuupxe',
    version='2.0.0',
    description='Amateur Radio Voice Services with AI/LLM Integration',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='NuupXe Project',
    author_email='contact@nuupxe.org',
    url='https://github.com/NuupXe/NuupXe',
    license='Apache License 2.0',
    
    # Package configuration
    packages=find_packages(exclude=['tests', 'tests.*', 'documentation']),
    include_package_data=True,
    zip_safe=False,
    
    # Requirements
    python_requires='>=3.8',
    install_requires=requirements,
    
    # Entry points for CLI commands
    entry_points={
        'console_scripts': [
            'nuupxe=nuupxe:main',
            'nuupxe-server=serviceManager:main',
        ],
    },
    
    # Package data
    package_data={
        'nuupxe': [
            'configuration/*.config.example',
            'learning/*',
            'morsefiles/*',
        ],
    },
    
    # Classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Communications :: Ham Radio',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Operating System :: POSIX :: Linux',
    ],
    
    # Keywords
    keywords=[
        'ham radio',
        'amateur radio',
        'voice services',
        'IRLP',
        'repeater',
        'AI',
        'LLM',
        'OpenAI',
        'GPT',
        'Whisper',
        'TTS',
        'speech recognition',
    ],
    
    # Project URLs
    project_urls={
        'Bug Reports': 'https://github.com/NuupXe/NuupXe/issues',
        'Source': 'https://github.com/NuupXe/NuupXe',
        'Documentation': 'https://github.com/NuupXe/NuupXe/tree/main/documentation',
    },
)
