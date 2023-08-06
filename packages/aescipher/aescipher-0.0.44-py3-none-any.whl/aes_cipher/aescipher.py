import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from typing import *


__ALL__ = ["AESCipher"]


str_or_bytes = Union[str, bytes]


class AESCipher(object):
    def __init__(self, key: str_or_bytes) -> None:
        if isinstance(key, str):
            key = key.encode()
        self.key = hashlib.sha256(key).digest()

    def encrypt(self, raw: str_or_bytes) -> str:
        raw = _pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode()

    def decrypt(self, enc: str) -> str_or_bytes:
        enc = base64.b64decode(enc)
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
    if isinstance(s, str):
        return s.encode("utf-8")
    return s


def _unpad(s: str_or_bytes) -> str_or_bytes:
    s = s[:-ord(s[len(s)-1:])]
    try:
        return s.decode("utf-8")
    except UnicodeDecodeError:
        return s


