# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brish']

package_data = \
{'': ['*']}

install_requires = \
['IPython>=7.13.0,<8.0.0', 'plumbum>=1.6.9,<2.0.0']

setup_kwargs = {
    'name': 'brish',
    'version': '0.1.3',
    'description': 'A bridge between zsh and Python.',
    'long_description': None,
    'author': 'NightMachinary',
    'author_email': 'rudiwillalwaysloveyou@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
