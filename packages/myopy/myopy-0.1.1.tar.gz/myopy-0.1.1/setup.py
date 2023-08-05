# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myopy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'myopy',
    'version': '0.1.1',
    'description': 'myopy, run blind python files.',
    'long_description': "![tests](https://github.com/loiccoyle/pyconf/workflows/tests/badge.svg)\n\n# myopy\n\n> Run blind python files.\n\nThis single class package, provides python objects to a python file at run time. This is ideal for configuration files where the user does not need to know where an object comes from or how to initialize it. It allows the python file to be blind to the origin of it's objects, removing the need for imports, object initializations or convoluted subclassing.\n\nThis is pretty much a standalone clone of the way the amazing [qutebrowser](https://github.com/qutebrowser/qutebrowser) handles it's config files.\n\nFeel free to copy paste the `PyConfig` class if you don't want the added dependency.\n\n# Installation\n```\npip install myopy\n```\n\n# Usage\n\nSay you want to allow the user to change a `dict` containing some settings for an application in a configuration file called `config.py`:\n\nIn the application you would have something along the lines of:\n\n```python\nfrom myopy import PyConfig\n\nuser_dict = {'something': 2}\n\nconfig = PyConfig('path/to/config.py')\nconfig.provide('settings', user_dict)  # we provide the config file the user_dict in the settings variable\nout = config.run()  # out is a dict of the provided objects\nprint('after running config: ', user_dict)\nprint('out: ', out)\n```\nAnd in the user facing `config.py`, the `user_dict` object would be provided in the `settings` variable, and the user can change its values at will:\n```python\nprint('in config: ', settings)\nsettings['something_else'] = 4\nsettings['something'] = 3\n```\n\nThe output would be:\n```\nin config: {'something': 2}\nafter running config: {'something': 3, 'something_else': 4}\nout: {'settings': {'something': 3, 'something_else': 4}}\n```\nthe `user_dict` is modified in place.\n\n",
    'author': 'Loic Coyle',
    'author_email': 'loic.coyle@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/loiccoyle/myopy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
