import functools

import time
from typing import NoReturn
from xmlrpc.client import boolean
from pyaww.errors import raise_error, raise_limit_error_and_await
from datetime import datetime, timedelta

SLEEPING_TIME = 5
class Route:
    def __init__(self, url) -> None:
        self.limit = 50
        self.calls = 0
        self.url = url
        self.timer_end = datetime.now()

    async def sleep(self) -> None:
        now = datetime.now()
        self.timer_end = now + timedelta(minutes = SLEEPING_TIME)
        time.sleep(60 * SLEEPING_TIME)
        self.calls = 0

    def sleep_until(self) -> datetime:
        return self.timer_end

    def callable(self) -> bool:
        if self.calls >= self.limit:
            self.sleep()
            return False
        self.calls += 1
        return True


routes = {}

def limiter(url: str) -> None:
    #how to get route
    if url not in routes:
        routes[url] = Route(url)
    if routes[url].callable() == False:
        raise_limit_error_and_await(routes[url])