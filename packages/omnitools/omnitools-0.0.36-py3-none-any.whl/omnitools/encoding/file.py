import chardet
from ..type import *
from .utf8 import *
from .b64 import *


__ALL__ = ["charenc"]


def charenc(b: str_or_bytes) -> str:
    if isinstance(b, str):
        try:
            b = b64d(b)
        except:
            b = utf8e(b)
    return chardet.detect(b)["encoding"]


