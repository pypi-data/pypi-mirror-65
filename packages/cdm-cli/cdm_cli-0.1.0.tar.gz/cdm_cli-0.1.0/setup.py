# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdm_cli']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.0,<5.0.0',
 'click>=7.1.1,<8.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['cdm = cdm_cli.cli:cli']}

setup_kwargs = {
    'name': 'cdm-cli',
    'version': '0.1.0',
    'description': 'A CLI for search and download mangas form the CDM website',
    'long_description': None,
    'author': 'Cleyson Lima',
    'author_email': 'cleysonph@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
