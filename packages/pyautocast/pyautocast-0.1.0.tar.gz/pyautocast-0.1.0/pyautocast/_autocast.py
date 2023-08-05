import inspect
import functools
from typing import OrderedDict, Tuple


def _cast(
        obj: object,
        cast_to: type,
        cast_rules: OrderedDict[Tuple[type, type], callable]):
    for (input_type, output_type), func in cast_rules.items():
        if isinstance(obj, input_type):
            return func(obj)
    else:
        return cast_to(obj)


def _autocast(
        cast_rules: OrderedDict[Tuple[type, type], callable] = {},
        **cast_to: type) -> callable:

    def wrapper(func: callable) -> callable:
        argspec = inspect.getfullargspec(func)
        arg_names = argspec.args
        for key, value in cast_to.items():
            if key not in arg_names:
                raise ValueError(
                    f"arg '{key}' not found in {func.__name__}().")
            if not isinstance(value, type):
                raise TypeError(
                    f"Cast destination of arg '{key}' in {func.__name__}() "
                    "must be an instance of type.")

        @functools.wraps(func)
        def _func_with_typecast(*args, **kwargs):
            args_casted = []
            for name, arg in zip(arg_names, args):
                if name in cast_to:
                    args_casted.append(_cast(arg, cast_to[name], cast_rules))
                else:
                    args_casted.append(arg)
            kwargs_casted = {}
            for name, arg in kwargs.items():
                if name in cast_to:
                    kwargs_casted[name] = _cast(arg, cast_to[name], cast_rules)
                else:
                    kwargs_casted[name] = arg
            return func(*args_casted, **kwargs_casted)

        _func_with_typecast.__signature__ = inspect.signature(func)
        return _func_with_typecast

    return wrapper


def autocast(**cast_to: type) -> callable:
    """Decorator to automatically cast function arguments.

    Parameters
    ----------
    cast_to : type
        Specifies casting destination of arguments.

    Returns
    -------
    callable
        Function with type casting.

    Example
    -------
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
    """
    return _autocast({}, **cast_to)
