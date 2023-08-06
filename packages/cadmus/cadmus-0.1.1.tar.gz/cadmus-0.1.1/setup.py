# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cadmus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cadmus',
    'version': '0.1.1',
    'description': 'A tool for printing coloured console output',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
