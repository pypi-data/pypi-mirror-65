# Omnitools

<badges>[![version](https://img.shields.io/pypi/v/omnitools.svg)](https://pypi.org/project/omnitools/)
[![license](https://img.shields.io/pypi/l/omnitools.svg)](https://pypi.org/project/omnitools/)
[![pyversions](https://img.shields.io/pypi/pyversions/omnitools.svg)](https://pypi.org/project/omnitools/)  
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>Miscellaneous functions written in short forms.</i>

# Hierarchy
```
omnitools
|---- encoding
|   |---- b64
|   |   |---- b64d()
|   |   |---- b64e()
|   |   |---- try_b64d()
|   |   '---- b64d_or_utf8e()
|   |---- file
|   |   '---- charenc()
|   '---- utf8
|       |---- utf8d()
|       |---- utf8e()
|       |---- try_utf8d()
|       '---- try_utf8e()
|---- hashing
|   |---- mac()
|   '---- sha512()
|---- rng
|   |---- randb()
|   '---- randi()
|---- stdout
|   '---- p()
'---- type
    |---- str_or_bytes
    |---- list_or_dict
    |---- key_pair_format
    |---- encryptedsocket_function
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

# base64 decode
p(b64d(b64e("test")))
# test

# base64 encode
p(b64e("test"))
# dGVzdA==

# try b64d str except return itself
p(try_b64d("test"))
# test

# try b64d str except utf8e str
p(b64d_or_utf8e(randb(64)))
# b"..."

# detect character encoding
p(charenc(b"\xe3\x81\x82"))
# utf-8

# utf8 decode
p(utf8d(utf8e("test")))
# test

# utf8 encode
p(utf8e("test"))
# b"test"

# try utf8d bytes except return itself
p(try_utf8d("test"))

# try utf8e str except return itself
p(try_utf8e(randb(64)))

# hash mac with hmac, sha3_512
p(mac(content="test", key=randb(64)))
# ...

# hash with sha3_512
p(sha512("test"))
# ...

# generate random 64 bytes
p(randb(64))
# b"..."

# generate int from 10**power to 10**(power+1)-1
p(randi(power=2))
# 101 # from 100 to 999

# turn (nested) dict into an object
p(Obj({"a":{"b":{"c":123}}}).a.b.c)
# 123
```

## shell
```shell script
rem omnitools.exe <function name> [argument] ...
omnitools.exe p abc
```