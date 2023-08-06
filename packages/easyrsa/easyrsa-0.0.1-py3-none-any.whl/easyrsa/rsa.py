from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from omnitools import *


__ALL__ = ["EasyRSA"]


class EasyRSA(object):
    def __init__(self, bits: int = None, public_key: bytes = None, private_key: bytes = None) -> None:
        self.key = bits
        if self.key is not None:
            self.key = RSA.generate(bits=self.key)
        self.public_key = public_key
        self.private_key = private_key

    def gen_private_key(self, key_pair: key_pair_format):
        if self.public_key is None and self.private_key is None:
            key_pair["private_key"] = self.key.export_key()
        return self

    def gen_public_key(self, key_pair: key_pair_format):
        if self.public_key is None and self.private_key is None:
            key_pair["public_key"] = self.key.publickey().export_key()
        return self

    def encrypt(self, v: str_or_bytes) -> bytes:
        if self.key is None and self.private_key is None:
            if isinstance(v, str):
                v = v.encode()
            return PKCS1_OAEP.new(RSA.import_key(self.public_key)).encrypt(v)

    def decrypt(self, v: str_or_bytes) -> str_or_bytes:
        if self.public_key is None and self.key is None:
            try:
                from base64 import b64decode
                v = b64decode(v)
            except:
                pass
            v = PKCS1_OAEP.new(RSA.import_key(self.private_key)).decrypt(v)
            try:
                return v.decode()
            except UnicodeDecodeError:
                return v

