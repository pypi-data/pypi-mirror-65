import json
from typing import *


__ALL__ = ["jo", "jl", "dumpobj"]


def jd(o: Any, **kwargs) -> str:
    return json.dumps(o, **kwargs)


def jl(s: str, **kwargs) -> Any:
    return json.loads(s, **kwargs)


def _dumpobj(obj: Any, isObj: bool = False, indent: int = -1, indent_scale: int = 4) -> str:
    do_indent = True if indent >= 0 else False
    if indent >= 0 and indent % indent_scale != 0:
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
            if do_indent:
                if indent >= 0:
                    indent += indent_scale
            for i, item in enumerate(obj):
                if i:
                    tmp += ","
                    if not do_indent:
                        tmp += " "
                if do_indent:
                    if indent >= 0:
                        tmp += "\n"
                        tmp += " "*indent
                tmp += _dumpobj(item, indent=indent, indent_scale=indent_scale)
            if do_indent:
                if indent >= 0:
                    tmp += "\n"
                    tmp += " "*(indent-indent_scale)
            tmp += "]" if isinstance(obj, list) else ")"
            return tmp
        elif isinstance(obj, dict):
            col = ": "
            if do_indent:
                tmp = "Obj({" if isObj else "{"
                if indent >= 0:
                    indent += indent_scale
            else:
                tmp = "{"
            for i, (k, v) in enumerate(obj.items()):
                if i:
                    tmp += ","
                    if not do_indent:
                        tmp += " "
                if do_indent:
                    if indent >= 0:
                        tmp += "\n"
                        tmp += " "*indent
                tmp += f'''{_dumpobj(k)}{col}{_dumpobj(v, indent=indent, indent_scale=indent_scale)}'''
            if do_indent:
                if indent >= 0:
                    tmp += "\n"
                    tmp += " "*(indent-indent_scale)
            tmp += "}"
            if do_indent:
                tmp += ")"
            return tmp
        elif isinstance(obj, Obj):
            return obj.dump(indent=indent, indent_scale=indent_scale)
        else:
            return f'''{type(obj).__name__}({str(obj)})'''


def dumpobj(obj: Any, isObj: bool = False, indent: int = -1, indent_scale: int = 4) -> str:
    if indent >= 0 and indent % indent_scale != 0:
        raise Exception(f"indent {indent} is not multiples of indent_scale {indent_scale}")
    import inspect
    stack = [a[3] for a in inspect.stack()]
    dumpobjsize = len([_ for _ in stack if _ == inspect.stack()[1][3]])
    dumpsize = len([_ for _ in stack if _ == "dump"])
    stack.reverse()
    try:
        dumpstack = stack.index("dump")
    except:
        import sys
        dumpstack = sys.maxsize * 2 + 1
    try:
        dumpobjstack = stack.index(inspect.stack()[1][3])
    except:
        import sys
        dumpobjstack = sys.maxsize * 2 + 1
    spacing = ""
    if (dumpobjstack < dumpstack and dumpsize == 0 and dumpobjsize == 1) or \
            (dumpobjstack == dumpstack and dumpsize == dumpobjsize == 1):
        spacing = " "*indent
    return spacing+_dumpobj(obj, isObj, indent, indent_scale)


