# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stackdriver_log_formatter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stackdriver-log-formatter',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Shinichi TAMURA',
    'author_email': 'shnch.tmr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
