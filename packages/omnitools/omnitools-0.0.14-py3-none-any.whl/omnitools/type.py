from typing import *


str_or_bytes = Union[str, bytes]
list_or_dict = Union[list, dict]
key_pair_format = Dict[str, bytes]
encryptedsocket_function = Dict[str, Callable[[Any], Any]]

