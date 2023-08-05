# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfmake', 'tfmake.custom']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'pathlib>=1.0.1,<2.0.0', 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['tfmake = tfmake.cli:main']}

setup_kwargs = {
    'name': 'tfmake',
    'version': '0.7.6',
    'description': 'Python based Makefile wrapper for terraform projects',
    'long_description': None,
    'author': 'Pascal Prins',
    'author_email': 'pascal.prins@foobar-it.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
