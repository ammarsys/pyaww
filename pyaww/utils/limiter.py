import asyncio
import time
from datetime import datetime, timedelta

SLEEPING_TIME = 1
class Route:
    """ Each called route will create a Route class that manages itself to limit itself """
    
    def __init__(self, url) -> None:
        self.limit = 40 if not is_console_input(url) else 120
        self.calls = 0
        self.url = url
        self.timer_end = datetime.now()

    def check_timer(self) -> None:
        """ checks if the timer for the limit rate has expired """
        now = datetime.now()
        if now > self.timer_end:
            self.calls = 1
        else:
            self.timer_end = now + timedelta(minutes = SLEEPING_TIME)


    def sleep_until(self) -> datetime:
        """ returns the time in which the route will reset its limit """
        return self.timer_end

    def callable(self) -> bool:
        """ returns whether the route is currently callable or not """
        self.check_timer()
        if self.calls >= self.limit:
            return False
        self.calls += 1
        return True

def is_console_input(url: str) -> bool:
        return url.split('/')[-2] == 'send_input'