#!/usr/bin/env python
from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here,"README.md")) as f:
    long_description = f.read()

VERSION = '0.0.1'

classifiers=[  
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]


setup(
    name='jse',
    version=VERSION,
    description="quickly edit json files from the command line",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Brian Jubelirer',
    author_email='brian2386@gmail.com',
    url='https://github.com/bjubes/jse',
    license='GPL3',
    classifiers=classifiers,
    keywords='json editor',
    packages=find_packages(where='jse'),
    python_requires='>=3.4',
    extras_require={  
            'test': ['pytest'],
    },
    entry_points={'jse': [
            'jse=jse:main'
        ]
    }
)