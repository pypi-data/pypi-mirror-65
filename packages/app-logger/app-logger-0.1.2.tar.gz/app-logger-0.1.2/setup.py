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
    'version': '0.1.2',
    'description': 'A drop in logger configurable through environment variables',
    'long_description': '# app-logger\n\nThis is a drop in logger that uses [python-json-logger](https://github.com/madzak/python-json-logger) to log json to stdout and stderr appropriately. DEBUG and INFO go to stdout, WARNING, ERROR, CRITICAL go to stderr.\n\n# Configuration\nAll configuration is through environment variables, all have defaults so none are required.\n\n## LOGGER_NAME\nWhat should the logger be called? Default will use the root logger. Using the default or `root` will log not only log statements from `app_logger` but also any statements from libraries you\'re using.\n**Format**: Just a regular string\n**Default**: `root`\n**Example**: `mysweetapp`\n\n## LOG_LEVELS\nUsed to set log levels. Can be used to set any log level you wish so you can selectively control logging. May be upper or lower case.\n**Format**: A comma separated string of key=value pairs\n**Default**: `root=INFO`\n**Example**: `root=DEBUG,asyncio=INFO`\n\n## LOG_FORMAT\nUsed to control the log format.\n**Format**: A log format string of [log record attributes](https://docs.python.org/3.7/library/logging.html#logrecord-attributes)\n**Default**: `%(levelname)%(name)%(asctime)%(module)%(funcName)%(lineno)%(message)``\n\n## Usage\nThe logger initializes itself and makes itself available as a variable called `app_logger`. It\'s a regular python logger and can be used as such.\n**Example** `app_logger.info("I always hated python logging but now it\'s easy and just works")`\n**Resulting log** `{"levelname": "INFO", "name": "root", "asctime": "2020-04-11 11:24:17,299", "module": "main", "funcName": "main", "lineno": 14, "message": "I always hated python logging but now it\'s easy and just works"}`\n\n### Adding context\nYou can use the `extra=` feature of python-json-logger to add context to your messages. This makes it really easy to have logging that\'s easy to parse, search, learn, and alert on if you\'re using log aggregation.\n**Example**\nGiven you have something that\'s a dictionary, you can include it in log statements without verbose string formatting.\n`app_logger.error(\'Error handling message\', extra=message)`\n**Resulting log**\n`{"levelname": "ERROR", "name": "root", "asctime": "2020-04-11 11:27:36,584", "module": "main", "funcName": "main", "lineno": 16, "message": "Error handling message", "guid": "7cc81eba-3bbc-4555-8fab-2a7556072f5d", "subject": "test"}\n`\nYou can see how easy it would be to find logs like this in kibana, and it\'s already in json format so it\'s easily indexable/searchable, including the context given via `extra=`',
    'author': 'zackary stevens',
    'author_email': 'zackary.n.stevens@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TnLCommunity/app-logger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
