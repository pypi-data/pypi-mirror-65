import chardet
from .type import *
from base64 import b64decode, b64encode


__ALL__ = ["charenc", "b64e", "b64d", "utf8e", "utf8d"]


def charenc(b: str_or_bytes) -> str:
    if isinstance(b, str):
        try:
            b = b64d(b)
        except:
            b = utf8e(b)
    return chardet.detect(b)["encoding"]


def b64e(s: str_or_bytes) -> str:
    if isinstance(s, str):
        return b64e(utf8e(s))
    return utf8d(b64encode(s))


def b64d(s: str) -> bytes:
    return b64decode(s)


def try_b64d(s: str) -> str_or_bytes:
    try:
        return b64d(s)
    except:
        return s


def utf8e(s: str) -> bytes:
    return s.encode("utf-8")


def utf8d(b: bytes) -> str:
    return b.decode("utf-8")


def try_utf8d(b: bytes) -> str_or_bytes:
    try:
        return utf8d(b)
    except:
        return b


def b64d_or_utf8e(v: str) -> bytes:
    try:
        return b64d(v)
    except:
        return utf8e(v)

