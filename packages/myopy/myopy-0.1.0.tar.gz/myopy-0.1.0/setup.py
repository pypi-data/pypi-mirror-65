# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myopy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'myopy',
    'version': '0.1.0',
    'description': 'myopy, run blind python files.',
    'long_description': None,
    'author': 'Loic Coyle',
    'author_email': 'loic.coyle@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
