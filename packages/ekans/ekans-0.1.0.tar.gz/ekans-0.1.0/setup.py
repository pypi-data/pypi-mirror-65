# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ekans']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'packaging>=20.3,<21.0', 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'ekans',
    'version': '0.1.0',
    'description': 'A simple utility to check Conda environments integrity',
    'long_description': None,
    'author': 'Diego Vicente',
    'author_email': 'mail@diego.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
