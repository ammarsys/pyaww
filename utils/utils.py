"""Helper functions for the API wrapper"""

# Standard library imports
import datetime
from functools import wraps
from typing import (
    Any,
    Iterator,
    TypeVar,
    Callable
)

# Related third party imports
from typing_extensions import ParamSpec

T = TypeVar("T")
P = ParamSpec("P")

cache = {}
ratelimit = {}


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
    def real_decorator(func: Callable[[P], T]) -> Callable[[P], T]:
        """The actual decorator"""
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            """The wrapper"""
            if func.__name__ not in cache:
                cache[func.__name__] = [None, None]

            cached_dict_value = cache[func.__name__]

            if cached_dict_value[0] is None or datetime.datetime.now() > cached_dict_value[1]:
                ret = func(*args, **kwargs)
                cache[func.__name__] = [ret, datetime.datetime.now() + datetime.timedelta(seconds=seconds)]
                return ret
            else:
                return cached_dict_value[0]

        return wrapper
    return real_decorator


def update_cached_function(corresponding_function: str) -> Callable:
    """
    Update a cached function and next time it's ran ensure it's not of cache and up-to-date.

    Args:
        corresponding_function (str): corresponding function to update

    Returns:
        Callable
    """
    def real_decorator(func: Callable[[P], T]) -> Callable[[P], T]:
        """The actual decorator"""
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            """The wrapper"""
            ret = func(*args, **kwargs)
            cache[corresponding_function] = [None, None]
            return ret

        return wrapper
    return real_decorator
