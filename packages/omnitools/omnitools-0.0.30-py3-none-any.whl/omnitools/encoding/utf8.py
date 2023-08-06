from ..type import *

__ALL__ = ["utf8e", "utf8d", "try_utf8d"]


def utf8e(s: str) -> bytes:
    return s.encode("utf-8")


def utf8d(b: bytes) -> str:
    return b.decode("utf-8")


def try_utf8d(b: bytes) -> str_or_bytes:
    try:
        return utf8d(b)
    except:
        return b


