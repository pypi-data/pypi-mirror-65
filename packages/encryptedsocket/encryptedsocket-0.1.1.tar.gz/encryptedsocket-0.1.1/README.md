# Encrypted Socket

<badges>![version](https://img.shields.io/pypi/v/encryptedsocket.svg)
![license](https://img.shields.io/pypi/l/encryptedsocket.svg)
![pyversions](https://img.shields.io/pypi/pyversions/encryptedsocket.svg)
![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)
![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)
</badges>

<i>Secured yet simple socket server-client for interprocess communications.</i>

# Hierarchy

```
encryptedsocket
|---- SS()
|   |---- start()
|   '---- stop()
'---- SC()
    '---- request()
```

# Example

## python
```python
# You can start an unencrypted socket server
# if you know what you are doing
# SS(host="remote ip", port=12321, encrypted=False)
# SC(host="remote ip", port=12321, encrypted=False)

# You can transmit objects as long as
# both sides have access to their classes

from encryptedsocket import *

# server
def test(data):
    return f"Data:\t{data}"
functions = dict(test=test)
SS(functions=functions).start()
print("test socket server started.", flush=True)
# # Nothing is printed, you must start it from an other thread

# client
for i in range(5):
    print(SC().request(command="test", data=f"Hello, {i}!"))
print("test socket client started.", flush=True)
# Data:   Hello, 0!
# Data:   Hello, 1!
# Data:   Hello, 2!
# Data:   Hello, 3!
# Data:   Hello, 4!
# test socket client started.
```

## shell
```shell script
rem encryptedsocket.exe {server|client}
rem echo test server-client example
encryptedsocket.exe server
encryptedsocket.exe client
```