"""Utility functions for calculating CRC16."""

"""Generator polynomial."""
GENERATOR = 0x2F15

"""Lookup table used during CRC calculation. Will be calculated once the module is loaded."""
LOOKUP = [0] * 256


def __generate_lookup() -> None:
    """Generates the lookup table that is used in CRC calculation."""
    crc = 0x8000
    i = 1

    while i < 256:
        if crc & 0x8000:
            crc = (crc << 1) ^ GENERATOR
        else:
            crc = crc << 1

        for j in range(i):
            LOOKUP[i+j] = (crc ^ LOOKUP[j]) & 0xFFFF

        i <<= 1


__generate_lookup()


def crc16(data: bytes) -> int:
    """
    Calculates and returns the CRC16 value of the supplied byte string.
    :param data: Bytestring to digest
    :return: CRC16 value of bytes
    """
    crc = 0
    for b in data:
        crc = ((crc << 8) ^ LOOKUP[b ^ (crc >> 8)]) & 0xFFFF

    return crc

