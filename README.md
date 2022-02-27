# Tmlog

Python Time logger based on pure python time module.

## usage

```
from Tmlog import Lg
with Lg("test code 1"):
    sleep(10)

with Lg("test code 2") as lg:
    for i in range(10):
        with lg.stk("inner case 1"):
            sleep(10)
        
        with lg.stk("inner case 2"):
            sleep(5)


>> [test code 1] time pasts: 10.00 seconds
>> [test code 2] time pasts: 150.00 seconds
        inner case 1: 100 sec
        inner case 2: 50 sec
```