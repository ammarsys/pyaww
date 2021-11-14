"""Helper functions for the API wrapper"""

# Standard library imports

import datetime

from functools import wraps
from typing import Any, Iterator, TypeVar, Callable

# Related third party imports

from typing_extensions import ParamSpec

# Local application/library specific imports

# from pyaww.errors import raise_error

T = TypeVar("T")
P = ParamSpec("P")


def flatten(items: Any) -> Iterator:
    """
    A function to "completely" flatten a list. For example, itertools.chain() would flatten it once but with recursion
    this function flattens it completely til it's a list with no nested lists.

    Args:
        items (Any): items to be flattened

    Returns:
        Iterator: Iterator with flattened items (nothing nested)
    """
    try:
        if isinstance(items, str):
            raise TypeError

        for i in items:
            yield from flatten(i)
    except TypeError:
        yield items


def cache_func(seconds: int = 300) -> Callable:
    """
    Cache functions. Automatically adds to dictionary. Cache time is 5 minutes by default.

    Args:
        seconds (int): TTL for the cached version of the function

    Returns:
        Callable
    """

    def real_decorator(func: Callable[P, T]) -> Callable[P, T]:
        """The actual decorator"""

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            """The wrapper"""

            cache = args[0].cache

            if not args[0].use_cache:
                return func(*args, **kwargs)

            try:
                hash()
            if (func.__qualname__, (args, tuple(kwargs.items()))) not in cache:
                ret = func(*args, **kwargs)

                cache[(func.__qualname__, (args, tuple(kwargs.items())))] = [
                    ret,
                    datetime.datetime.now() + datetime.timedelta(seconds=seconds),
                ]

                return ret

            cached_dict_value = cache[
                (func.__qualname__, (args, tuple(kwargs.items())))
            ]

            if cached_dict_value[1] >= datetime.datetime.now():
                return cached_dict_value[0]

            del cache[(func.__qualname__, (args, tuple(kwargs.items())))]  # expired

        return wrapper

    return real_decorator
