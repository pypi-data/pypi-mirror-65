#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright 2020, Justin Luce"
__license__ = "MIT"
__email__ = "support@justinluce.com"

## Bitcoin API calls
# https://en.bitcoin.it/wiki/Original_Bitcoin_client/API_calls_list#Full_list

## Bitvaluta API calls
# https://docs.bitvaluta.net/#/json-rpc-api-reference

import requests
import json
import os


class Client:
    """JSON-RPC Client."""

    def __init__(
        self,
        testnet=False,
        username=None,
        password=None,
        ip=None,
        port=None,
        directory=None,
    ):

        if not ip:
            self.ip = "localhost"  # default to localhost
        else:
            self.ip = ip

        if not username and not password:
            if not directory:
                try:
                    self.username, self.password = (
                        self.userpass()
                    )  # try to read from ~/.bitvaluta
                except:
                    self.username, self.password = self.userpass(
                        dir="bitvaluta"
                    )  # try to read from ~/.bitvaluta
            else:
                self.username, self.password = self.userpass(
                    dir=directory
                )  # try some other directory

        else:
            self.username = username
            self.password = password
        if testnet is True:
            self.testnet = True
            self.port = 15733
            self.url = "http://{0}:{1}".format(self.ip, self.port)
        else:
            self.testnet = False
            self.port = 15733
            self.url = "http://{0}:{1}".format(self.ip, self.port)
        if port is not None:
            self.port = port
            self.url = "http://{0}:{1}".format(self.ip, self.port)

        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.headers.update({"content-type": "application/json"})

    def userpass(self, dir="Bitvaluta"):
        """Reads config file for username/password"""

        source = os.path.expanduser("~/.{0}/{0}.conf").format(dir)
        dest = open(source, "r")
        with dest as conf:
            for line in conf:
                if line.startswith("rpcuser"):
                    username = line.split("=")[1].strip()
                if line.startswith("rpcpassword"):
                    password = line.split("=")[1].strip()

        return username, password

    def req(self, method, params=()):
        """send request to bitvalutad"""

        response = self.session.post(
            self.url,
            data=json.dumps({"method": method, "params": params, "jsonrpc": "1.1"}),
        ).json()

        if response["error"] is not None:
            return response["error"]
        else:
            return response["result"]

    def batch(self, reqs):
        """ send batch request using jsonrpc 2.0 """

        batch_data = []

        for req_id, req in enumerate(reqs):
            batch_data.append(
                {"method": req[0], "params": req[1], "jsonrpc": "2.0", "id": req_id}
            )

        data = json.dumps(batch_data)
        response = self.session.post(self.url, data=data).json()
        return response

    # RPC methods
    # general syntax is req($method, [array_of_parameters])

    # == Blockchain ==

    def getblockchaininfo(self):
        """return getblockchaininfo from bitvalutad"""
        return self.req("getblockchaininfo")

    def getbestblockhash(self):
        """Returns the hash of the best (tip) block in the longest block chain."""
        return self.req("getbestblockhash")

    def getblock(self, blockhash):
        """return getblock from bitvalutad"""
        return self.req("getblock", [blockhash])

    def getblockcount(self):
        """return getblockcount from bitvalutad"""
        return self.req("getblockcount")

    def getblockhash(self, height):
        """return getblockhash from bitvalutad"""
        return self.req("getblockhash", [height])

    def getblockheader(self, hash, verbose=False):
        """return getblockheader from bitvalutad"""
        return self.req("getblockheader")

    def getchaintips(self):
        """return getchaintips from bitvalutad"""
        return self.req("getchaintips")

    def getchaintxstats(self, nblocks=0, blockhash=""):
        """return getchaintxstats from bitvalutad"""
        query = nblocks
        if nblocks == 0 and blockhash != "":
            query = blockhash
        return self.req("getchaintxstats", [query])

    def getdifficulty(self):
        """return getdifficulty from bitvalutad"""
        return self.req("getdifficulty")

    def getmempoolancestors(self, txid, verbose=False):
        """return getinfo from bitvalutad"""
        return self.req("getmempoolancestors", [txid, verbose])

    def getmempoolentry(self, txid):
        """return getmempoolentry from bitvalutad"""
        return self.req("getmempoolentry", [txid])

    def getmempoolinfo(self):
        """return getinfo from bitvalutad"""
        return self.req("getmempoolinfo")

    def getrawmempool(self, verbose=False):
        """return getrawmempool from bitvalutad"""
        return self.req("getrawmempool", [verbose])

    def gettxout(self, txid, n, include_mempool=False):
        """return gettxout from bitvalutad"""
        return self.req("gettxout", [txid, n, include_mempool])

    def gettxoutproof(self, txids=[], blockhash=""):
        """return gettxoutproof from bitvalutad"""
        if blockhash == "":
            return self.req("gettxoutproof", [txids])
        else:
            return self.req("gettxoutproof", [txids, blockhash])

    def gettxoutsetinfo(self):
        """return gettxoutsetinfo from bitvalutad"""
        return self.req("gettxoutsetinfo")

    def preciousblock(self, blockhash=""):
        """Treats a block as if it were received before others with the same work."""
        return self.req("preciousblock", [blockhash])

    def savemempool(self):
        """return savemempool from bitvalutad"""
        return self.req("savemempool")

    def verifychain(self, checklevel=3, nblocks=6):
        """return verifychain from bitvalutad"""
        return self.req("verifychain", [checklevel, nblocks])

    def verifytxoutproof(self, proof):
        """return verifytxoutproof from bitvalutad"""
        return self.req("gettxout", [proof])

    # == Network ==

    def setnetworkactive(self, state=True):
        """Disable/enable all p2p network activity."""
        return self.req("setnetworkactive", [state])

    def getpeerinfo(self):
        """return getpeerinfo from bitvalutad"""
        return self.req("getpeerinfo")

    def ping(self):
        """Requests that a ping be sent to all other nodes, to measure ping time.
           Results provided in getpeerinfo, pingtime and pingwait fields are decimal seconds.
           Ping command is handled in queue with all other commands, so it measures processing backlog, not just network ping."""
        return self.req("ping")

    def getnetworkinfo(self):
        """Returns an object containing various state info regarding P2P networking."""
        return self.req("getnetworkinfo")

    def addnode(self, node, operation):
        """Attempts add or remove <node> from the addnode list or try a connection to <node> once."""
        return self.req("addnode", [node, operation])

    def disconnectnode(self, address="", nodeid=""):
        """Immediately disconnects from the specified peer node."""
        return self.req("disconnectnode", [address, nodeid])

    def clearbanned(self):
        """Clear all banned IPs."""
        return self.req("clearbanned")

    def listbanned(self):
        """List all banned IPs/Subnets."""
        return self.req("listbanned")

    def getaddednodeinfo(self, nodeid=""):
        """Returns information about the given added node, or all added nodes"""
        return self.req("getaddednodeinfo", [nodeid])

    def getconnectioncount(self):
        """Returns the number of connections to other nodes."""
        return self.req("getconnectioncount")

    def getnettotals(self):
        """Returns information about network traffic, including bytes in, bytes out,
           and current time."""
        return self.req("getnettotals")

    # == Control ==

    def help(self, command=None):
        """List commands, or get help for a command."""
        return self.req("help", [command]) if command else self.req("help")

    def getmemoryinfo(self, mode=None):
        """return getmemoryinfo from bitvalutad"""
        if mode:
            return self.req("getmemoryinfo", [mode])
        else:
            return self.req("getmemoryinfo")

    def stop(self):
        """stop bitvalutad"""
        return self.req("stop")

    def uptime(self):
        """return uptime from bitvalutad"""
        return self.req("uptime")

    # == Mining ==

    def getmininginfo(self):
        """return getmininginfo from bitvalutad"""
        return self.req("getmininginfo")

    def getnetworkhashps(self, nblocks, height):
        """Returns the estimated network hashes per second based on the last n blocks.
           Pass in [blocks] to override # of blocks, -1 specifies since last difficulty change.
           Pass in [height] to estimate the network speed at the time when a certain block was found."""
        return self.req("getnetworkhashps", [nblocks, height])

    # == Rawtransactions ==

    def combinerawtransaction(self, hexstrings=[]):
        """return combinerawtransaction from bitvalutad"""
        return self.req("combinerawtransaction", [hexstrings])

    def createrawtransaction(self, inputs=[], outputs={}, locktime=None):
        """return createrawtransaction from bitvalutad"""
        if locktime:
            return self.req("createrawtransaction", [inputs, outputs, locktime])
        else:
            return self.req("createrawtransaction", [inputs, outputs])

    def decoderawtransaction(self, hexstrings, iswitness=False):
        """return decoderawtransaction from bitvalutad"""
        return self.req("decoderawtransaction", [hexstrings, iswitness])

    def decodescript(self, hexstring):
        """return decodescript from bitvalutad"""
        return self.req("decodescript", [hexstring])

    def getrawtransaction(self, txid, verbose=False):
        """return getrawtransaction from bitvalutad"""
        return self.req("getrawtransaction", [txid, verbose])

    def sendrawtransaction(self, hexstring):
        """return sendrawtransaction from bitvalutad"""
        return self.req("sendrawtransaction", [hexstring])

    # == Util ==

    def validateaddress(self, address):
        """return validateaddress from bitvalutad"""
        return self.req("validateaddress", [address])

    def verifymessage(self, address, signature, message):
        """return decodescript from bitvalutad"""
        return self.req("verifymessage", [address, signature, message])

    # == Wallet ==

    def keypoolrefil(self, newsize=None):
        """Fills the keypool."""
        return self.req("keypoolrefil", [newsize])

    def dumpprivkey(self, address):
        """return dumpprivkey from bitvalutad"""
        return self.req("dumpprivkey", [address])

    def getaccount(self, address):
        """return getaccount from bitvalutad"""
        return self.req("getaccount", [address])

    def getaccountaddress(self, account):
        """return getaccountaddress from bitvalutad"""
        return self.req("getaccountaddress", [account])

    def getaddressesbyaccount(self, account):
        """return decodescript from bitvalutad"""
        return self.req("getaddressesbyaccount", [account])

    def getbalance(self, account="*", minconf=0):
        """return getbalance from bitvalutad"""
        return self.req("getbalance", [account, minconf])

    def getreceivedbyaccount(self, account, minconf=0):
        """return getreceivedbyaccount from bitvalutad"""
        return self.req("getreceivedbyaccount", [account, minconf])

    def getreceivedbyaddress(self, address, minconf=0):
        """ getreceivedbyaddress from bitvalutad"""
        return self.req("getreceivedbyaddress", [address, minconf])

    def gettransaction(self, txid, include_watchonly=True):
        """return gettransaction from bitvalutad"""
        return self.req("decodescript", [txid])

    def getwalletinfo(self):
        """return getwalletinfo from bitvalutad"""
        return self.req("getwalletinfo")

    def importaddress(self, address, label="", rescan=True):
        """return importaddress from bitvalutad"""
        return self.req("importaddress", [address, label, rescan])

    def importprivkey(self, privkey, label="", rescan=True):
        """return importprivkey from bitvalutad"""
        return self.req("importprivkey", [privkey, label, rescan])

    def listaccounts(self, minconf=0, include_watchonly=True):
        """return listaccounts from bitvalutad"""
        return self.req("listaccounts", [minconf, include_watchonly])

    def listtransactions(self, count=99999, skip=0, include_watchonly=False):
        """returns up to 'count' most recent transactions"""
        return self.req("listtransactions", ["*", count, skip, include_watchonly])

    def rescanblockchain(self, start_height=None, stop_height=None):
        """return rescanblockchain from bitvalutad"""
        if start_height is not None:
            if stop_height is not None:
                return self.req("rescanblockchain", [start_height, stop_height])
            else:
                return self.req("rescanblockchain", [start_height])
        else:
            return self.req("rescanblockchain")

    def sendtoaddress(self, address, amount):
        """send <amount> of BTV to <address>"""
        return self.req("sendtoaddress", [address, amount])

    def walletpassphrase(self, passphrase, timeout):
        """ return wallerpassphrase from bitvalutad"""
        return self.req("walletpassphrase", [passphrase, timeout])
