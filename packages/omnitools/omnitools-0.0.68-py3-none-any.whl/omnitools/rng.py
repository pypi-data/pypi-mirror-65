import os
import random


__ALL__ = ["randb", "randi"]


def randb(size=64):
    return os.urandom(size)


def randi(power: int = 6) -> int:
    power = int(power)
    return random.randint(10 ** power, 10 ** (power + 1) - 1)

