# Copyright (c) 2020 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Reference:
# https://github.com/libbitcoin/libbitcoin-system/wiki/Altcoin-Version-Mappings#bip44-altcoin-version-mapping-table

# Imports
import binascii
import sha3
from .bip32         import Bip32Const
from .bip_coin_conf import *
from .P2WPKH        import P2WPKH


class BitcoinHelper:
    """ Bitcoin class. It contains the constants some helper methods for BIP-0044 Bitcoin. """

    # Main net versions (zpub / zprv)
    MAIN_NET_VER = {"pub" : binascii.unhexlify(b"04b24746"), "priv" : binascii.unhexlify(b"04b2430c")}
    # Test net versions (vpub / vprv)
    TEST_NET_VER = {"pub" : binascii.unhexlify(b"045f1cf6"), "priv" : binascii.unhexlify(b"045f18bc")}

    @staticmethod
    def GetMainNetVersions():
        """ Get main net versions.

        Returns (dict):
            Main net versions (public at key "pub", private at key "priv")
        """
        return BitcoinHelper.MAIN_NET_VER

    @staticmethod
    def GetTestNetVersions():
        """ Get test net versions.

        Returns (dict):
            Test net versions (public at key "pub", private at key "priv")
        """
        return BitcoinHelper.TEST_NET_VER

    @staticmethod
    def GetWifNetVersions():
        """ Get WIF net versions.

        Returns (dict):
            WIF net versions (public at key "pub", private at key "priv")
        """
        return BitcoinConf.WIF_NET_VER

    @staticmethod
    def ComputeAddress(pub_key_bytes, is_testnet = False):
        """ Get address in P2WPKH format.

        Args:
            pub_key_bytes (bytes)       : public key bytes
            is_testnet (bool, optional) : true if test net, false if main net (default value)

        Returns (str):
            Address string
        """
        addr_ver = BitcoinConf.P2WPKH_NET_VER["main"] if not is_testnet else BitcoinConf.P2WPKH_NET_VER["test"]
        return P2WPKH.ToAddress(pub_key_bytes, addr_ver)


class LitecoinHelper:
    """ Litecoin class. It contains the constants some helper methods for BIP-0044 Litecoin. """

    # Main net versions (same of Bitcoin)
    MAIN_NET_VER = BitcoinHelper.MAIN_NET_VER
    # Test net versions (ttub / ttpv)
    TEST_NET_VER = {"pub" : binascii.unhexlify(b"0436f6e1"), "priv" : binascii.unhexlify(b"0436ef7d")}

    @staticmethod
    def GetMainNetVersions():
        """ Get main net versions.

        Returns (dict):
            Main net versions (public at key "pub", private at key "priv")
        """
        return LitecoinHelper.MAIN_NET_VER

    @staticmethod
    def GetTestNetVersions():
        """ Get test net versions.

        Returns (dict):
            Test net versions (public at key "pub", private at key "priv")
        """
        return LitecoinHelper.TEST_NET_VER

    @staticmethod
    def GetWifNetVersions():
        """ Get WIF net versions.

        Returns (dict):
            WIF net versions (public at key "pub", private at key "priv")
        """
        return LitecoinConf.WIF_NET_VER

    @staticmethod
    def ComputeAddress(pub_key_bytes, is_testnet = False):
        """ Get address in P2WPKH format.

        Args:
            pub_key_bytes (bytes)       : public key bytes
            is_testnet (bool, optional) : true if test net, false if main net (default value)

        Returns (str):
            Address string
        """
        addr_ver = LitecoinConf.P2WPKH_NET_VER["main"] if not is_testnet else LitecoinConf.P2WPKH_NET_VER["test"]
        return P2WPKH.ToAddress(pub_key_bytes, addr_ver)
