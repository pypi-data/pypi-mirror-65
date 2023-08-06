import json
from typing import *


def jd(o: Any, **kwargs) -> str:
    return json.dumps(o, **kwargs)


def jl(s: str, **kwargs) -> Any:
    return json.loads(s, **kwargs)


def dumpobj(obj: Any) -> str:
    try:
        if not isinstance(obj, (tuple, list, dict)):
            return jd(obj)
        raise
    except:
        if isinstance(obj, (tuple, list)):
            tmp = "[" if isinstance(obj, list) else "("
            for i, item in enumerate(obj):
                if i:
                    tmp += ", "
                tmp += dumpobj(item)
            tmp += "]" if isinstance(obj, list) else ")"
            return tmp
        elif isinstance(obj, dict):
            tmp = "{"
            for i, (k, v) in enumerate(obj.items()):
                if i:
                    tmp += ", "
                tmp += f'''{dumpobj(k)}: {dumpobj(v)}'''
            tmp += "}"
            return tmp
        else:
            return f'''{type(obj).__name__}({str(obj)})'''




