import asyncio
import time
from datetime import datetime, timedelta

SLEEPING_TIME = 1
class Route:
    def __init__(self, url) -> None:
        self.limit = 40
        self.calls = 0
        self.url = url
        self.timer_end = datetime.now()

    def check_timer(self) -> None:
        now = datetime.now()
        if now > self.timer_end:
            self.calls = 1
        else:
            self.timer_end = now + timedelta(minutes = SLEEPING_TIME)


    def sleep_until(self) -> datetime:
        return self.timer_end

    def callable(self) -> bool:
        self.check_timer()
        if self.calls >= self.limit:
            return False
        self.calls += 1
        return True