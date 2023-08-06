import chardet
from .type import str_or_bytes
from base64 import b64decode, b64encode


__ALL__ = ["charenc"]


def charenc(b: str_or_bytes) -> str:
    if isinstance(b, str):
        try:
            b = b64d(b)
        except:
            b = b.encode("utf-8")
    return chardet.detect(b)["encoding"]


def b64e(s: str_or_bytes) -> str:
    if isinstance(s, str):
        return b64e(s.encode("utf-8"))
    return b64encode(s).decode("utf-8")


def b64d(s: str) -> str_or_bytes:
    try:
        return b64decode(s).decode("utf-8")
    except:
        return b64decode(s)

