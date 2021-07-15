from typing import Any, Iterator
from typing_extensions import ParamSpec
from typing import TypeVar, Callable
import datetime

T = TypeVar("T")
P = ParamSpec("P")
_cache = {}

def flatten(items: Any) -> Iterator:
    """
    A function to "completely" flatten a list. For example, itertools.chain() would flatten it once but with recursion
    this function flattens it completely til it's a list with no nested lists.

    :param Any items: items to be flattened
    :return: Iterator with flattened items (nothing nested)
    """
    try:
        if isinstance(items, str): raise TypeError

        for i in items:
            yield from flatten(i)
    except TypeError:
        yield items

def cache_func(seconds: int = 300):
    def real_decorator(func: Callable[[P], T]) -> Callable[[P], T]:
        """
        Cache functions. Automatically adds to dictionary. Cache time is 5 minutes.

        :param func: function it's being decorated with
        """

        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            if func.__name__ not in _cache:
                _cache[func.__name__] = [None, None]
            cache = _cache[func.__name__]
            if cache[0] is None or datetime.datetime.now() > cache[1]:
                ret = func(*args, **kwargs)
                _cache[func.__name__] = [ret, datetime.datetime.now() + datetime.timedelta(seconds=seconds)]
                return ret
            else:
                return cache[0]
        return wrapper
    return real_decorator

def update_cached_function(corresponding_function: str):
    def real_decorator(func: Callable[[P], T]) -> Callable[[P], T]:
        """
        Update a cached function and next time it's ran ensure it's not of cache and up-to-date.

        :param func: function it's being decorated with
        """
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            ret = func(*args, **kwargs)
            _cache[corresponding_function] = [None, None]
            return ret
        return wrapper
    return real_decorator
