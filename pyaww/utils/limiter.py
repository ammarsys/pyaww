import functools

import time
from pyaww.errors import raise_error
from datetime import datetime, timedelta

SLEEPING_TIME = 5
class Route:
    def __init__(self):
        self.limit = 50
        self.calls = 0
        self.timer_end = datetime.now()

    async def sleep(self):
        now = datetime.now()
        self.timer_end = now + timedelta(minutes = SLEEPING_TIME)
        time.sleep(60 * SLEEPING_TIME)
        self.calls = 0

    def sleep_until(self):
        return self.timer_end

    def callable(self):
        if self.calls >= self.limit:
            self.sleep()
            return False
        self.calls += 1
        return True


routes = {}

def limiter(url: str):
    #how to get route
    if url not in routes:
        routes[url] = Route()
    if routes[url].callable() == False:
        raise_error((429, "Console limit reached."))