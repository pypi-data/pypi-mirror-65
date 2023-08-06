# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brish']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'brish',
    'version': '0.1.5',
    'description': 'A bridge between zsh and Python.',
    'long_description': None,
    'author': 'NightMachinary',
    'author_email': 'rudiwillalwaysloveyou@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
