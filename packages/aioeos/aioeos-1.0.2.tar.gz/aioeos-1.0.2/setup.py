# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioeos', 'aioeos.contracts', 'aioeos.types']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.3.1,<4.0.0', 'base58==2.0.0', 'ecdsa>=0.15,<0.16']

setup_kwargs = {
    'name': 'aioeos',
    'version': '1.0.2',
    'description': 'Async library for interacting with EOS.io blockchain',
    'long_description': "# aioeos\n\n[![Documentation Status](https://readthedocs.org/projects/aioeos/badge/?version=latest)](http://aioeos.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/ulamlabs/aioeos/branch/master/graph/badge.svg)](https://codecov.io/gh/ulamlabs/aioeos) ![Python package](https://github.com/ulamlabs/aioeos/workflows/Python%20package/badge.svg) ![Upload Python Package](https://github.com/ulamlabs/aioeos/workflows/Upload%20Python%20Package/badge.svg)\n\nAsync Python library for interacting with EOS.io blockchain. \n\n## Features\n\n1. Async JSON-RPC client.\n2. Signing and verifying transactions using private and public keys.\n3. Serializer for basic EOS.io blockchain ABI types.\n4. Helpers which provide an easy way to generate common actions, such as token\n   transfer.\n\n## Installation\n\nLibrary is available on PyPi, you can simply install it using `pip`.\n```\n$ pip install aioeos\n```\n\n## Usage\n\n### Importing a private key\n\n```\nfrom aioeos import EosAccount\n\naccount = EosAccount(private_key='your key')\n```\n\n### Transferring funds\n\n```\nfrom aioeos import EosJsonRpc, EosTransaction\nfrom aioeos.contracts import eosio_token\n\n\nrpc = EosJsonRpc(url='http://127.0.0.1:8888')\nblock = await rpc.get_head_block()\n\ntransaction = EosTransaction(\n   ref_block_num=block['block_num'] & 65535,\n   ref_block_prefix=block['ref_block_prefix'],\n   actions=[\n      eosio_token.transfer(\n         from_addr=account.name,\n         to_addr='mysecondacc1',\n         quantity='1.0000 EOS',\n         authorization=[account.authorization('active')]\n      )\n   ]\n)\nawait rpc.sign_and_push_transaction(transaction, keys=[account.key])\n```\n\n### Creating a new account\n\n```\nfrom aioeos import EosJsonRpc, EosTransaction, EosAuthority\nfrom aioeos.contracts import eosio\n\n\nmain_account = EosAccount(name='mainaccount1', private_key='private key')\nnew_account = EosAccount(name='mysecondacc1')\nowner = EosAuthority(\n   threshold=1,\n   keys=[new_account.key.to_key_weight(1)]\n)\n\nrpc = EosJsonRpc(url='http://127.0.0.1:8888')\nblock = await rpc.get_head_block()\n\nawait rpc.sign_and_push_transaction(\n   EosTransaction(\n      ref_block_num=block['block_num'] & 65535,\n      ref_block_prefix=block['ref_block_prefix'],\n      actions=[\n            eosio.newaccount(\n               main_account.name,\n               new_account.name,\n               owner=owner,\n               authorization=[main_account.authorization('active')]\n            ),\n            eosio.buyrambytes(\n               main_account.name,\n               new_account.name,\n               2048,\n               authorization=[main_account.authorization('active')]\n            )\n      ],\n   ),\n   keys=[main_account.key]\n)\n```\n\n## Documentation\n\nDocs and usage examples are available [here](https://aioeos.readthedocs.io/en/latest).\n\n## Unit testing\n\nTo run unit tests, you need to bootstrap an EOS testnet node first. Use the provided `ensure_eosio.sh` script.\n\n```\n$ ./ensure_eosio.sh\n```\n",
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
