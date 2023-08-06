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

    def addmultisigaddress(self, nrequired, key, account):
        """addmultisigaddress <nrequired> <'["key","key"]'> [account]"""
        return self.req("addmultisigaddress", [nrequired, key, account])

    def addnode(self, node, operation):
        """addnode <node> <add|remove|onetry>"""
        return self.req("addnode", [node, operation])

    def addredeemscript(self, redeemScript, account):
        """addredeemscript <redeemScript> [account]"""
        return self.req("addredeemscript", [redeemScript, account])
    
    def backupwallet(self, location):
        """backupwallet <destination>"""
        return self.req("backupwallet", [location])

    def burn(self, amount, hex_string):
        """burn <amount> [hex string]"""
        return self.req("burn", [amount, hex_string])

    def burnwallet(self, hex_string, force):
        """burnwallet [hex string] [force]"""
        return self.req("burnwallet", [hex_string, force])

    def checkkernel(self, txid, createblocktemplate=false):
        """checkkernel [{"txid":txid,"vout":n},...] [createblocktemplate=false]"""
        return self.req("checkkernel", [txid, createblocktemplate])

    def checkwallet(self):
        """checkwallet"""
        return self.req("checkwallet")

    def createrawtransaction(self, txid, amount):
        """createrawtransaction [{"txid":txid,"vout":n},...] {address:amount,...}"""
        return self.req("createrawtransaction", [txid, amount])

    def decoderawtransaction(self, hex_string):
        """decoderawtransaction <hex string>"""
        return self.req("decoderawtransaction", [hex_string])

    def decodescript(self, hex_string):
        """decodescript <hex string>"""
        return self.req("decodescript", [hex_string])

    def dumpprivkey(self, bitvalutaaddress):
        """dumpprivkey <bitvalutaaddress>"""
        return self.req("dumpprivkey", [bitvalutaaddress])

    def dumpwallet(self, filename):
        """dumpwallet <filename>"""
        return self.req("dumpwallet", [filename])

    def getaccount(self, bitvalutaaddress):
        """getaccount <bitvalutaaddress>"""
        return self.req("getaccount", [bitvalutaaddress])

    def getaccountaddress(self, account):
        """getaccountaddress <account>"""
        return self.req("getaccountaddress", [account])

    def getaddednodeinfo(self, dns, node):
        """getaddednodeinfo <dns> [node]"""
        return self.req("getaddednodeinfo", [dns, node])

    def getaddressesbyaccount(self, account):
        """getaddressesbyaccount <account>"""
        return self.req("getaddressesbyaccount", [account])

    def getbalance(self, account, mincomf=1):
        """getbalance [account] [minconf=1]"""
        return self.req("getbalance", [account, mincomf])

    def getbestblockhash(self):
        """getbestblockhash"""
        return self.req("command")

    def getblock(self, hash, txinfo):
        """getblock <hash> [txinfo]"""
        return self.req("getblock", [hash, txinfo])

    def getblockbynumber(self, number, txinfo):
        """getblockbynumber <number> [txinfo]"""
        return self.req("getblockbynumber", [number, txinfo])

    def getblockcount(self):
        """getblockcount"""
        return self.req("getblockcount")

    def getblockhash(self, index):
        """getblockhash <index>"""
        return self.req("getblockhash", [index])

    def getblocktemplate(self, params):
        """getblocktemplate [params]"""
        return self.req("getblocktemplate", [params])

    def getcheckpoint(self):
        """getcheckpoint"""
        return self.req("getcheckpoint")

    def getconnectioncount(self):
        """getconnectioncount"""
        return self.req("getconnectioncount")

    def getdifficulty(self):
        """getdifficulty"""
        return self.req("getdifficulty")

    def getinfo(self):
        """getinfo"""
        return self.req("getinfo")

    def getmininginfo(self):
        """getmininginfo"""
        return self.req("getmininginfo")

    def getnettotals(self):
        """getnettotals"""
        return self.req("getnettotals")

    def getnewaddress(self, account):
        """getnewaddress [account]"""
        return self.req("getnewaddress", [account])

    def getnewpubkey(self, account):
        """getnewpubkey [account]"""
        return self.req("getnewpubkey", [account])

    def getpeerinfo(self):
        """getpeerinfo"""
        return self.req("getpeerinfo")

    def getrawmempool(self):
        """getrawmempool"""
        return self.req("getrawmempool")

    def getrawtransaction(self, txid, verbose=0):
        """getrawtransaction <txid> [verbose=0]"""
        return self.req("getrawtransaction", [txid, verbose])

    def getreceivedbyaccount(self, account, mincomf=1):
        """getreceivedbyaccount <account> [minconf=1]"""
        return self.req("getreceivedbyaccount", [account, mincomf])

    def getreceivedbyaddress(self, bitvalutaaddress, mincomf=1):
        """getreceivedbyaddress <bitvalutaaddress> [minconf=1]"""
        return self.req("getreceivedbyaddress", [bitvalutaaddress, mincomf])

    def getstakesubsidy(self, hex_string):
        """getstakesubsidy <hex string>"""
        return self.req("getstakesubsidy", [hex_string])

    def getstakinginfo(self):
        """getstakinginfo"""
        return self.req("getstakinginfo")

    def getsubsidy(self, nTarget):
        """getsubsidy [nTarget]"""
        return self.req("getsubsidy", [nTarget])

    def gettransaction(self, txid):
        """gettransaction <txid>"""
        return self.req("gettransaction", [txid])

    def getwork(self, data):
        """getwork [data]"""
        return self.req("getwork", [data])

    def getworkex(self, data):
        """getworkex [data, coinbase]"""
        return self.req("getworkex", [data])

    def help(self, cmd):
        """help [command]"""
        return self.req("help", [cmd])

    def importprivkey(self, bitvalutaprivkey, label, rescan=true):
        """importprivkey <bitvalutaprivkey> [label] [rescan=true]"""
        return self.req("importprivkey", [bitvalutaprivkey, label, rescan])

    def importwallet(self, filename):
        """importwallet <filename>"""
        return self.req("importwallet", [filename])

    def keypoolrefill(self, new_size):
        """keypoolrefill [new-size]"""
        return self.req("keypoolrefill", [new_size])

    def listaccounts(self, minconf=1):
        """listaccounts [minconf=1]"""
        return self.req("listaccounts", [minconf])

    def listaddressgroupings(self):
        """listaddressgroupings"""
        return self.req("listaddressgroupings")

    def listreceivedbyaccount(self, minconf=1, includeempty=false):
        """listreceivedbyaccount [minconf=1] [includeempty=false]"""
        return self.req("listreceivedbyaccount", [minconf, includeempty])

    def listreceivedbyaddress(self, minconf=1, includeempty=false):
        """listreceivedbyaddress [minconf=1] [includeempty=false]"""
        return self.req("listreceivedbyaddress", [minconf, includeempty])

    def listsinceblock(self, blockhash, target_confirmations):
        """listsinceblock [blockhash] [target-confirmations]"""
        return self.req("listsinceblock", [blockhash, target_confirmations])

    def listtransactions(self, account, count=10, from_param=0):
        """listtransactions [account] [count=10] [from=0]"""
        return self.req("listtransactions", [account, count, from_param])

    def listunspent(self, mincomf, maxconf, address):
        """listunspent [minconf=1] [maxconf=9999999] ["address",...]"""
        return self.req("listunspent", [mincomf, maxconf, address])

    def makekeypair(self, prefix):
        """makekeypair [prefix]"""
        return self.req("makekeypair", [prefix])

    def move(self, from_account, to_account, amount, mincomf=1, comment=""):
        """move <fromaccount> <toaccount> <amount> [minconf=1] [comment]"""
        return self.req("move", [from_account, to_account, amount, mincomf, comment])

    def ping(self):
        """ping"""
        return self.req("ping")

    def repairwallet(self):
        """repairwallet"""
        return self.req("repairwallet")

    def resendtx(self):
        """resendtx"""
        return self.req("resendtx")

    def reservebalance(self, param):
        """reservebalance [<reserve> [amount]]"""
        return self.req("reservebalance", [param])

    def sendalert(self, message, privatekey, minver, maxver, priority, id, cancelupto):
        """sendalert <message> <privatekey> <minver> <maxver> <priority> <id> [cancelupto]"""
        return self.req("sendalert", [message, privatekey, minver, maxver, priority, id, cancelupto])

    def sendfrom(self, from_account, tobitvalutaaddress, amount, mincomf=1, comment="", comment_to=""):
        """sendfrom <fromaccount> <tobitvalutaaddress> <amount> [minconf=1] [comment] [comment-to]"""
        return self.req("sendfrom", [from_account, tobitvalutaaddress, amount, mincomf, comment, comment_to])

    def sendmany(self, from_account, address, mincomf=1, comment=""):
        """sendmany <fromaccount> {address:amount,...} [minconf=1] [comment]"""
        return self.req("sendmany", [from_account, address, mincomf, comment])

    def sendrawtransaction(self, hex_string):
        """sendrawtransaction <hex string>"""
        return self.req("sendrawtransaction", [hex_string])

    def sendtoaddress(self, bitvalutaaddress, amount, comment="", comment_to=""):
        """sendtoaddress <bitvalutaaddress> <amount> [comment] [comment-to]"""
        return self.req("sendtoaddress", [bitvalutaaddress, amount, comment, comment_to])

    def setaccount(self, bitvalutaaddress, account):
        """setaccount <bitvalutaaddress> <account>"""
        return self.req("setaccount", [bitvalutaaddress, account])

    def settxfee(self, amount):
        """settxfee <amount>"""
        return self.req("settxfee", [amount])

    def signmessage(self, bitvalutaaddress, message):
        """signmessage <bitvalutaaddress> <message>"""
        return self.req("signmessage", [bitvalutaaddress, message])

    def signrawtransaction(self, hex_string, param, priv_key, signhashtype="ALL"):
        """signrawtransaction <hex string> [{"txid":txid,"vout":n,"scriptPubKey":hex,"redeemScript":hex},...] [<privatekey1>,...] [sighashtype="ALL"]"""
        return self.req("signrawtransaction", [hex_string, param, priv_key, signhashtype])

    def stop(self):
        """stop"""
        return self.req("stop")

    def submitblock(self, hex_data):
        """submitblock <hex data> [optional-params-obj]"""
        return self.req("submitblock", [hex_data])

    def validateaddress(self, bitvalutaaddress):
        """validateaddress <bitvalutaaddress>"""
        return self.req("validateaddress", [bitvalutaaddress])

    def validatepubkey(self, bitvalutapubkey):
        """validatepubkey <bitvalutapubkey>"""
        return self.req("validatepubkey", [bitvalutapubkey])

    def verifymessage(self, bitvalutaaddress, signature, message):
        """verifymessage <bitvalutaaddress> <signature> <message>"""
        return self.req("verifymessage", [bitvalutaaddress, signature, message])

    def walletlock(self):
        """walletlock"""
        return self.req("walletlock")

    def walletpassphrase(self, passphrase, timeout, stakingonly):
        """walletpassphrase <passphrase> <timeout> [stakingonly]"""
        return self.req("walletpassphrase", [passphrase, timeout, stakingonly])

    def walletpassphrasechange(self, oldpassphrase, newpassphrase):
        """walletpassphrasechange <oldpassphrase> <newpassphrase>"""
        return self.req("walletpassphrasechange", [oldpassphrase, newpassphrase])