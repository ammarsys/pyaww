"""TTL Cache functions for the API wrapper"""

# Standard library imports

import datetime

from typing import TypeVar, Any, Union, Optional
from dataclasses import dataclass
from collections.abc import Mapping

# Related third party imports

from typing_extensions import ParamSpec

T = TypeVar("T")
P = ParamSpec("P")


@dataclass(frozen=True, eq=True)
class CachedResponse:
    params: tuple
    future: datetime.datetime
    ret: Any


class URLCache(Mapping):
    """
    TTL cache for URLs. This class should be used inside a regular dictionary in the following style,

    >>> {'www.domain.com/api/v0/thing': URLCache(...)}

    Keys/Values expire (get deleted) when you interact with them. In other words, when you call __getitem__ or
    __contains__, the item will be checked to see if it's an instance of utils.cache.CachedResponse if it is,
    see if the timedelta in the future is less than now, if it is, meaning its expired, pop the value and raise a
    KeyError. Instances other than CachedResponse are ignored.
    """

    def __init__(
        self,
        name: str,
        max_len: Union[float, int] = float("inf"),
        to_cache: tuple = None,
    ):  # Defaulting max_len because of the update_cache function
        self.name = name
        self.max_len = max_len
        self.cache: dict[tuple, CachedResponse] = {}

        if to_cache:
            self.__setitem__(*to_cache)

    def __check_if_expired(self, item: CachedResponse) -> Optional[None]:
        """Method to see if a key has expired, private because it can mess with caching."""
        if item.future <= datetime.datetime.now():
            self.cache.pop(item.params)
            raise KeyError

    def __getitem__(self, item):
        item = self.cache[item]

        if isinstance(item, CachedResponse):
            self.__check_if_expired(item)

        return item

    def __contains__(self, item):
        try:
            item = self.cache[item]
            if isinstance(item, CachedResponse):
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
