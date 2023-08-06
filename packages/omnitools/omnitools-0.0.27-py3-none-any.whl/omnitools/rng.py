import os


__ALL__ = ["gen_bytes"]


def gen_bytes(size=64):
    return os.urandom(size)

