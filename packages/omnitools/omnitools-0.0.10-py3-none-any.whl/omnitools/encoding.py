import chardet


def encoding(b: bytes) -> str:
    return chardet.detect(b)["encoding"]

