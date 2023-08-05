# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kac']

package_data = \
{'': ['*'], 'kac': ['templates/*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'jinja2>=2.11.1,<3.0.0',
 'pyperclip>=1.8.0,<2.0.0',
 'questionary>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['kac = kac.kac:cli']}

setup_kwargs = {
    'name': 'kac',
    'version': '0.3.0',
    'description': 'A command line tool for CHANGELOG files that follow the Keep-a-Changelog standard.',
    'long_description': None,
    'author': 'Adam Walsh',
    'author_email': 'adam@grid.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/atwalsh/kac',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
