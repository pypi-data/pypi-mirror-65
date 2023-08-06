"""Utility methods that are used in csvblend."""

import zlib


def hash_function(value):
    """Map a group of characters to a fixed-size value.

    One that does not violate the keyword, identifier or parameter database
    requirements.

    :param str value: The value to hash.
    :rtype: str
    """
    # Ref: https://docs.python.org/3/library/zlib.html#zlib.crc32
    result = zlib.crc32(value.encode()) & 0xFFFFFFFF
    return str(result)
