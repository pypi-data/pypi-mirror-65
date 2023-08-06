from hashlib import sha3_512
import hmac
from . import *


__ALL__ = ["sha512", "mac"]


def sha512(content: str_or_bytes) -> str:
    return sha3_512(try_utf8e(content)).hexdigest()


def mac(key: str_or_bytes, content: str_or_bytes) -> str:
    return hmac.new(try_utf8e(key), try_utf8e(content), sha3_512).hexdigest()


