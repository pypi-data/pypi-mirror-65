# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stackdriver_log_formatter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stackdriver-log-formatter',
    'version': '0.1.1',
    'description': 'Python log formatter for Google Stackdriver Logging',
    'long_description': "# python-stackdriver-log-formatter\n\n[![Build Status](https://travis-ci.com/tmshn/python-stackdriver-log-formatter.svg?branch=master)](https://travis-ci.com/tmshn/python-stackdriver-log-formatter)\n\n[![PyPI version](https://img.shields.io/pypi/v/stackdriver-log-formatter.svg)](https://pypi.python.org/pypi/stackdriver-log-formatter/)\n\nPython log formatter for Google Stackdriver Logging.\n\n## Usage\n\n```python\n>>> # setup\n>>> import logging, sys\n>>> from stackdriver_log_formatter import StackdriverLogFormatter\n>>> logging.basicConfig(level=logging.INFO, stream=sys.stdout)\n>>> logging.root.handlers[0].setFormatter(StackdriverLogFormatter())\n>>> # logging\n>>> logger = logging.getLogger(__name__)\n>>> logger.info('Hello world')\n```\n",
    'author': 'Shinichi TAMURA',
    'author_email': 'hello@tmshn.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tmshn/python-stackdriver-log-formatter',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
