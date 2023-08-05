# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpleelf']

package_data = \
{'': ['*']}

install_requires = \
['construct>=2.10.56,<3.0.0', 'pytest>=5.4.1,<6.0.0']

setup_kwargs = {
    'name': 'simpleelf',
    'version': '0.1.3',
    'description': 'Simple ELF parser and builder',
    'long_description': None,
    'author': 'DoronZ',
    'author_email': 'doron88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/doronz88/simpleelf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
