# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqapy']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.2,<2.0.0']

setup_kwargs = {
    'name': 'sqapy',
    'version': '0.1.0',
    'description': 'Simulated quantum annealing implemented in Python',
    'long_description': None,
    'author': 'Hirofumi Tsuruta',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
