# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clutch',
 'clutch.method',
 'clutch.network',
 'clutch.network.rpc',
 'clutch.schema.request',
 'clutch.schema.request.session',
 'clutch.schema.request.torrent',
 'clutch.schema.user',
 'clutch.schema.user.method',
 'clutch.schema.user.method.session',
 'clutch.schema.user.method.torrent',
 'clutch.schema.user.response',
 'clutch.schema.user.response.session',
 'clutch.schema.user.response.torrent']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.4,<2.0', 'requests>=2.22.0,<3.0.0']

extras_require = \
{':python_version == "3.6" or python_version == "3.7"': ['typing-extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'transmission-clutch',
    'version': '3.0.0.dev5',
    'description': 'An RPC client library for the Transmission BitTorrent client',
    'long_description': 'Clutch\n--------\n\n.. image:: https://readthedocs.org/projects/clutch/badge/?version=latest\n    :target: https://clutch.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://img.shields.io/pypi/v/transmission-clutch.svg?style=flat-square\n    :target: https://pypi.org/project/transmission-clutch\n\n.. image:: https://img.shields.io/pypi/pyversions/transmission-clutch.svg?style=flat-square\n    :target: https://pypi.org/project/transmission-clutch\n\n.. image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square\n    :target: https://en.wikipedia.org/wiki/MIT_License\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\nQuick start\n===========\n\nInstall the package:\n\n.. code-block:: console\n\n    $ pip install transmission-clutch\n\nMake a client:\n\n.. code-block:: python\n\n    from clutch.client import Client\n    client = Client()\n\nIf you find the client isn\'t connecting (an error will be raised), make sure you\'re entering the address correctly. Reference `urllib.parse.urlparse`_ for parsing rules.\n\nYou can specify Transmission\'s address when making the client:\n\n.. code-block:: python\n\n    client = Client(address="http://localhost:9091/transmission/rpc")\n\n.. _urllib.parse.urlparse: https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse\n\nRPC methods are separated into groups: torrent, session, queue and misc.\n\nMethods are called by first specifying a group:\n\n.. code-block:: python\n\n    client.torrent.add(...)\n',
    'author': 'mhadam',
    'author_email': 'michael@hadam.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mhadam/clutch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
