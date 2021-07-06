from .sched_task import SchedTask

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class AlwaysOnTask(SchedTask):
    """Inherits sheduled task class because they're pretty similar. Only 1 method difference."""
    def __init__(self, resp: dict, user: 'User') -> None:
        super().__init__(resp, user)

    def restart(self) -> None:
        """Restart a always_on task."""
        self._user.request('POST', self.url + 'restart/')

    def __str__(self):
        return self.url
