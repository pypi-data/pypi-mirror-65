# bitvaluta_rpc

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/peercoin_rpc.svg?style=flat-square)](https://pypi.python.org/pypi/bitvaluta_rpc/)
[![](https://img.shields.io/badge/python-2.7+-blue.svg)](https://www.python.org/download/releases/2.7.0/) 


Bitvaluta_rpc is a simple and minimal library made for communication with `bitvalutad` via JSON-RPC protocol.
It has a single dependency - a Python `requests` library and it supports both mainnet and testnet bitvaluta network with authentication or SSL encryption.
There is a single class to be imported from the library - `Client`.

`Client` class methods are named the same as `bitvalutad` RPC methods so learning curve is non-existant.

## Install

> pip install bitvaluta_rpc

## How to use

> from bitvaluta_rpc import Client

Spawn a new Client object with desired arguments:

> node = Client(testnet=True, username="username", password="password", ip=<ip>, port=<port>)

Use it:

> node.getblockchaininfo()

> node.getpeerinfo()

> node.getbalance()

Availible Commands:

> `addmultisigaddress <nrequired> <'["key","key"]'> [account]` 
 
> `addnode <node> <add|remove|onetry>`
 
> `addredeemscript <redeemScript> [account]`
 
> `backupwallet <destination>`
 
> `burn <amount> [hex string]`
 
> `burnwallet [hex string] [force]`
 
> `checkkernel [{"txid":txid,"vout":n},...] [createblocktemplate=false]`
 
> `checkwallet`
 
> `createrawtransaction [{"txid":txid,"vout":n},...] {address:amount,...}`
 
> `decoderawtransaction <hex string>`
 
> `decodescript <hex string>`
 
> `dumpprivkey <bitvalutaaddress>`
 
> `dumpwallet <filename>`
 
> `getaccount <bitvalutaaddress>`
 
> `getaccountaddress <account>`
 
> `getaddednodeinfo <dns> [node]`
 
> `getaddressesbyaccount <account>`
 
> `getbalance [account] [minconf=1]`
 
> `getbestblockhash`
 
> `getblock <hash> [txinfo]`
 
> `getblockbynumber <number> [txinfo]`
 
> `getblockcount`
 
> `getblockhash <index>`
 
> `getblocktemplate [params]`
 
> `getcheckpoint`
 
> `getconnectioncount`
 
> `getdifficulty`
 
> `getinfo`
 
> `getmininginfo`
 
> `getnettotals`
 
> `getnewaddress [account]`
 
> `getnewpubkey [account]`
 
> `getpeerinfo`
 
> `getrawmempool`
 
> `getrawtransaction <txid> [verbose=0]`
 
> `getreceivedbyaccount <account> [minconf=1]`
 
> `getreceivedbyaddress <bitvalutaaddress> [minconf=1]`
 
> `getstakesubsidy <hex string>`
 
> `getstakinginfo`
 
> `getsubsidy [nTarget]`
 
> `gettransaction <txid>`
 
> `getwork [data]`
 
> `getworkex [data, coinbase]`
 
> `help [command]`
 
> `importprivkey <bitvalutaprivkey> [label] [rescan=true]`
 
> `importwallet <filename>`
 
> `keypoolrefill [new-size]`
 
> `listaccounts [minconf=1]`
 
> `listaddressgroupings`
 
> `listreceivedbyaccount [minconf=1] [includeempty=false]`
 
> `listreceivedbyaddress [minconf=1] [includeempty=false]`
 
> `listsinceblock [blockhash] [target-confirmations]`
 
> `listtransactions [account] [count=10] [from=0]`
 
> `listunspent [minconf=1] [maxconf=9999999] ["address",...]`
 
> `makekeypair [prefix]`
 
> `move <fromaccount> <toaccount> <amount> [minconf=1] [comment]`
 
> `ping`
 
> `repairwallet`
 
> `resendtx`
 
> `reservebalance [<reserve> [amount]]`
 
> `sendalert <message> <privatekey> <minver> <maxver> <priority> <id> [cancelupto]`
 
> `sendfrom <fromaccount> <tobitvalutaaddress> <amount> [minconf=1] [comment] [comment-to]`
 
> `sendmany <fromaccount> {address:amount,...} [minconf=1] [comment]`
 
> `sendrawtransaction <hex string>`
 
> `sendtoaddress <bitvalutaaddress> <amount> [comment] [comment-to]`
 
> `setaccount <bitvalutaaddress> <account>`
 
> `settxfee <amount>`
 
> `signmessage <bitvalutaaddress> <message>`
 
> `signrawtransaction <hex string> [{"txid":txid,"vout":n,"scriptPubKey":hex,"redeemScript":hex},...] [<privatekey1>,...] [sighashtype="ALL"]`
 
> `stop`
 
> `submitblock <hex data> [optional-params-obj]`
 
> `validateaddress <bitvalutaaddress>`
 
> `validatepubkey <bitvalutapubkey>`
 
> `verifymessage <bitvalutaaddress> <signature> <message>`
 
> `walletlock`
 
> `walletpassphrase <passphrase> <timeout> [stakingonly]`
 
> `walletpassphrasechange <oldpassphrase> <newpassphrase>`