# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioeos', 'aioeos.contracts']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.3.1,<4.0.0', 'base58==2.0.0', 'ecdsa==0.13.3']

setup_kwargs = {
    'name': 'aioeos',
    'version': '1.0.1',
    'description': 'Async library for interacting with EOS.io blockchain',
    'long_description': '# aioeos\n\n[![Documentation Status](https://readthedocs.org/projects/aioeos/badge/?version=latest)](http://aioeos.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/ulamlabs/aioeos/branch/master/graph/badge.svg)](https://codecov.io/gh/ulamlabs/aioeos) ![Python package](https://github.com/ulamlabs/aioeos/workflows/Python%20package/badge.svg) ![Upload Python Package](https://github.com/ulamlabs/aioeos/workflows/Upload%20Python%20Package/badge.svg)\n\nAsync Python library for interacting with EOS.io blockchain. \n\n## Features\n\n1. Async JSON-RPC client.\n2. Signing and verifying transactions using private and public keys.\n3. Serializer for basic EOS.io blockchain ABI types.\n4. Helpers which provide an easy way to generate common actions, such as token\n   transfer.\n\n## Installation\n\nLibrary is available on PyPi, you can simply install it using `pip`.\n```\n$ pip install aioeos\n```\n\n## Documentation\n\nDocs and usage examples are available [here](https://aioeos.readthedocs.io/en/latest).',
    'author': 'Maciej Janiszewski',
    'author_email': 'maciej@ulam.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ulam.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
