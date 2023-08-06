# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['app_logger']

package_data = \
{'': ['*']}

install_requires = \
['python-json-logger>=0.1.11,<0.2.0']

setup_kwargs = {
    'name': 'app-logger',
    'version': '0.1.1',
    'description': 'A drop in logger configurable through environment variables',
    'long_description': None,
    'author': 'zackary stevens',
    'author_email': 'zackary.n.stevens@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
