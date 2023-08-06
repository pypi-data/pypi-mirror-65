# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qcheck']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'qcheck',
    'version': '0.1.0',
    'description': 'Simple way to validate data structures',
    'long_description': None,
    'author': 'miphreal',
    'author_email': 'miphreal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
