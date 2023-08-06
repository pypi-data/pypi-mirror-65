import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from omnitools import *


__ALL__ = ["AESCipher"]


class AESCipher(object):
    def __init__(self, key: str_or_bytes) -> None:
        if isinstance(key, str):
            key = utf8e(key)
        self.key = hashlib.sha256(key).digest()

    def encrypt(self, raw: str_or_bytes) -> str:
        raw = _pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64e(iv + cipher.encrypt(raw))

    def decrypt(self, enc: str) -> str_or_bytes:
        enc = b64d(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return _unpad(cipher.decrypt(enc[AES.block_size:]))


def _pad(s: str_or_bytes) -> bytes:
    gap = AES.block_size - len(s) % AES.block_size
    char = ""
    if isinstance(s, bytes):
        char = bytes(bytearray.fromhex(format(gap, "x").zfill(2)))
    else:
        char = chr(gap)
    s = s + char * gap
    return try_utf8e(s)


def _unpad(s: str_or_bytes) -> str_or_bytes:
    s = s[:-ord(s[len(s)-1:])]
    return try_utf8d(s)


