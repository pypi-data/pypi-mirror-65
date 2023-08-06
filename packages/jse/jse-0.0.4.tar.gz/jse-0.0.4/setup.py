# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jse']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['jse = jse.jse:main']}

setup_kwargs = {
    'name': 'jse',
    'version': '0.0.4',
    'description': 'quickly edit json files from the command line',
    'long_description': None,
    'author': 'Brian Jubelirer',
    'author_email': 'brian2386@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
