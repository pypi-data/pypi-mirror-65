import json
from typing import *


def jd(o: Any, **kwargs) -> str:
    return json.dumps(o, **kwargs)


def jl(s: str, **kwargs) -> Any:
    return json.loads(s, **kwargs)


def dumpobj(obj: Any, object: bool = False, indent: int = -1) -> str:
    indent_size = 4
    try:
        if not isinstance(obj, (tuple, list, dict)):
            return jd(obj)
        raise
    except:
        from .xtypes import Obj
        if isinstance(obj, bytes):
            return str(obj)
        elif isinstance(obj, (tuple, list)):
            tmp = "[" if isinstance(obj, list) else "("
            if object:
                if indent >= 0:
                    indent += indent_size
            for i, item in enumerate(obj):
                if i:
                    tmp += ","
                    if not object:
                        tmp += " "
                if object:
                    if indent >= 0:
                        tmp += "\n"
                        tmp += " "*indent
                tmp += dumpobj(item, object, indent)
            if object:
                if indent >= 0:
                    tmp += "\n"
                    tmp += " "*(indent-indent_size)
            tmp += "]" if isinstance(obj, list) else ")"
            return tmp
        elif isinstance(obj, dict):
            col = ": "
            if object:
                tmp = "Obj({"
                if indent >= 0:
                    indent += indent_size
            else:
                tmp = "{"
            for i, (k, v) in enumerate(obj.items()):
                if i:
                    tmp += ","
                    if not object:
                        tmp += " "
                if object:
                    if indent >= 0:
                        tmp += "\n"
                        tmp += " "*indent
                tmp += f'''{dumpobj(k, object)}{col}{dumpobj(v, object, indent)}'''
            if object:
                if indent >= 0:
                    tmp += "\n"
                    tmp += " "*(indent-indent_size)
            tmp += "}"
            if object:
                tmp += ")"
            return tmp
        elif isinstance(obj, Obj):
            return obj.str(indent)
        else:
            return f'''{type(obj).__name__}({str(obj)})'''


# z=Obj({
#     "a": (
#         0,
#         [
#             1,
#             Obj({
#                 "b": Obj({
#                     "c": 2,
#                     "d": b"3"
#                 })
#             })
#         ]
#     )
# })
# print(z)
# print(dumpobj(z))
#
# print(z.a[1][1].b.c)
# print(z.a[1][1].b.d)
