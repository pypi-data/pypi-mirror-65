import chardet
from .type import str_or_bytes


def charenc(b: str_or_bytes) -> str:
    if isinstance(b, str):
        try:
            from base64 import b64decode
            b = b64decode(b)
        except:
            b = b.encode("utf-8")
    return chardet.detect(b)["encoding"]

