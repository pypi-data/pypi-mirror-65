# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['segdtw']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'segdtw',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'stegben',
    'author_email': 'stegben.benjamin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
