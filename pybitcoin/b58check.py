# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import re
from binascii import hexlify, unhexlify
from hashlib import sha256
from utilitybelt import change_charset
from .hash import bin_checksum

HEX_KEYSPACE = "0123456789abcdef"
B58_KEYSPACE = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58check_encode(bin_s, version_byte=0):
    """ Takes in a binary string and converts it to a base 58 check string. """
    # append the version byte to the beginning
    bin_s = chr(int(version_byte)).encode('utf-8') + bin_s
    # calculate the number of leading zeros
    num_leading_zeros = len(re.match(r'^\x00*', bin_s.decode('latin_1')).group(0))
    # add in the checksum add the end
    bin_s = bin_s + bin_checksum(bin_s)
    # convert from b2 to b16
    hex_s = hexlify(bin_s)
    # convert from b16 to b58
    b58_s = change_charset(hex_s.decode(), HEX_KEYSPACE, B58_KEYSPACE)

    return B58_KEYSPACE[0] * num_leading_zeros + b58_s


def b58check_unpack(b58_s):
    """ Takes in a base 58 check string and returns: the version byte, the
        original encoded binary string, and the checksum.
    """
    num_leading_zeros = len(re.match(r'^1*', b58_s).group(0))
    # convert from b58 to b16
    hex_s = change_charset(b58_s, B58_KEYSPACE, HEX_KEYSPACE)
    # if an odd number of hex characters are present, add a zero to the front
    if len(hex_s) % 2 == 1:
        hex_s = "0" + hex_s
    # convert from b16 to b2
    bin_s = unhexlify(hex_s)
    # add in the leading zeros
    bin_s = b'\x00' * num_leading_zeros + bin_s
    # make sure the newly calculated checksum equals the embedded checksum
    newly_calculated_checksum = bin_checksum(bin_s[:-4])
    embedded_checksum = bin_s[-4:]
    if not (newly_calculated_checksum == embedded_checksum):
        raise ValueError('b58check value has an invalid checksum')
    # return values
    version_byte = bin_s[:1]
    encoded_value = bin_s[1:-4]
    checksum = bin_s[-4:]
    return version_byte, encoded_value, checksum


def b58check_decode(b58_s):
    """ Takes in a base 58 check string and returns the original encoded binary
        string.
    """
    version_byte, encoded_value, checksum = b58check_unpack(b58_s)
    return encoded_value


def b58check_version_byte(b58_s):
    """ Takes in a base 58 check string and returns the version byte as an
        integer. """
    version_byte, encoded_value, checksum = b58check_unpack(b58_s)
    return ord(version_byte)


def is_b58check(b58_s):
    version_byte, binary_s, checksum = b58check_unpack(b58_s)
    return (b58_s == b58check_encode(
        binary_s, version_byte=ord(version_byte)))
