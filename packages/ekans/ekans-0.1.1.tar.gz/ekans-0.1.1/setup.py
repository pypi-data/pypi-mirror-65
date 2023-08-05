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
    'version': '0.1.1',
    'description': 'A simple utility to check Conda environments integrity',
    'long_description': '# `ekans` - A simple utility to check Conda environments integrity\n\n[![builds.sr.ht status](https://builds.sr.ht/~diego/ekans.svg)](https://builds.sr.ht/~diego/ekans?)\n\n`ekans` is an simple set of scripts able to perform different checks on\nAnaconda environments. This script is mainly thought as an easy way to\nsubstitute the notion of development dependencies, which is lacking in Conda\nenvironments.\n\nDevelopment dependencies are packages that are used during development and that\nmust strictly correlate with the Python version of the project. Some other\npackage managers (like Poetry) are able to define these dependencies to be\ninstalled in regular environments but excluded from builds or using flags. This\nis not possible in Conda: all packages in the declared environment are treated\nequally, which implies this unwanted dependencies being bundled in production\nas well. On the other hand, fighting against it makes the environment prone to\nbe non-consistent between production and development.\n\nOne way to solve this situation is having two different environments:\n`env/prod.yml` and `env/dev.yml`. `ekans` is able to check that **all versions\nare fixed and that production is a strict subset of development**. This results\nin the desired scenario: correctly excluding the unwanted dependencies while\nensuring that both environments have the same real dependencies to test\nagainst.\n\n## Install\n\n`TODO`\n\n## Usage\n\nTo check if an environment can be reproduced correctly, use the `verify` in the\nCLI tool. Not passing `-f` will cause the command to interactively prompt the\nuser to enter the path to the file.\n\n```shell\nekans verify [-f path/to/environment.yml]\n```\n',
    'author': 'Diego Vicente',
    'author_email': 'mail@diego.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.sr.ht/~diego/ekans',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
