import os
import random


__ALL__ = ["gen_bytes", "randno"]


def gen_bytes(size=64):
    return os.urandom(size)


def randno(power: int = 6) -> int:
    power = int(power)
    return random.randint(10 ** power, 10 ** (power + 1) - 1)

