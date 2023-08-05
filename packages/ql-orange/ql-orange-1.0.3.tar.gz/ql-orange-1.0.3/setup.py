# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blib2to3', 'blib2to3.pgen2']

package_data = \
{'': ['*']}

modules = \
['black']
install_requires = \
['aiohttp-cors',
 'aiohttp>=3.3.2',
 'appdirs',
 'click>=6.5',
 'mypy_extensions>=0.4.3',
 'pathspec>=0.6',
 'regex>=2019.8',
 'toml>=0.9.4',
 'typed-ast==1.4.0',
 'typing_extensions>=3.7.4']

entry_points = \
{'console_scripts': ['orange = black:patched_main']}

setup_kwargs = {
    'name': 'ql-orange',
    'version': '1.0.3',
    'description': '',
    'long_description': None,
    'author': 'quantlane.com',
    'author_email': 'info@quantlane.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
