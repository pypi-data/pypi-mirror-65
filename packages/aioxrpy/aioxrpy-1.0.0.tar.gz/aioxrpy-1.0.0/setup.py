# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioxrpy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.3.1,<4.0.0', 'base58==2.0.0', 'ecdsa>=0.15,<0.16']

setup_kwargs = {
    'name': 'aioxrpy',
    'version': '1.0.0',
    'description': 'Ripple blockchain library for Python',
    'long_description': "# aioxrpy\n\n[![Documentation Status](https://readthedocs.org/projects/aioxrpy/badge/?version=latest)](http://aioxrpy.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/ulamlabs/aioxrpy/branch/master/graph/badge.svg)](https://codecov.io/gh/ulamlabs/aioxrpy) ![Python package](https://github.com/ulamlabs/aioxrpy/workflows/Python%20package/badge.svg) ![Upload Python Package](https://github.com/ulamlabs/aioxrpy/workflows/Upload%20Python%20Package/badge.svg)\n\nRipple blockchain library for Python.\n\n## Features\n\n1. Async JSON-RPC client.\n2. Signing and verifying transactions using private and public keys.\n3. Support for signing transactions with multiple keys.\n4. Serializer and deserializer for Ripple objects.\n\n## Installation\n\nLibrary is available on PyPi, you can simply install it using `pip`.\n```\n$ pip install aioxrpy\n```\n\n## Usage\n\n### Keys\n\nSigning and verifying transactions, as well as generating new accounts is done through `RippleKey` class. \n\n```\nfrom aioxrpy.keys import RippleKey\n\n# New key\nkey = RippleKey()\n\n# From public key\nkey = RippleKey(public_key=b'public key')\n\n# From master seed\nkey = RippleKey(private_key='seed')\n\n# From private key\nkey = RippleKey(private_key=b'private key')\n```\n\nSuch key can be converted to Account ID and public key. \n\n### Submitting transactions\n\nRPC client provides a helper which signs and submits transaction. As a first \nargument it takes a transaction dict. The second one is a `RippleKey` instance\nused for signing this transaction.\n\n```\nfrom aioxrpy.rpc import RippleJsonRpc\n\nrpc = RippleJsonRpc(url)\nawait rpc.sign_and_submit(\n    {\n        'Account': account,\n        'TransactionType': RippleTransactionType.Payment,\n        'Amount': decimals.xrp_to_drops(200),\n        'Destination': destination,\n        'Fee': 10\n    },\n    signer\n)\n```\n\n### Multi-signed transactions\n\nRPC client provides a helper which signs and submits transaction using multiple\nkeys. As a second argument, it expects a list of `RippleKey` instances. Please \ndon't forget that each signer increases transaction fees.\n\n```\nfrom aioxrpy.rpc import RippleJsonRpc\n\nrpc = RippleJsonRpc(url)\nawait rpc.multisign_and_submit(\n    {\n        'Account': account,\n        'TransactionType': RippleTransactionType.Payment,\n        'Amount': decimals.xrp_to_drops(200),\n        'Destination': destination,\n        'Fee': 30\n    },\n    [signer_1, signer_2]\n)\n```\n\n## Documentation\n\nDocs and usage examples are available [here](https://aioxrpy.readthedocs.io/en/latest).\n\n## Unit testing\n\nTo run unit tests, you need to bootstrap a Rippled regtest node first. Use the provided `docker-compose.yml` file.\n\n```\n$ docker-compose up -d\n```\n",
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
