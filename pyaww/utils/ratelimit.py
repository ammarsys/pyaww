# Standard library imports

import datetime
from dataclasses import dataclass
from typing import Callable, TypeVar
import time

# Related third party imports

from typing_extensions import ParamSpec

# Local library/Library specific imports

from ..errors import raise_error

T = TypeVar("T")
P = ParamSpec("P")


@dataclass
class URL:
    http_requests: list[datetime.datetime]
    max_requests: int


class RateLimiter:
    def __init__(self, default: int = 60):
        self.limit: dict[str, tuple[datetime.datetime, URL]] = {}
        self.default = default


def ratelimit(func: Callable[P, T]) -> Callable[P, T]:
    """WIP"""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        """WIP"""

        url = args[1] if not "url" in kwargs else kwargs["url"]
        rl: RateLimiter = args[0].ratelimiter
        max_ = rl.default
        url_class = rl.limit[url]

        if url in rl.limit:
            rl.limit[url][1].http_requests.append(datetime.datetime.now())

            if (
                len(url_class[1].http_requests) >= max_
                and url_class[1].http_requests[-1] <= url_class[0]
            ):
                # ratelimited
                time.sleep((url_class[0] - datetime.datetime.now()).total_seconds())
            else:
                del rl.limit[url]

        else:
            rl.limit[url] = (
                datetime.datetime.now() + datetime.timedelta(seconds=1),
                URL([datetime.datetime.now()], max_),
            )

        return func(*args, **kwargs)

    return wrapper
