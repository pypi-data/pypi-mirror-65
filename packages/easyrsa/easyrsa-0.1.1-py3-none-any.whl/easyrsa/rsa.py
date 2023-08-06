from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA3_512
from Crypto.Signature import PKCS1_v1_5
from omnitools import *


__ALL__ = ["EasyRSA"]


class EasyRSA(object):
    def __init__(self, bits: int = None,
                 public_key: str_or_bytes = None,
                 private_key: str_or_bytes = None) -> None:
        self.key = bits
        if self.key is not None:
            self.key = RSA.generate(bits=self.key)
        self.public_key = public_key
        if isinstance(self.public_key, str):
            self.public_key = try_b64d(self.public_key)
        self.private_key = private_key
        if isinstance(self.private_key, str):
            self.private_key = try_b64d(self.private_key)

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
            v = try_utf8e(v)
            return PKCS1_OAEP.new(RSA.import_key(self.public_key)).encrypt(v)

    def decrypt(self, v: str_or_bytes) -> str_or_bytes:
        if self.public_key is None and self.key is None:
            if isinstance(v, str):
                v = b64d_or_utf8e(v)
            v = PKCS1_OAEP.new(RSA.import_key(self.private_key)).decrypt(v)
            return try_utf8d(v)

    def sign(self, v: str_or_bytes) -> bytes:
        if self.public_key is None and self.key is None:
            return PKCS1_v1_5.new(RSA.import_key(self.private_key)).sign(SHA3_512.new(try_utf8e(v)))

    def verify(self, v: str_or_bytes, s: bytes) -> bool:
        if self.key is None and self.private_key is None:
            return PKCS1_v1_5.new(RSA.importKey(self.public_key).publickey()).verify(SHA3_512.new(try_utf8e(v)), s)


