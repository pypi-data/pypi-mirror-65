from Crypto import Random
from Crypto.Cipher import AES
from omnitools import sha256d, str_or_bytes, b64e, b64d, try_utf8e, try_utf8d


__ALL__ = ["AESCipher"]


class AESCipher(object):
    def __init__(self, key: str_or_bytes) -> None:
        self.key = sha256d(key)

    def encrypt(self, raw: str_or_bytes) -> str:
        raw = try_utf8e(self.__pad(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64e(iv + cipher.encrypt(raw))

    def decrypt(self, enc: str) -> str_or_bytes:
        enc = b64d(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return try_utf8d(self.__unpad(cipher.decrypt(enc[AES.block_size:])))

    @staticmethod
    def __pad(s: str_or_bytes) -> str_or_bytes:
        gap = AES.block_size - len(s) % AES.block_size
        char = ""
        if isinstance(s, bytes):
            char = bytes(bytearray.fromhex(format(gap, "x").zfill(2)))
        else:
            char = chr(gap)
        s = s + char * gap
        return s

    @staticmethod
    def __unpad(s: str_or_bytes) -> str_or_bytes:
        s = s[:-ord(s[len(s)-1:])]
        return s


