from typing import *


__ALL__ = ["str_or_bytes", "list_or_dict", "key_pair_format", "encryptedsocket_function", "Obj"]


str_or_bytes = Union[str, bytes]
list_or_dict = Union[list, dict]
key_pair_format = Dict[str, bytes]
encryptedsocket_function = Dict[str, Callable[[Any], Any]]


class Obj(object):
    """
    @DynamicAttrs
    """
    def __init__(self, a):
        self._org = a
        for b, c in a.items():
            if isinstance(c, (list, tuple)):
               setattr(self, b, [Obj(x) if isinstance(x, dict) else x for x in c])
            else:
               setattr(self, b, Obj(c) if isinstance(c, dict) else c)


