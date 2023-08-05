# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mercure',
 'mercure.client',
 'mercure.client.publisher',
 'mercure.client.publisher.tests',
 'mercure.client.subscriber']

package_data = \
{'': ['*']}

extras_require = \
{'async': ['aiohttp>=3.4.4,<4.0.0'],
 'common': ['requests>=2.21,<3.0'],
 'gevent': ['requests>=2.21,<3.0', 'gevent>=1.4.0,<2.0.0']}

setup_kwargs = {
    'name': 'mercure',
    'version': '0.0.1',
    'description': 'The service to push events between parties. The messenger of gods.',
    'long_description': None,
    'author': 'BCD TripTech',
    'author_email': 'development@bcdtriptech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
