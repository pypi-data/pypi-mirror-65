import chardet


def charenc(b: bytes) -> str:
    return chardet.detect(b)["encoding"]

