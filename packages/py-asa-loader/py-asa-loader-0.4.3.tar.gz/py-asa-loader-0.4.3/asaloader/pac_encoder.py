from .pac_const import *
import enum


def pac_encode(pac):
    chksum = sum(pac['data']) % 256

    res = bytes()
    res += HEADER
    res += pac['command'].to_bytes(1, 'little')
    res += TOCKEN
    res += len(pac['data']).to_bytes(2, 'big')
    res += pac['data']
    res += chksum.to_bytes(1, 'little')
    return res
