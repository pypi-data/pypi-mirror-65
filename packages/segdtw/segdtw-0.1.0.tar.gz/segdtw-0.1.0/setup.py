# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['segdtw', 'segdtw.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.2,<2.0.0']

setup_kwargs = {
    'name': 'segdtw',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'stegben',
    'author_email': 'stegben.benjamin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
