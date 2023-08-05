# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pspipe', 'pspipe.tests']

package_data = \
{'': ['*'], 'pspipe': ['templates/*', 'templates/config/*']}

install_requires = \
['astropy>=4.0,<5.0',
 'asyncssh>=2.0,<3.0',
 'matplotlib>=3.2.0,<4.0.0',
 'progressbar2>=3.47,<4.0',
 'python-casacore>=3.2.0,<4.0.0',
 'tables>=3.6.1,<4.0.0',
 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'pspipe',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': '"Florent Mertens"',
    'author_email': '"florent.mertens@gmail.com"',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
