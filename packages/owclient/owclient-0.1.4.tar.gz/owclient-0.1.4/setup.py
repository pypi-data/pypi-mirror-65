# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['owclient', 'owclient.devices', 'owclient.exc']

package_data = \
{'': ['*']}

install_requires = \
['pyownet>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'owclient',
    'version': '0.1.4',
    'description': 'A light layer to use OWFS and pyownet with a more OOP approach.',
    'long_description': '',
    'author': 'Ferran Comabella',
    'author_email': 'ferran@fccma.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/fcomabella/ow-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
