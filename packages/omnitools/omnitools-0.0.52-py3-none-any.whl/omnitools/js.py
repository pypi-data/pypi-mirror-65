import json
from typing import *


def jd(o: Any, **kwargs) -> str:
    return json.dumps(o, **kwargs)


def jl(s: str, **kwargs) -> Any:
    return json.loads(s, **kwargs)


def dumpobj(obj: Any, object: bool = False, indent: int = -1, indent_scale: int = 4) -> str:
    if indent >=0 and indent % indent_scale != 0:
        raise Exception(f"indent {indent} is not multiples of indent_scale {indent_scale}")

    def _dumpobj(obj: Any, object: bool = False, indent: int = -1, indent_scale: int = 4) -> str:
        if indent >=0 and indent % indent_scale != 0:
            raise Exception(f"indent {indent} is not multiples of indent_scale {indent_scale}")
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
                        indent += indent_scale
                for i, item in enumerate(obj):
                    if i:
                        tmp += ","
                        if not object:
                            tmp += " "
                    if object:
                        if indent >= 0:
                            tmp += "\n"
                            tmp += " "*indent
                    tmp += _dumpobj(item, object, indent, indent_scale)
                if object:
                    if indent >= 0:
                        tmp += "\n"
                        tmp += " "*(indent-indent_scale)
                tmp += "]" if isinstance(obj, list) else ")"
                return tmp
            elif isinstance(obj, dict):
                col = ": "
                if object:
                    tmp = "Obj({"
                    if indent >= 0:
                        indent += indent_scale
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
                    tmp += f'''{_dumpobj(k, object)}{col}{_dumpobj(v, object, indent, indent_scale)}'''
                if object:
                    if indent >= 0:
                        tmp += "\n"
                        tmp += " "*(indent-indent_scale)
                tmp += "}"
                if object:
                    tmp += ")"
                return tmp
            elif isinstance(obj, Obj):
                return obj.tostr(indent, indent_scale)
            else:
                return f'''{type(obj).__name__}({str(obj)})'''

    return " "*(indent*indent_scale)+_dumpobj(obj, object, indent, indent_scale)


