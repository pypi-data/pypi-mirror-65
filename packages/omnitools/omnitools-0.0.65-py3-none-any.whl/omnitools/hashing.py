from hashlib import sha3_512, sha3_256
import hmac
from . import str_or_bytes, try_utf8e


__ALL__ = ["sha512", "mac"]


def sha256d(content: str_or_bytes) -> bytes:
    return sha3_256(try_utf8e(content)).digest()


def sha512(content: str_or_bytes) -> str:
    return sha3_512(try_utf8e(content)).hexdigest()


def mac(key: str_or_bytes, content: str_or_bytes, method=sha3_512) -> str:
    return hmac.new(try_utf8e(key), try_utf8e(content), method).hexdigest()


