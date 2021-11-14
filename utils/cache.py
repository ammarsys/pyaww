"""Cache functions for the API wrapper"""

# Standard library imports

import datetime
import inspect

from functools import wraps
from typing import TypeVar, Callable

# Related third party imports

from typing_extensions import ParamSpec


T = TypeVar("T")
P = ParamSpec("P")


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

            if not args[0].use_cache:
                return func(*args, **kwargs)

            cache = args[0].cache

            siggy = inspect.signature(func).bind(*args, **kwargs)
            siggy.apply_defaults()
            params = tuple(siggy.arguments.values())

            time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)

            if func.__qualname__ in cache:
                if params in cache[func.__qualname__]:
                    cached_dict_value = cache[func.__qualname__][params]

                    if cached_dict_value[0] >= datetime.datetime.now():
                        return cached_dict_value[1]

                    del cache[func.__qualname__][params]  # expired
                else:
                    ret = func(*args, **kwargs)
                    cache[func.__qualname__][params] = (time, ret)
                    return ret
            else:
                ret = func(*args, **kwargs)
                cache[func.__qualname__] = {params: (time, ret)}
                return ret

            return func(*args, **kwargs)

        return wrapper

    return real_decorator
