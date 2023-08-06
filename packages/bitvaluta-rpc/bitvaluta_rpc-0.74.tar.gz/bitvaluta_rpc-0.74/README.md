# bitvaluta_rpc

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/peercoin_rpc.svg?style=flat-square)](https://pypi.python.org/pypi/peercoin_rpc/)
[![](https://img.shields.io/badge/python-2.7+-blue.svg)](https://www.python.org/download/releases/2.7.0/) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


Bitvaluta_rpc is a simple and minimal library made for communication with `bitvalutad` via JSON-RPC protocol.
It has a single dependency - a Python `requests` library and it supports both mainnet and testnet bitvaluta network with authentication or SSL encryption.
There is a single class to be imported from the library - `Client`.

`Client` class methods are named the same as `bitvalutad` RPC methods so learning curve is non-existant.

## Install

> pip install git+git://github.com/peercoin/peercoin_rpc.git

or

> pip install bitvaluta_rpc

## How to use

> from bitvaluta_rpc import Client

Spawn a new Client object with desired arguments:

> node = Client(testnet=True, username="username", password="password", ip=<ip>, port=<port>)

Use it:

> node.getblockchaininfo()

> node.getpeerinfo()

> node.getbalance()
