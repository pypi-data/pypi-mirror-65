from hashlib import sha3_512
import hmac
from . import *


__ALL__ = ["sha512", "mac"]


def sha512(content: str_or_bytes) -> str:
    if isinstance(content, str):
        content = content.encode("utf-8")
    return sha3_512(content).hexdigest()


def mac(content: str_or_bytes, key: str_or_bytes) -> str:
    if isinstance(content, str):
        content = content.encode("utf-8")
    if isinstance(key, str):
        key = key.encode("utf-8")
    return hmac.new(key, content, sha3_512).hexdigest()
