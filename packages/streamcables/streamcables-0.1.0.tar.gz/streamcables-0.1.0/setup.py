# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['streamcables']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4,<2.0',
 'beautifulsoup4>=4.8,<5.0',
 'maya>=0.6.1,<0.7.0',
 'requests>=2.23,<3.0',
 'toml>=0.10.0,<0.11.0',
 'tweepy>=3.8,<4.0']

setup_kwargs = {
    'name': 'streamcables',
    'version': '0.1.0',
    'description': 'Syndicate audio streaming metadata to webservices.',
    'long_description': None,
    'author': 'Sander van Dragt',
    'author_email': 'sander@vandragt.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
