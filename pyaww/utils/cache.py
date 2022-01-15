"""TTL Cache functions for the API wrapper"""

# Standard library imports

import datetime
import asyncio

from typing import (
    Optional,
    TYPE_CHECKING,
    Generic,
    TypeVar,
    Hashable,
    Generator,
    Union,
    Any,
)
from collections.abc import MutableMapping

# Local application/library specific imports

if TYPE_CHECKING:
    from pyaww import Console, SchedTask


KT = TypeVar("KT", bound=Hashable)
VT = TypeVar("VT")


def _check_if_expired(item: datetime.datetime) -> bool:
    """Check if a record has expired"""
    return item <= datetime.datetime.now()


def _time(seconds: int) -> datetime.datetime:
    """Make a timedelta in the future"""
    return datetime.datetime.now() + datetime.timedelta(seconds=seconds)


class TTLCache(MutableMapping[KT, VT], Generic[KT, VT]):
    """
    TTL (time-to-live) cache for pyaww module. This class is utilised inside pyaww.utils.Cache. Records may expire
    upon interacting with them (__getitem__ and __contains__.)

    Ordinary format for the cache instance variable is the submodule initialized class id and the initialized class.
    """

    def __init__(self, ttl_time: int = 30):
        self.ttl = ttl_time
        self.cache: dict[KT, tuple[VT, datetime.datetime]] = {}

    def __getitem__(self, item: KT) -> Optional[VT]:
        if item not in self:
            raise KeyError

        return self.cache[item][0]

    def __contains__(self, item: KT) -> bool:
        try:
            _, dt = self.cache[item]

            if not _check_if_expired(dt):
                return True
        except KeyError:
            return False
        return False

    def __setitem__(self, key: KT, value: VT) -> None:
        self.cache[key] = (value, _time(self.ttl))

    def __len__(self) -> int:
        return len(self.cache)

    def __iter__(self) -> Generator:
        yield from self.cache

    def __delitem__(self, key: KT) -> None:
        del self.cache[key]

    def pop(self, key: KT) -> VT:
        return self.cache.pop(key)

    async def natural_values(self) -> list[VT]:
        return [data[0] for data in self.cache.values()]


class Cache:
    def __init__(self):
        """
        Main caching class for the module.

        Each "type" (submodule) has its own get, set, delete, get_all and a record in the _submodule_dict instance variable
        . The types in question are, pyaww.Console, pyaww.AlwaysOnTask, pyaww.StaticFile, pyaww.StaticHeader,
        pyaww.WebApp and pyaww.File. Alongside each type, an instance variable (format: _type_cache) representing its cache will be created with the value
        being initialized pyaww.TTLCache.

        Anti-race-condition measures are taken into count here via asyncio.Lock().
        """
        self.lock = asyncio.Lock()

        self._console_cache: TTLCache[int, "Console"] = TTLCache()
        self._sched_task_cache: TTLCache[int, "SchedTask"] = TTLCache()

        self._submodule_dict: dict[str, TTLCache] = {
            "console": self._console_cache,
            "sched_task": self._sched_task_cache,
        }  # PA support 3.10 smh

    async def all(self, submodule: str) -> list[Any]:
        type_ = self._submodule_dict[submodule]
        return await type_.natural_values()

    async def get(self, submodule: str, id_: int) -> Optional[Any]:
        type_ = self._submodule_dict[submodule]
        return type_.get(id_, None)

    async def pop(self, submodule: str, id_: int) -> None:
        type_ = self._submodule_dict[submodule]

        async with self.lock:
            type_.pop(id_)

    async def set(self, submodule: str, object_: Union[Any, list[Any]]):
        type_ = self._submodule_dict[submodule]

        async with self.lock:
            if not isinstance(object_, list):
                object_ = [object_]

            for object_ in object_:
                if object_.id in type_:
                    continue  # present in cache, unnecessary calls

                type_[object_.id] = object_
