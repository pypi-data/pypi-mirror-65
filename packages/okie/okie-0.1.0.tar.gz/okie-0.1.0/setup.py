# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['okie', 'okie.builders', 'okie.ctrl']

package_data = \
{'': ['*']}

install_requires = \
['httptools>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'okie',
    'version': '0.1.0',
    'description': '[WIP] Small(and dumb) http request generator and stream controller',
    'long_description': '==================\n[WIP] 🌲 okie\n==================\n\n\n**Minimalistic http client for production and tests.**\n',
    'author': 'Martin Winks',
    'author_email': 'cat@snejugal.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uwinx/okie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
