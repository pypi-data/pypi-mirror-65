import json
from typing import *


def jd(o: Any) -> str:
    return json.dumps(o)


def jl(s: str) -> Any:
    return json.loads(s)

