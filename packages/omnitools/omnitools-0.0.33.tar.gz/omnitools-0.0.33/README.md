# Omnitools

<i>Miscellaneous functions written in short forms.</i> &#10084; UTF8

# Hierarchy
```
omnitools
|---- p()
|---- charenc()
'---- Obj()
```

# Example

## python
```python
from omnitools import *

# print and always flush buffer
p("abc")
# abc
# 

# detect character encoding
p(charenc(b"\xe3\x81\x82"))
# utf-8

# turn (nested) dict into an object
p(Obj({"a":{"b":{"c":123}}}).a.b.c)
# 123
```

## shell
```shell script
rem omnitools.exe <function name> [argument] ...
omnitools.exe p abc
```