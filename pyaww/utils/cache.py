"""TTL Cache functions for the API wrapper"""

# Standard library imports

import datetime
import inspect

from functools import wraps
from typing import TypeVar, Callable, Any, Union, Optional, Awaitable
from dataclasses import dataclass
from collections.abc import Mapping

# Related third party imports

from typing_extensions import ParamSpec


T = TypeVar("T")
P = ParamSpec("P")


@dataclass(frozen=True, eq=True)
class CachedRecord:
    """Cache records; used for utils.cache.FunctionCache and utils.cache.cache_func"""

    params: tuple
    future: datetime.datetime
    ret: Any


class FunctionCache(Mapping):
    """
    TTL cache for functions. This class must be used inside a regular dictionary in the following style,

    >>> {"bar.foo": FunctionCache(...)}

    Keys/Values expire (get deleted) when you interact with them. In other words, when you call __getitem__,
    __contains__ etc. the item will be checked to see if it's an instance of utils.cache.CachedRecord if it is,
    see if the timedelta in the future is less than now, if it is, meaning its expired, pop the value and raise a
    KeyError. Instances other than CachedRecord are ignored.
    """

    def __init__(
        self, name: str, max_len: Union[float, int], to_cache: tuple = None
    ):  # No need to default max_len since it gets passed from utils.cache.cache_func and it's defaulted there.
        self.name = name
        self.max_len = max_len
        self.cache: dict[tuple, CachedRecord] = {}

        if to_cache:
            self.__setitem__(*to_cache)

    def __check_if_expired(self, item: CachedRecord) -> Optional[None]:
        """Method to see if a key has expired, private because it can mess with caching."""
        if item.future <= datetime.datetime.now():
            self.cache.pop(item.params)
            raise KeyError

    def __getitem__(self, item):
        item = self.cache[item]

        if isinstance(item, CachedRecord):
            self.__check_if_expired(item)

        return item

    def __contains__(self, item):
        try:
            item = self.cache[item]
            if isinstance(item, CachedRecord):
                if not self.__check_if_expired(item):
                    return item in self.cache
        except KeyError:
            return False
        return False

    def __setitem__(self, key, value):
        if len(self.cache) >= self.max_len:  # max values and/or old values
            self.cache.pop(list(self.cache)[0])

        self.cache[key] = value

    def __len__(self):
        return len(self.cache)

    def __iter__(self):
        yield from self.cache


def cache_func(
    seconds: Union[int, float] = 300, max_len: Union[int, float] = float("inf")
) -> Callable:
    """
    Cache functions. Cache time is 5 minutes by default.

    The user is able to disable this caching via pyaww.User.use_cache or disable a specific method from being cached
    by appending the qualname of the function to the pyaww.User.disable_cache. Cached instances are stored in a
    dictionary which keys are the functions qualname(s) and it's values an utils.cache.FunctionCache object.
    The time-to-live of values is handled inside the utils.cache.FunctionCache objects.

    Passed function in this deco must be a class instance (have self as it's first attribute) and that class must
    contain "disable_cache", "use_cache", "cache" and "lock" instance variables. Please see how they're defined in the
    example bellow.

    Examples:
        >>> import asyncio
        >>>
        >>> class Foo:
        >>>    def __init__(self):
        >>>         self.cache = {}
        >>>         self.use_cache = True
        >>>         self.disable_cache = ()
        >>>         self.lock = asyncio.Lock()
        >>>
        >>>    @cache_func(seconds=1)
        >>>    async def bar(self, baz):
        >>>         print("I was ran.")
        >>>         return baz + 1

    Args:
        max_len (Union[float, int] = float('inf')): maximum number of cached records
        seconds (Union[int, float]): TTL for the cached version of the function

    Returns:
        Callable
    """

    def real_decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        """The actual decorator, the function is expected to be an awaitable."""

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Awaitable[T]:
            """The wrapper"""

            if not args[0].use_cache or func.__qualname__ in args[0].disable_cache:
                return await func(*args, **kwargs)

            cache = args[0].cache
            lock = args[0].lock

            siggy = inspect.signature(func).bind(*args, **kwargs)
            siggy.apply_defaults()
            params = tuple(siggy.arguments.values())

            time_ = datetime.datetime.now() + datetime.timedelta(seconds=seconds)

            if func.__qualname__ in cache:
                try:
                    return cache[func.__qualname__][params].ret
                except KeyError:
                    ret = await func(*args, **kwargs)
                    async with lock:
                        cache[func.__qualname__][params] = CachedRecord(params, time_, ret)
                    return ret
            else:
                ret = await func(*args, **kwargs)
                async with lock:
                    cache[func.__qualname__] = FunctionCache(
                        name=func.__qualname__,
                        to_cache=(params, CachedRecord(params, time_, ret)),
                        max_len=max_len,
                    )
                return ret

        return wrapper

    return real_decorator
