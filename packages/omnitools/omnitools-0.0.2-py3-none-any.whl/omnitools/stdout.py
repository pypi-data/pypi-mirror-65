import sys
from typing import *


__ALL__ = ["flush", "new_line", "out", "format_args", "p"]


def flush() -> None:
    sys.stdout.flush()


def out(s: str) -> None:
    sys.stdout.write(s)


def format_args(arg: Any) -> str:
    if isinstance(arg, str):
        return f"'{arg}'"
    elif isinstance(arg, int):
        return str(arg)
    elif isinstance(arg, float):
        arg = str(arg)
        if "e-" in arg:
            arg = arg.split("e-")
        else:
            return arg
        arg[0] = arg[0].replace(".", "")
        arg[1] = int(arg[1])
        arg = "0."+"0"*(arg[1]-1)+arg[0]
        return arg
    elif isinstance(arg, (list, tuple)):
        tmp = "[" if isinstance(arg, list) else "("
        for i in range(len(arg)):
            if i > 0:
                tmp += ", "
            tmp += format_args(arg[i])
        tmp += "]" if isinstance(arg, list) else ")"
        return tmp
    elif isinstance(arg, dict):
        tmp = "{"
        for i, item in enumerate(arg.items()):
            k, v = item
            if i > 0:
                tmp += ", "
            tmp += f"'{k}': "+format_args(v)
        tmp += "}"
        return tmp
    else:
        try:
            return f"{type(arg).__name__}({str(arg)})"
        except:
            return f"{type(arg).__name__}()"


def p(*args, end="\n") -> None:
    tmp = ""
    for arg in args:
        tmp += format_args(arg)
    if end == "\n":
        tmp += end
    out(tmp)
    flush()


