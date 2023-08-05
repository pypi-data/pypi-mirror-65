# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['investify']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'requests>=2.23.0,<3.0.0', 'twilio>=6.38.0,<7.0.0']

setup_kwargs = {
    'name': 'investify',
    'version': '0.0.1',
    'description': 'Get automated price alert based on investing.com prices',
    'long_description': None,
    'author': 'Abhishek Guha',
    'author_email': 'abhi.workspace@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
