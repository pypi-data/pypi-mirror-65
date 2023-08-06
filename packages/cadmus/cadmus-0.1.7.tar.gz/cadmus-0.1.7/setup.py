# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cadmus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cadmus',
    'version': '0.1.7',
    'description': 'Lightweight commands for printing output',
    'long_description': None,
    'author': 'Rhaz Solomon',
    'author_email': 'rhaz.solomon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
