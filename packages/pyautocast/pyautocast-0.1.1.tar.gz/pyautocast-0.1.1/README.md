# pyautocast
Python library to automatically cast function arguments using decorator.

## Install

```bash
pip install pyautocast
```

## Usage

```py
>>> from pyautocast import autocast
>>> @autocast(x=str)
... def func(x):
...     assert(isinstance(x, str))
...     return "arg 'x' in func() is " + x
...
>>> func(2)
"arg 'x' in func() is 2"
>>> func([1, 2, 3])
"arg 'x' in func() is [1, 2, 3]"
```

```py
>>> from pyautocast import CustomCast
>>> mycast = CustomCast()
>>> mycast.add_cast_rule(int, tuple, lambda x: (x, x))
>>> @mycast.autocast(x=tuple)
... def func(x):
...     print(x)
>>> func(2)
(2, 2)
>>> func(-4.5)
Traceback (most recent call last):
...
TypeError: 'float' object is not iterable
```
